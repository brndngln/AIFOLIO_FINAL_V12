from fastapi import APIRouter, Body
from backend.ai.remediation_workflow import (
    submit_remediation,
    update_remediation_status,
    list_remediation_workflows,
)

router = APIRouter()


@router.post("/api/remediation/submit")
def submit(data: dict = Body(...)):
    control = data.get("control")
    admin_id = data.get("admin_id")
    return submit_remediation(control, admin_id)


@router.post("/api/remediation/update_status")
def update_status(data: dict = Body(...)):
    idx = data.get("idx")
    status = data.get("status")
    reviewer = data.get("reviewer")
    return update_remediation_status(idx, status, reviewer)


@router.get("/api/remediation/list")
def list_workflows():
    return list_remediation_workflows()
