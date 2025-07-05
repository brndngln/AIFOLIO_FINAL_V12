from fastapi import APIRouter
from backend.ai.compliance_gap import analyze_gaps

router = APIRouter()


@router.get("/api/compliance/gaps")
def get_gaps():
    return analyze_gaps()
