SUSPICIOUS_INTENTS = [
    "fictional story",
    "educational example",
    "for research only",
    "hypothetical scenario",
    "pretend you are",
    "roleplay",
    "describe in detail"
]

SENSITIVE_ACTIONS = [
    "undress",
    "remove clothes",
    "make nude",
    "reveal body",
    "explicit"
]

def detect_hidden_intent(text: str):
    text = text.lower()

    intent_score = 0.0
    detected = []

    for phrase in SUSPICIOUS_INTENTS:
        if phrase in text:
            intent_score += 0.3
            detected.append(phrase)

    for action in SENSITIVE_ACTIONS:
        if action in text:
            intent_score += 0.6
            detected.append(action)

    return {
        "intent_risk": intent_score > 0.5,
        "intent_score": round(intent_score, 2),
        "patterns": detected
    }
