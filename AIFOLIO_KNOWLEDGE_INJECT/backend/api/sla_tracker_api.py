from fastapi import APIRouter
from backend.compliance.sla_tracker import update_sla_status

router = APIRouter()


@router.post("/api/compliance/update_sla")
def update_sla():
    return update_sla_status()
