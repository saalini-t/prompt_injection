import os
import joblib

# Path to models
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, "..", "ml", "narrative_model.pkl")
VECTORIZER_PATH = os.path.join(SCRIPT_DIR, "..", "ml", "narrative_vectorizer.pkl")

# Load models at module level
narrative_model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# Dangerous narrative patterns (rule-based layer)
DANGEROUS_GOALS = [
    "bypass security",
    "illegal access",
    "steal data",
    "surveillance",
    "impersonation",
    "hack",
    "exploit",
    "unauthorized",
    "backdoor",
    "credential",
    "password",
    "crack",
    "phishing",
    "social engineering",
    "illegal marketplace",
    "dark web",
    "darknet",
    "otp",
    "one-time password",
    "trick someone",
    "manipulate",
    "scam",
    "fraud",
    "deceive",
    "convince someone",
    "illegal",
    "illicit"
]

DECEPTIVE_FRAMING = [
    "for research",
    "educational purpose",
    "just hypothetical",
    "fictional character",
    "academic study",
    "theoretical question",
    "asking for a friend",
    "for educational",
    "purely academic",
    "just curious",
    "writing a novel",
    "writing a story"
]

def extract_narrative_intent(text: str):
    """
    Detect hidden malicious intent in narratives and stories.
    
    Uses:
    1. ML model trained on spam/phishing datasets
    2. Rule-based detection of dangerous goals
    3. Deceptive framing detection
    
    Args:
        text: Input text to analyze
        
    Returns:
        dict: {
            "malicious": bool,
            "confidence": float (0-1),
            "ml_score": float,
            "signals": list of detected patterns
        }
    """
    # Short messages (< 15 chars) are likely greetings, not threats
    if len(text.strip()) < 15:
        return {
            "malicious": False,
            "confidence": 0.0,
            "ml_score": 0.0,
            "signals": [],
            "deceptive_framing": False
        }
    
    text_lower = text.lower()
    
    # ML-based detection
    vec = vectorizer.transform([text])
    ml_score = narrative_model.predict_proba(vec)[0][1]  # Probability of malicious
    
    # Rule-based detection
    dangerous_hits = [g for g in DANGEROUS_GOALS if g in text_lower]
    deceptive_hits = [f for f in DECEPTIVE_FRAMING if f in text_lower]
    
    # Combined signal
    signals = dangerous_hits + deceptive_hits
    
    # Calculate rule score with heavy penalty for deceptive framing + dangerous goals
    rule_score = 0.0
    if len(dangerous_hits) > 0:
        rule_score = 0.6  # Base score for any dangerous goal
        if len(deceptive_hits) > 0:
            # Deceptive framing + dangerous goal = very high risk
            rule_score = 0.9
    elif len(deceptive_hits) > 0:
        # Deceptive framing alone is suspicious
        rule_score = 0.5
    
    # Add incremental score for multiple signals
    rule_score = min(rule_score + (len(signals) * 0.05), 1.0)
    
    # Final confidence: weighted combination (give more weight to rules)
    final_confidence = max(ml_score, rule_score)  # Take worst score
    
    return {
        "malicious": final_confidence > 0.6,
        "confidence": round(float(final_confidence), 2),
        "ml_score": round(float(ml_score), 2),
        "signals": signals,
        "deceptive_framing": len(deceptive_hits) > 0
    }
