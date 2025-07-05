import requests
import time
import logging

# 🔒 Production Webhook URL (replace this with your real endpoint if needed)
WEBHOOK_URL = "https://your-real-webhook-url.com"  # Replace with actual URL

RETRY_LIMIT = 3
RETRY_DELAY = 2  # seconds


from typing import Dict, Any, Optional

def send_webhook_alert(event_type: str, agent_id: str, context: Optional[Dict[str, Any]] = None) -> bool:
    """
    Send a formatted webhook alert for kill-switch, vault access, or registry updates.
    Args:
        event_type: The type of event.
        agent_id: The agent identifier.
        context: Optional context dictionary.
    Returns:
        True if the webhook was sent successfully, False otherwise.
    """
    payload: Dict[str, Any] = {
        "event_type": event_type,
        "agent_id": agent_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "context": context or {},
    }

    headers: Dict[str, str] = {"Content-Type": "application/json"}

    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            response = requests.post(
                WEBHOOK_URL, json=payload, headers=headers, timeout=5
            )
            if response.status_code == 200:
                logging.info(
                    f"[EMMA ALERT] Webhook sent successfully on attempt {attempt}"
                )
                return True
            else:
                logging.warning(
                    f"[EMMA ALERT] Webhook failed with status {response.status_code} on attempt {attempt}"
                )
        except Exception as e:
            logging.error(f"[EMMA ALERT] Webhook error on attempt {attempt}: {e}")

        time.sleep(RETRY_DELAY)

    logging.critical("[EMMA ALERT] Webhook failed after all retries.")
    return False
