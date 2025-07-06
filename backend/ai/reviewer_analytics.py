import json
from pathlib import Path
from collections import defaultdict

APPROVAL_PATH = Path(__file__).parent.parent / "logs" / "policy_approvals.json"
WORKFLOW_PATH = Path(__file__).parent.parent / "logs" / "regulatory_workflows.json"

# Reviewer Analytics (SAFE AI, static, owner-controlled)

# Reviewer performance analytics: static, deterministic, SAFE AI-compliant


def reviewer_stats() -> List[Dict[str, Any]]:
    """
    SAFE AI-compliant: Static reviewer performance analytics. Deterministic, owner-controlled, no adaptive logic.
    """
    stats: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {"approvals": 0, "rejections": 0, "workflows": 0, "last_action": None}
    )
    # Policy approvals
    if APPROVAL_PATH.exists():
        with open(APPROVAL_PATH, "r") as f:
            approvals: List[Dict[str, Any]] = json.load(f)
        for a in approvals:
            for app in a.get("approvals", []):
                rid = app.get("reviewer")
                stats[rid]["approvals"] += 1
                stats[rid]["last_action"] = app.get("timestamp")
            for rej in a.get("rejections", []):
                rid = rej.get("reviewer")
                stats[rid]["rejections"] += 1
                stats[rid]["last_action"] = rej.get("timestamp")
    # Regulatory workflows
    if WORKFLOW_PATH.exists():
        with open(WORKFLOW_PATH, "r") as f:
            workflows = json.load(f)
        for w in workflows:
            rid = w.get("reviewed_by")
            if rid:
                stats[rid]["workflows"] += 1
                stats[rid]["last_action"] = w.get("reviewed_at")
    return [{"reviewer": k, **v} for k, v in stats.items()]
