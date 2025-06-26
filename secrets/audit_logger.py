import os
import json
from datetime import datetime

AUDIT_LOG_PATH = os.path.join(os.path.dirname(__file__), '../logs/secret_rotation_audit.json')

# Log event: never log secret value
def log_rotation_event(key, status, error=None):
    entry = {
        'key': key,
        'status': status,
        'timestamp': datetime.utcnow().isoformat(),
        'error': error
    }
    os.makedirs(os.path.dirname(AUDIT_LOG_PATH), exist_ok=True)
    if os.path.exists(AUDIT_LOG_PATH):
        with open(AUDIT_LOG_PATH, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(entry)
    with open(AUDIT_LOG_PATH, 'w') as f:
        json.dump(logs, f, indent=2)
