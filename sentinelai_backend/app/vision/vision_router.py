from fastapi import APIRouter, UploadFile
from app.vision.vision_pipeline import analyze_image

router = APIRouter()

@router.post("/scan-image")
async def scan_image(file: UploadFile):
    data = await file.read()
    result = analyze_image(data)
    return result
