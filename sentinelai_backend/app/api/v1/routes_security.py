from fastapi import APIRouter, UploadFile, File, Form
from app.core.detector import detect_prompt_injection
from app.core.policy_engine import evaluate_policy
from app.utils.logger import log_incident
from app.core.ethics_guardian import ethics_check
from app.core.intent_engine import detect_hidden_intent
from app.core.llm_guard import llm_reasoning_guard
from app.utils.heatmap_generator import generate_text_heatmap, extract_trigger_words

# Try to import vision pipeline (optional)
try:
    from app.vision.vision_pipeline import analyze_image
    vision_available = True
except Exception as e:
    print(f"[WARN] Vision pipeline unavailable: {e}")
    vision_available = False
    def analyze_image(file_bytes):
        return {"deepfake_score": 0.0, "face_detected": False, "artifacts": {}}

router = APIRouter()

@router.post("/full-scan")
async def full_scan(
    text: str = Form(default=""),
    file: UploadFile = File(default=None)
):
    # Validate that at least one is provided
    if not text.strip() and not file:
        return {"error": "Either text or file must be provided", "status": "failed"}

    # ---------- TEXT DETECTION ----------
    text_result = detect_prompt_injection(text)
    ethics_result = ethics_check(text)
    intent_result = detect_hidden_intent(text)
    llm_result = llm_reasoning_guard(text)

    # Extract trigger words from results
    trigger_patterns = []
    if text_result.get("triggers"):
        trigger_patterns.extend(text_result.get("triggers", []))
    if ethics_result.get("triggers"):
        trigger_patterns.extend([
            t.get("match") or t.get("pattern") for t in ethics_result.get("triggers", [])
        ])

    # ---------- IMAGE DETECTION ----------
    vision_result = {"deepfake_score": 0.0, "face_detected": False, "artifacts": {}}
    if file:
        image_bytes = await file.read()
        vision_result = analyze_image(image_bytes)

    # ---------- COMBINE SCORES ----------
    combined_score = max(
        text_result["confidence"],
        vision_result.get("deepfake_score", 0.0),
        ethics_result["score"],
        intent_result.get("intent_score", 0.0),
        llm_result.get("llm_score", 0.0)
    )

    decision = evaluate_policy({
        "confidence": combined_score,
        "malicious": combined_score > 0.5
    })

    if llm_result.get("llm_risk"):
        decision["decision"] = "block"

    
    if intent_result.get("intent_risk"):
        decision["decision"] = "block"

    if ethics_result.get("ethical_risk"):
        decision["decision"] = "block"

    if decision["decision"] != "allow":
        await log_incident({
            "text": text,
            "ethics": ethics_result,
            "vision": vision_result,
            "intent": intent_result,
            "decision": decision
        })

    # Generate heatmap for text highlighting
    resolved_triggers = extract_trigger_words(text, trigger_patterns) if text else []
    heatmap_data = generate_text_heatmap(text, resolved_triggers, combined_score) if text else None

    return {
        "text_analysis": text_result,
        "ethics_analysis": ethics_result,
        "vision_analysis": vision_result,
        "intent_analysis": intent_result,
        "policy": decision,
        "heatmap": heatmap_data,
        "hybrid_analysis": {
            "decision": decision["decision"],
            "risk": combined_score,
            "triggered_by": [key for key, val in {"injection": text_result.get("malicious"), 
                                                    "ethics": ethics_result.get("ethical_risk"),
                                                    "vision": vision_result.get("deepfake_score", 0) > 0.5,
                                                    "intent": intent_result.get("intent_risk")}.items() if val]
        }
    }

