import cv2
import numpy as np
from app.vision.deepfake_detector import deepfake_risk

def analyze_image(file_bytes):
    nparr = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    result = deepfake_risk(image)

    if result["deepfake_score"] > 0.6:
        result["risk_level"] = "high"
    else:
        result["risk_level"] = "low"

    return result
