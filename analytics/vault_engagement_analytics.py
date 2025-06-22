import json
import datetime
import os

ENGAGEMENT_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), 'vault_engagement_analytics_log.jsonl'))
os.makedirs(os.path.dirname(ENGAGEMENT_LOG), exist_ok=True)

# --- Vault Engagement Over Time ---
def log_engagement(vault_id, event_type, user_id=None, metadata=None):
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'event_type': event_type,
        'user_id': user_id,
        'metadata': metadata or {}
    }
    with open(ENGAGEMENT_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry

def calculate_engagement(vault_id, since_days=30):
    now = datetime.datetime.utcnow()
    count = 0
    try:
        with open(ENGAGEMENT_LOG, 'r') as f:
            for line in f:
                e = json.loads(line)
                if e['vault_id'] == vault_id:
                    t = datetime.datetime.fromisoformat(e['timestamp'].replace('Z',''))
                    if (now - t).days <= since_days:
                        count += 1
    except FileNotFoundError:
        pass
    return count
