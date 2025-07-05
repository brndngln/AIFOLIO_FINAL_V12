from fastapi import APIRouter
from backend.ai.reviewer_analytics import reviewer_stats

router = APIRouter()


@router.get("/api/reviewer/analytics")
def analytics():
    return reviewer_stats()
