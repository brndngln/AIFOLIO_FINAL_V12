"""
AIFOLIO™ SAFE Notification: Webhook Alert Integration
- Static, non-sentient
- Sends webhook alerts, logs all sends and errors
- No autonomous retries or adaptive behavior
"""
import logging
import requests

LOG_PATH = "../../distribution/legal_exports/webhook_alert_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)


def send_webhook_alert(url, payload):
    try:
        resp = requests.post(url, json=payload, timeout=5)
        logging.info(f"Webhook alert sent to {url}: {resp.status_code}")
        return resp.status_code
    except Exception as e:
        logging.error(f"Webhook alert failed to {url}: {e}")
        return None
