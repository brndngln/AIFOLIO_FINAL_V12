"""
AIFOLIO™ SAFE AI MODULE: Webhook Triggers
- Static only. No sentience, recursion, or adaptive logic.
- Sends webhooks for refund issued, download started, vault version update.
- All actions logged for auditability.
"""
import json
import logging
import requests

LOG_PATH = "../../distribution/legal_exports/webhook_trigger_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

WEBHOOK_URLS = {
    "refund_issued": "https://your.webhook.url/refund",
    "download_started": "https://your.webhook.url/download",
    "vault_version_update": "https://your.webhook.url/vault_version"
}

def send_webhook(event, payload):
    url = WEBHOOK_URLS.get(event)
    if not url:
        logging.error(f"No webhook URL for event: {event}")
        return False
    try:
        resp = requests.post(url, json=payload)
        logging.info(f"Webhook {event} sent: {resp.status_code}")
        return resp.status_code == 200
    except Exception as e:
        logging.error(f"Webhook {event} failed: {e}")
        return False
