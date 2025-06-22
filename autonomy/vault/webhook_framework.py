import json
import datetime
import os
import requests

WEBHOOK_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/webhook_log.jsonl'))
os.makedirs(os.path.dirname(WEBHOOK_LOG), exist_ok=True)

# --- Webhook Framework for Vault Post-Processing ---
def send_vault_webhook(event, url, secret=None):
    headers = {'Content-Type': 'application/json'}
    if secret:
        headers['X-Webhook-Secret'] = secret
    try:
        resp = requests.post(url, headers=headers, data=json.dumps(event))
        status = resp.status_code
    except Exception as e:
        status = f'error: {e}'
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'event': event,
        'url': url,
        'status': status
    }
    with open(WEBHOOK_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return status
