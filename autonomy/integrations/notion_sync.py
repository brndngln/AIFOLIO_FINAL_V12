import json
import datetime
import os

NOTION_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/notion_sync_log.jsonl'))
os.makedirs(os.path.dirname(NOTION_LOG), exist_ok=True)

def sync_notion(vault_id, metadata):
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'metadata': metadata,
        'status': 'synced'
    }
    with open(NOTION_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry
