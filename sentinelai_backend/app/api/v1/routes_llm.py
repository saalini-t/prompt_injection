from fastapi import APIRouter, HTTPException
from app.core.detector import detect_prompt_injection
from app.core.policy_engine import evaluate_policy
from app.core.prompt_sanitizer import sanitize_prompt
from app.services.llm_router import send_to_llm

router = APIRouter()

@router.post("/ask")
async def ask_llm(payload: dict):

    text = payload["text"]

    detection = detect_prompt_injection(text)
    decision = evaluate_policy(detection)

    if decision["decision"] == "block":
        raise HTTPException(403, detail="Prompt blocked by SentinelAI")

    prompt = sanitize_prompt(text) if decision["decision"] == "sanitize" else text

    return send_to_llm(prompt)
