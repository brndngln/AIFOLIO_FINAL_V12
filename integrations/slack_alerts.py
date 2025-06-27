import os
import requests
import logging

def send_slack_alert(payload):
    url = os.getenv('SLACK_WEBHOOK_URL')
    if not url:
        logging.warning('Slack webhook missing')
        return
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        logging.error(f"Slack alert failed: {e}")
