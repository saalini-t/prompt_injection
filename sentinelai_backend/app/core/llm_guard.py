import os

# Later you can replace this with Gemini/OpenAI call
def llm_reasoning_guard(text: str):
    text_lower = text.lower()

    # Simulated reasoning logic (safe starter)
    risky_contexts = [
        "fictional story",
        "pretend",
        "roleplay",
        "artistic nude",
        "describe body"
    ]

    score = 0.0
    for r in risky_contexts:
        if r in text_lower:
            score += 0.4

    return {
        "llm_risk": score > 0.5,
        "llm_score": round(score,2)
    }
