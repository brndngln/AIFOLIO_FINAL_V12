import requests
import json
from datetime import datetime


def send_webhook(url, event_type, payload):
    data = {
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "payload": payload,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers, timeout=10)
    response.raise_for_status()
    return response.status_code


# Example usage:
# send_webhook('https://hooks.slack.com/services/XXX/YYY/ZZZ', 'sla_breach', {'violation_id': 123, 'sla_status': 'danger'})
