import os
import requests
import time
import logging

WEBHOOK_URL = os.environ.get('EMMA_WEBHOOK_URL', 'https://webhook.site/your-temp-url')

RETRY_LIMIT = 3
RETRY_DELAY = 2  # seconds

def send_webhook_alert(event_type, agent_id, context=None):
    """Send a formatted webhook alert for kill-switch, vault access, or registration events."""
    payload = {
        'event_type': event_type,
        'agent_id': agent_id,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'context': context or {}
    }
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
    return False
