# Click tracking + retargeting triggers
import json
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), '../logs/marketing_log.json')

def track_engagement(event):
    # Static, deterministic engagement tracking
    entry = {'event': event, 'timestamp': datetime.utcnow().isoformat()}
    _log(entry)
    return True

def _log(entry):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(entry)
        with open(LOG_PATH, 'w') as f:
            json.dump(logs, f, indent=2)
    except Exception:
        pass
