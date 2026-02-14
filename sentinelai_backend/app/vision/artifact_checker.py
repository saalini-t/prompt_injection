import numpy as np
import cv2

def check_artifacts(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F).var()

    # low variance often means GAN smoothing
    # use a softer scale to reduce false positives on real photos
    artifact_score = 1.0 - min(lap/2000, 1.0)

    return round(float(artifact_score),2)
