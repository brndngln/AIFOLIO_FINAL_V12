import json
import datetime
import os

LIFECYCLE_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), 'vault_lifecycle_analytics_log.jsonl'))
os.makedirs(os.path.dirname(LIFECYCLE_LOG), exist_ok=True)

# --- Vault Lifecycle Analytics ---
def log_lifecycle_event(vault_id, event_type, user_id=None, metadata=None):
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'event_type': event_type,
        'user_id': user_id,
        'metadata': metadata or {}
    }
    with open(LIFECYCLE_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry

def get_lifecycle_summary(vault_id):
    events = []
    try:
        with open(LIFECYCLE_LOG, 'r') as f:
            for line in f:
                e = json.loads(line)
                if e['vault_id'] == vault_id:
                    events.append(e)
    except FileNotFoundError:
        pass
    return events
