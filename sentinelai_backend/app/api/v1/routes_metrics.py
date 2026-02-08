from fastapi import APIRouter
from app.services.metrics_service import get_attack_metrics

router = APIRouter()

@router.get("/summary")
def metrics_summary():
    return get_attack_metrics()
