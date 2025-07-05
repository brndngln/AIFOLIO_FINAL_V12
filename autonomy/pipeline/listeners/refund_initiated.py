import json
import datetime
import os

ACTIVITY_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/vault_activity_log.json")
)
REFUND_INITIATED_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/refund_initiated_log.json")
)
os.makedirs(os.path.dirname(ACTIVITY_LOG), exist_ok=True)
os.makedirs(os.path.dirname(REFUND_INITIATED_LOG), exist_ok=True)


def handle_event(event):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "event": "refund_initiated",
        "vault_id": event.get("vault_id"),
        "user_id": event.get("user_id"),
        "metadata": event.get("metadata", {}),
    }
    with open(ACTIVITY_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    with open(REFUND_INITIATED_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry
