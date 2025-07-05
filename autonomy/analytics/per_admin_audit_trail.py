"""
Per-admin audit trail logger
- Logs which admin triggered which events/actions
- 100% static, non-sentient, SAFE
"""
import os
import json
import datetime

AUDIT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../analytics/per_admin_audit_trail.json")
)
os.makedirs(os.path.dirname(AUDIT_PATH), exist_ok=True)


def log_admin_action(admin_id, action, details):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "admin_id": admin_id,
        "action": action,
        "details": details,
    }
    with open(AUDIT_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry
