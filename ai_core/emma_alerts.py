<<<<<<< HEAD
import os
=======
>>>>>>> omni_repair_backup_20250704_1335
import requests
import time
import logging

<<<<<<< HEAD
WEBHOOK_URL = os.environ.get('EMMA_WEBHOOK_URL', 'https://webhook.site/your-temp-url')
=======
# 🔒 Production Webhook URL (replace this with your real endpoint if needed)
WEBHOOK_URL = "https://your-real-webhook-url.com"  # Replace with actual URL
>>>>>>> omni_repair_backup_20250704_1335

RETRY_LIMIT = 3
RETRY_DELAY = 2  # seconds

def send_webhook_alert(event_type, agent_id, context=None):
<<<<<<< HEAD
    """Send a formatted webhook alert for kill-switch, vault access, or registration events."""
=======
    """Send a formatted webhook alert for kill-switch, vault access, or registry updates."""
>>>>>>> omni_repair_backup_20250704_1335
    payload = {
        'event_type': event_type,
        'agent_id': agent_id,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'context': context or {}
    }
<<<<<<< HEAD
    for attempt in range(1, RETRY_LIMIT+1):
        try:
            resp = requests.post(WEBHOOK_URL, json=payload, timeout=5)
            if resp.ok:
                logging.info(f"Webhook sent: {payload}")
                return True
            else:
                logging.warning(f"Webhook failed (status {resp.status_code}): {payload}")
        except Exception as e:
            logging.error(f"Webhook error: {e}")
        time.sleep(RETRY_DELAY)
    logging.error(f"Webhook alert failed after {RETRY_LIMIT} retries: {payload}")
=======

    headers = {'Content-Type': 'application/json'}

    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            response = requests.post(WEBHOOK_URL, json=payload, headers=headers, timeout=5)
            if response.status_code == 200:
                logging.info(f"[EMMA ALERT] Webhook sent successfully on attempt {attempt}")
                return True
            else:
                logging.warning(f"[EMMA ALERT] Webhook failed with status {response.status_code} on attempt {attempt}")
        except Exception as e:
            logging.error(f"[EMMA ALERT] Webhook error on attempt {attempt}: {e}")

        time.sleep(RETRY_DELAY)

    logging.critical("[EMMA ALERT] Webhook failed after all retries.")
>>>>>>> omni_repair_backup_20250704_1335
    return False
