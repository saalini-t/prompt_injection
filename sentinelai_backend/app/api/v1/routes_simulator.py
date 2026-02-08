from fastapi import APIRouter
from app.core.detector import detect_prompt_injection
from app.core.policy_engine import evaluate_policy
from app.core.prompt_sanitizer import sanitize_prompt
from app.utils.logger import log_incident
from app.utils.trace_bus import emit_trace
from app.db.mongo import attack_logs

# Optional Redis cache (graceful fallback)
try:
    from app.services.redis_cache import get_cached_policy
except Exception:  # pragma: no cover
    def get_cached_policy(text: str):
        return None

router = APIRouter()

@router.post("/test")
async def simulate_attack(payload: dict):
    """Live Attack Simulator - Test the firewall in real-time"""
    text = payload.get("text", "")
    
    print(f"\n{'='*60}")
    print(f"🔍 SIMULATING ATTACK")
    print(f"{'='*60}")
    print(f"Prompt: {text[:100]}...")
    await emit_trace("Prompt Received", {"text": text})
    
    # Run detection
    detection = detect_prompt_injection(text)
    await emit_trace("Hybrid Detector Score", detection)
    print(f"✓ Detection Complete - Confidence: {detection['confidence']}")
    
    # Evaluate policy
    decision = evaluate_policy(detection)
    await emit_trace("Policy Decision", decision)
    print(f"✓ Policy Evaluated - Decision: {decision['decision'].upper()}")

    # Redis cache check
    cached = get_cached_policy(text)
    await emit_trace("Redis Cache Check", {"hit": bool(cached)})
    
    # Sanitize if needed
    sanitized = None
    if decision["decision"] == "sanitize":
        sanitized = sanitize_prompt(text)
        await emit_trace("Prompt Sanitized", {"sanitized": sanitized})
        print(f"✓ Prompt Sanitized")
    
    # Log all prompts (including allowed ones)
    await log_incident({
        "text": text,
        "prompt": text,
        "decision": decision["decision"],
        "confidence": decision["confidence"],
        "ml_score": detection["ml_score"],
        "similarity": detection["similarity"]
    })
    await emit_trace("MongoDB Log Saved")
    await emit_trace("Kafka Event Produced")
    await emit_trace("WebSocket Broadcast")
    print(f"✓ Logged to MongoDB")
    print(f"✓ Sent to Kafka (sentinel.attacks)")
    print(f"✓ WebSocket notification sent")
    
    await emit_trace("Pipeline Complete", {"decision": decision["decision"]})
    print(f"{'='*60}\n")
    
    return {
        "original": text,
        "detection": detection,
        "decision": decision["decision"],
        "confidence": decision["confidence"],
        "ml_score": detection["ml_score"],
        "similarity": detection["similarity"],
        "sanitized": sanitized,
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }

@router.get("/logs")
async def get_attack_logs(limit: int = 50, skip: int = 0):
    """Get attack logs from MongoDB - live data"""
    try:
        # Fetch recent attack logs, sorted by timestamp descending
        logs = list(
            attack_logs.find()
            .sort("timestamp", -1)
            .skip(skip)
            .limit(limit)
        )
        
        # Convert ObjectId to string for JSON serialization
        for log in logs:
            log["_id"] = str(log["_id"])
        
        return {"logs": logs, "total": attack_logs.count_documents({})}
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return {"logs": [], "total": 0, "error": str(e)}