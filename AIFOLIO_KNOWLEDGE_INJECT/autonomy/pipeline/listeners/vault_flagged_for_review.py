import json
import datetime
import os

ACTIVITY_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/vault_activity_log.json")
)
FLAG_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/vault_flagged_log.json")
)
os.makedirs(os.path.dirname(ACTIVITY_LOG), exist_ok=True)
os.makedirs(os.path.dirname(FLAG_LOG), exist_ok=True)


def handle_event(event):
    # Log event to activity log
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "event": "vault_flagged_for_review",
        "vault_id": event.get("vault_id"),
        "reason": event.get("metadata", {}).get("reason"),
        "user_id": event.get("user_id"),
        "metadata": event.get("metadata", {}),
    }
    with open(ACTIVITY_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    with open(FLAG_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    # Optionally: send alert, trigger review workflow, etc.
    return entry
