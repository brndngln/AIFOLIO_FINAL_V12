import json
import datetime

# Emma Compliance Lock
OWNER_LOCK = True
import os

ACTIVITY_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/vault_activity_log.jsonl")
)
os.makedirs(os.path.dirname(ACTIVITY_LOG), exist_ok=True)


# --- Vault Activity Log ---
def log_vault_activity(event, user_id, action, result):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "event": event,
        "user_id": user_id,
        "action": action,
        "result": result,
    }
    with open(ACTIVITY_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry
