import json
import datetime
import os

XBRL_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/xbrl_export_log.jsonl'))
os.makedirs(os.path.dirname(XBRL_LOG), exist_ok=True)

def export_xbrl(vault_id, data):
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'data': data,
        'status': 'exported'
    }
    with open(XBRL_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry
