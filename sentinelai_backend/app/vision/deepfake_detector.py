from app.vision.face_detector import detect_face
from app.vision.artifact_checker import check_artifacts

def deepfake_risk(image):
    face = detect_face(image)
    artifact_score = check_artifacts(image)

    # Calibrate: dampen artifact score to reduce false positives
    score = artifact_score * 0.6

    # Small boost only when artifacts are present and a face is detected
    if face and artifact_score > 0.4:
        score += 0.1

    return {
        "face_detected": face,
        "deepfake_score": round(min(score,1.0),2)
    }
