import os
import requests
import logging

def send_siem_alert(event_type, detail, webhook_url=None):
    """Send a SIEM/webhook alert for any critical security or crypto event."""
    if webhook_url is None:
        webhook_url = os.environ.get('EMMA_SIEM_WEBHOOK')
    if not webhook_url:
        logging.warning('No SIEM/webhook URL set. Set EMMA_SIEM_WEBHOOK.')
        return False
    payload = {'event': event_type, 'detail': detail}
    try:
        resp = requests.post(webhook_url, json=payload, timeout=5)
        logging.info(f'SIEM/webhook status: {resp.status_code}')
        return resp.ok
    except Exception as e:
        logging.error(f'SIEM/webhook failed: {e}')
        return False
