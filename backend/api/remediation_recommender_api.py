from fastapi import APIRouter
from backend.ai.remediation_recommender import recommend_remediation

router = APIRouter()

@router.get('/api/compliance/remediation')
def get_remediation():
    return recommend_remediation()
