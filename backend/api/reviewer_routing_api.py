from fastapi import APIRouter, Body
from backend.ai.reviewer_routing import assign_custom_reviewers

router = APIRouter()


@router.post("/api/reviewer/custom_assign")
def custom_assign(data: dict = Body(...)):
    idx = data.get("idx")
    policy_type = data.get("policy_type")
    num_reviewers = data.get("num_reviewers", 2)
    return assign_custom_reviewers(idx, policy_type, num_reviewers)
