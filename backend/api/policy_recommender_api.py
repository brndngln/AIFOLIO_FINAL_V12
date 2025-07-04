from fastapi import APIRouter
from backend.ai.policy_recommender import recommend_policies

router = APIRouter()

@router.get('/api/policy/recommend')
def policy_recommend():
    return recommend_policies()
