import requests
import os
import datetime
import json

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")
ALERT_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/telegram_alert_log.jsonl")
)
os.makedirs(os.path.dirname(ALERT_LOG), exist_ok=True)


# --- Telegram Alert Channel for Admins ---
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_ADMIN_CHAT_ID, "text": message}
    resp = requests.post(url, data=data)
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "message": message,
        "response_code": resp.status_code,
    }
    with open(ALERT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return resp.status_code


if __name__ == "__main__":
    print(send_telegram_alert("Test alert from AIFOLIO™"))
