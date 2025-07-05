# Emma Compliance Lock
OWNER_LOCK = True
import os
import json
import datetime
from autonomy.integrations.telegram_alerts import send_telegram_alert

# Slack integration stub (implemented below)

ALERT_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/vault_alert_log.jsonl")
)
os.makedirs(os.path.dirname(ALERT_LOG), exist_ok=True)

import requests
import dotenv

dotenv.load_dotenv()
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")


# --- Vault Alerting ---
def send_vault_alert(event, channel="telegram"):
    msg = f"[Vault Event] {event['event']} for vault {event['vault_id']} by user {event['user_id']}"
    if channel == "telegram":
        send_telegram_alert(msg)
    elif channel == "slack" and SLACK_WEBHOOK:
        requests.post(SLACK_WEBHOOK, json={"text": msg})
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "event": event,
        "channel": channel,
    }
    with open(ALERT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return True


if __name__ == "__main__":
    send_vault_alert(
        {"event": "vault_created", "vault_id": "vault123", "user_id": "user456"},
        channel="slack",
    )
