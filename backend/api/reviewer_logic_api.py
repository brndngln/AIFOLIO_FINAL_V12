from fastapi import APIRouter, Body
from pathlib import Path
import json
from datetime import datetime

WORKFLOW_PATH = (
    Path(__file__).parent.parent.parent / "logs" / "regulatory_workflows.json"
)

router = APIRouter()


@router.post("/api/reviewer/update_status")
def update_status(data: dict = Body(...)):
    idx = data.get("idx")
    status = data.get("status")
    reviewer = data.get("reviewer")
    if WORKFLOW_PATH.exists():
        with open(WORKFLOW_PATH, "r") as f:
            workflows = json.load(f)
    else:
        return {"success": False, "error": "No workflows"}
    if idx is not None and 0 <= idx < len(workflows):
        workflows[idx]["status"] = status
        workflows[idx]["reviewed_by"] = reviewer
        workflows[idx]["reviewed_at"] = datetime.utcnow().isoformat()
        with open(WORKFLOW_PATH, "w") as f:
            json.dump(workflows, f, indent=2)
        return {"success": True, "workflow": workflows[idx]}
    return {"success": False, "error": "Invalid index"}
