import json
from pathlib import Path
from datetime import datetime

REVIEWERS_PATH = Path(__file__).parent.parent / "config" / "reviewers.json"
APPROVAL_PATH = Path(__file__).parent.parent / "logs" / "policy_approvals.json"

# Deterministic, SAFE AI-compliant custom reviewer routing
# Assign by expertise, load, and history


def route_reviewer(policy_type, exclude=None):
    if exclude is None:
        exclude = []
    if not REVIEWERS_PATH.exists():
        return []
    with open(REVIEWERS_PATH, "r") as f:
        reviewers = json.load(f)
    # Reviewer: {id, expertise: [types], assigned: int}
    candidates = [
        r
        for r in reviewers
        if policy_type in r.get("expertise", []) and r["id"] not in exclude
    ]
    if not candidates:
        # fallback: any reviewer not excluded
        candidates = [r for r in reviewers if r["id"] not in exclude]
    if not candidates:
        return []
    # Sort by least assigned
    candidates.sort(key=lambda r: r.get("assigned", 0))
    return [candidates[0]["id"]]


def assign_custom_reviewers(idx, policy_type, num_reviewers=2):
    if not APPROVAL_PATH.exists():
        return {"success": False, "error": "No approvals"}
    with open(APPROVAL_PATH, "r") as f:
        approvals = json.load(f)
    assigned = []
    exclude = []
    for _ in range(num_reviewers):
        reviewer = route_reviewer(policy_type, exclude)
        if not reviewer:
            break
        assigned.extend(reviewer)
        exclude.extend(reviewer)
    if idx is not None and 0 <= idx < len(approvals):
        approvals[idx]["assigned_reviewers"] = assigned
        approvals[idx]["assignment_time"] = datetime.utcnow().isoformat()
        with open(APPROVAL_PATH, "w") as f:
            json.dump(approvals, f, indent=2)
        # Update reviewer load
        with open(REVIEWERS_PATH, "r") as f:
            reviewers = json.load(f)
        for r in reviewers:
            if r["id"] in assigned:
                r["assigned"] = r.get("assigned", 0) + 1
        with open(REVIEWERS_PATH, "w") as f:
            json.dump(reviewers, f, indent=2)
        return {"success": True, "assigned": assigned, "record": approvals[idx]}
    return {"success": False, "error": "Invalid index"}
