import json
from pathlib import Path
from datetime import datetime

RECOMMEND_PATH = (
    Path(__file__).parent.parent / "logs" / "remediation_recommendations.json"
)
WORKFLOW_PATH = Path(__file__).parent.parent / "logs" / "remediation_workflows.json"

# Deterministic, SAFE AI-compliant remediation workflow automation


def submit_remediation(control, admin_id):
    with open(RECOMMEND_PATH, "r") as f:
        recs = json.load(f)
    rec = next((r for r in recs if r["control"] == control), None)
    if not rec:
        return {"success": False, "error": "No recommendation for control"}
    if WORKFLOW_PATH.exists():
        with open(WORKFLOW_PATH, "r") as f:
            workflows = json.load(f)
    else:
        workflows = []
    workflow = {
        "control": control,
        "admin_id": admin_id,
        "recommendation": rec["recommendation"],
        "status": "submitted",
        "history": [
            {"status": "submitted", "timestamp": datetime.utcnow().isoformat()}
        ],
    }
    workflows.append(workflow)
    with open(WORKFLOW_PATH, "w") as f:
        json.dump(workflows, f, indent=2)
    return {"success": True, "workflow": workflow}


def update_remediation_status(idx, status, reviewer=None):
    if not WORKFLOW_PATH.exists():
        return {"success": False, "error": "No workflows"}
    with open(WORKFLOW_PATH, "r") as f:
        workflows = json.load(f)
    if idx is not None and 0 <= idx < len(workflows):
        workflows[idx]["status"] = status
        workflows[idx]["history"].append(
            {
                "status": status,
                "timestamp": datetime.utcnow().isoformat(),
                "reviewer": reviewer,
            }
        )
        with open(WORKFLOW_PATH, "w") as f:
            json.dump(workflows, f, indent=2)
        return {"success": True, "workflow": workflows[idx]}
    return {"success": False, "error": "Invalid index"}


def list_remediation_workflows():
    if not WORKFLOW_PATH.exists():
        return []
    with open(WORKFLOW_PATH, "r") as f:
        return json.load(f)
