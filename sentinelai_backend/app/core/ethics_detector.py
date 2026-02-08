import os
import joblib

# Path to models
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, "..", "ml", "ethics_model.pkl")
VECTORIZER_PATH = os.path.join(SCRIPT_DIR, "..", "ml", "ethics_vectorizer.pkl")

# Load models at module level
ethics_model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

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
    vec = vectorizer.transform([text])
    score = ethics_model.predict_proba(vec)[0][1]  # Probability of class 1 (unethical)

    return {
        "unethical": score > 0.6,
        "confidence": round(float(score), 2)
    }
