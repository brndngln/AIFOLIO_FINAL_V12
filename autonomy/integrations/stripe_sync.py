import json
import datetime
import os

STRIPE_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/stripe_sync_log.jsonl'))
os.makedirs(os.path.dirname(STRIPE_LOG), exist_ok=True)

def sync_stripe(vault_id, metadata):
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'metadata': metadata,
        'status': 'synced'
    }
    with open(STRIPE_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry
