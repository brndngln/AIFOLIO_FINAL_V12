import json
import datetime

# Emma Compliance Lock
OWNER_LOCK = True
import os

EVENT_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/vault_event_log.jsonl")
)
os.makedirs(os.path.dirname(EVENT_LOG), exist_ok=True)


# --- Vault Creation/Update Event Triggers ---
def on_vault_created(vault_id, user_id, metadata):
    event = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "event": "vault_created",
        "vault_id": vault_id,
        "user_id": user_id,
        "metadata": metadata,
    }
    with open(EVENT_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")
    return event


def on_vault_updated(vault_id, user_id, changes):
    event = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "event": "vault_updated",
        "vault_id": vault_id,
        "user_id": user_id,
        "changes": changes,
    }
    with open(EVENT_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")
    return event


if __name__ == "__main__":
    print(on_vault_created("vault123", "user456", {"title": "AI Vault"}))
    print(on_vault_updated("vault123", "user456", {"title": "AI Vault v2"}))
