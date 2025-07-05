from fastapi import APIRouter
from backend.ai.policy_mapping import map_policies_to_standards

router = APIRouter()


@router.get("/api/policy/mapping")
def get_policy_mapping():
    return map_policies_to_standards()
