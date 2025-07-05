import os
import requests
import logging


def send_n8n_event(payload):
    url = os.getenv("N8N_WEBHOOK_URL")
    if not url:
        logging.warning("n8n webhook missing")
        return
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        logging.error(f"n8n event failed: {e}")
