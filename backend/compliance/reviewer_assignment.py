import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

REVIEWERS_PATH = Path(__file__).parent.parent / "config" / "reviewers.json"
VIOLATION_LOG = Path(__file__).parent.parent / "logs" / "compliance_violations.json"
ASSIGNMENT_LOG = Path(__file__).parent.parent / "logs" / "reviewer_assignments.json"

BADGES = {
    "policy_defender": {"desc": "Most critical issues resolved"},
    "sla_champion": {"desc": "Most on-time remediations"},
    "reviewer_ace": {"desc": "Highest accuracy"},
    "load_balancer": {"desc": "Best load sharing"},
}


def load_reviewers():
    if not REVIEWERS_PATH.exists():
        return []
    with open(REVIEWERS_PATH, "r") as f:
        return json.load(f)


def assign_reviewer(violation, exclude=None):
    reviewers = load_reviewers()
    if not reviewers:
        return None
    if exclude is None:
        exclude = []
    # Only assign human reviewers for critical/major
    candidates = [
        r for r in reviewers if r["type"] == "human" and r["id"] not in exclude
    ]
    if not candidates:
        candidates = [r for r in reviewers if r["id"] not in exclude]
    # Score: lowest load, highest accuracy
    candidates.sort(key=lambda r: (r.get("assigned", 0), -r.get("accuracy", 1.0)))
    return candidates[0]["id"] if candidates else None


def assign_all_open_violations():
    if not VIOLATION_LOG.exists():
        return []
    with open(VIOLATION_LOG, "r") as f:
        violations = json.load(f)
    assignments = []
    for i, v in enumerate(violations):
        if v.get("status") == "open" and not v.get("assigned_reviewer"):
            reviewer_id = assign_reviewer(v)
            if reviewer_id:
                v["assigned_reviewer"] = reviewer_id
                v.setdefault("assignment_history", []).append(
                    {
                        "reviewer": reviewer_id,
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )
                assignments.append({"violation_idx": i, "reviewer": reviewer_id})
    with open(VIOLATION_LOG, "w") as f:
        json.dump(violations, f, indent=2)
    with open(ASSIGNMENT_LOG, "a") as f:
        for a in assignments:
            f.write(json.dumps(a) + "\n")
    return assignments


def reviewer_leaderboard():
    # Aggregate assignments, accuracy, and badges
    if not REVIEWERS_PATH.exists():
        return []
    with open(REVIEWERS_PATH, "r") as f:
        reviewers = json.load(f)
    # Load assignment stats
    stats = defaultdict(
        lambda: {"assigned": 0, "resolved": 0, "sla_met": 0, "badges": []}
    )
    if VIOLATION_LOG.exists():
        with open(VIOLATION_LOG, "r") as f:
            violations = json.load(f)
        for v in violations:
            rid = v.get("assigned_reviewer")
            if rid:
                stats[rid]["assigned"] += 1
                if v.get("status") == "resolved":
                    stats[rid]["resolved"] += 1
                if v.get("sla_status") == "ok":
                    stats[rid]["sla_met"] += 1
    # Assign badges
    for rid, s in stats.items():
        if s["resolved"] > 10:
            s["badges"].append("policy_defender")
        if s["sla_met"] > 10:
            s["badges"].append("sla_champion")
    # Merge with reviewer info
    leaderboard = []
    for r in reviewers:
        entry = {
            "id": r["id"],
            "name": r.get("name"),
            "type": r["type"],
            "accuracy": r.get("accuracy", 1.0),
        }
        entry.update(stats[r["id"]])
        entry["badges"] = [BADGES[b]["desc"] for b in entry["badges"]]
        leaderboard.append(entry)
    leaderboard.sort(key=lambda x: (-x["resolved"], -x["sla_met"], -x["accuracy"]))
    return leaderboard
