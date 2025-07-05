import json
from pathlib import Path
from datetime import datetime

POLICY_PATH = Path(__file__).parent.parent / "config" / "safe_ai_policies.json"
AUDIT_PATH = Path(__file__).parent.parent / "logs" / "safe_ai_policy_audit.json"

# Static, deterministic SAFE AI policy engine
# All logic is OWNER-controlled and fully auditable


def load_policies():
    if POLICY_PATH.exists():
        with open(POLICY_PATH, "r") as f:
            return json.load(f)
    return []


def enforce_policy(event):
    policies = load_policies()
    for p in policies:
        if p["type"] == event["type"]:
            # Static rule example: block if flagged
            if p.get("block") and event.get("flagged"):
                audit = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "policy": p,
                    "event": event,
                    "result": "blocked",
                }
                log_audit(audit)
                return False, "Blocked by SAFE AI policy."
    audit = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event,
        "result": "allowed",
    }
    log_audit(audit)
    return True, "Allowed."


def log_audit(audit):
    audits = []
    if AUDIT_PATH.exists():
        with open(AUDIT_PATH, "r") as f:
            audits = json.load(f)
    audits.append(audit)
    with open(AUDIT_PATH, "w") as f:
        json.dump(audits, f, indent=2)
