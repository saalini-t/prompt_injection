import cv2

_mp_face = None
try:
    import mediapipe as mp
    if hasattr(mp, "solutions") and hasattr(mp.solutions, "face_detection"):
        _mp_face = mp.solutions.face_detection.FaceDetection()
except Exception as e:
    print(f"[WARN] MediaPipe failed to load: {e}")
    _mp_face = None


def detect_face(image):
    if _mp_face is None:
        return False

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = _mp_face.process(rgb)

    return results.detections is not None
