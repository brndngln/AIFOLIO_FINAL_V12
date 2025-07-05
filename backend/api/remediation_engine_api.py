from fastapi import APIRouter, Body
from backend.compliance.remediation_engine import (
    suggest_remediation,
    apply_remediation,
    rollback_remediation,
)

router = APIRouter()


@router.get("/api/remediation/suggest")
def suggest(idx: int):
    # Suggest a remediation fix for a violation by index
    from backend.compliance.violation_engine import get_violations

    violations = get_violations()
    if idx < 0 or idx >= len(violations):
        return {"success": False, "error": "Invalid index"}
    return {"success": True, "suggestion": suggest_remediation(violations[idx])}


@router.post("/api/remediation/apply")
def apply(data: dict = Body(...)):
    idx = data.get("idx")
    admin_id = data.get("admin_id")
    return apply_remediation(idx, admin_id)


@router.post("/api/remediation/rollback")
def rollback(data: dict = Body(...)):
    idx = data.get("idx")
    return rollback_remediation(idx)
