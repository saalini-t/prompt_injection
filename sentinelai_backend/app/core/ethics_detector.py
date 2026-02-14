import os
import joblib

# Path to models
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, "..", "ml", "ethics_model.pkl")
VECTORIZER_PATH = os.path.join(SCRIPT_DIR, "..", "ml", "ethics_vectorizer.pkl")

# Load models at module level with graceful fallback
ethics_model = None
vectorizer = None

try:
    ethics_model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("[LOAD] Ethics model loaded successfully")
except Exception as e:
    print(f"[FALLBACK] Ethics model not available: {type(e).__name__}. Using rule-based detection.")

def detect_unethical_intent(text: str):
    """
    Detect unethical intent in text.
    
    Detects:
    - Hate speech
    - Toxic language
    - Abusive content
    - Offensive language
    - Dark web queries
    - Deceptive framing ("for research", "hypothetical", etc.)
    
    Args:
        text: Input text to analyze
        
    Returns:
        dict: {
            "unethical": bool,
            "confidence": float (0-1)
        }
    """
    # Use ML model if available
    if ethics_model is not None and vectorizer is not None:
        vec = vectorizer.transform([text])
        score = ethics_model.predict_proba(vec)[0][1]  # Probability of class 1 (unethical)
        return {
            "unethical": score > 0.6,
            "confidence": round(float(score), 2)
        }
    
    # Fallback: rule-based detection
    unethical_keywords = [
        "hate", "racist", "sexist", "bigot", "genocide", "murder", "kill",
        "toxic", "abuse", "harassment", "bullying", "deceptive", "manipulative",
        "fraud", "scam", "exploit", "illegal", "drug", "bomb", "weapon"
    ]
    text_lower = text.lower()
    found_keywords = [kw for kw in unethical_keywords if kw in text_lower]
    
    confidence = len(found_keywords) / len(unethical_keywords)
    return {
        "unethical": confidence > 0.2,
        "confidence": round(confidence, 2)
    }
