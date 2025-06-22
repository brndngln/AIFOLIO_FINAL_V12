import json
import datetime
import os

GUMROAD_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/gumroad_sync_log.jsonl'))
os.makedirs(os.path.dirname(GUMROAD_LOG), exist_ok=True)

def sync_gumroad(vault_id, metadata):
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'metadata': metadata,
        'status': 'synced'
    }
    with open(GUMROAD_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry
