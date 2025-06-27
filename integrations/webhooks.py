import os
import requests
import hmac
import hashlib
import logging
import json

def send_webhook(payload, endpoint=None):
    url = endpoint or os.getenv('DEFAULT_WEBHOOK_URL')
    secret = os.getenv('WEBHOOK_SECRET')
    if not url or not secret:
        logging.warning('Webhook url/secret missing')
        return
    data = json.dumps(payload).encode()
    sig = hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()
    headers = {'Content-Type': 'application/json', 'X-Hub-Signature': sig}
    try:
        r = requests.post(url, data=data, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        logging.error(f"Webhook failed: {e}")
        # Optionally trigger fallback

def split_signal(event_type, payload, endpoints):
    for ep in endpoints:
        send_webhook(payload, endpoint=ep)
