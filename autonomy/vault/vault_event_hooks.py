import json
import datetime
import os

EVENT_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/vault_event_hooks_log.jsonl'))
os.makedirs(os.path.dirname(EVENT_LOG), exist_ok=True)

# --- Vault Event Hooks ---
def log_event(event_type, vault_id, user_id=None, metadata=None):
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'vault_id': vault_id,
        'user_id': user_id,
        'metadata': metadata or {}
    }
    with open(EVENT_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry

def refund_issued(vault_id, user_id, metadata=None):
    return log_event('refund_issued', vault_id, user_id, metadata)

def download_clicked(vault_id, user_id, metadata=None):
    return log_event('download_clicked', vault_id, user_id, metadata)

def upsell_clicked(vault_id, user_id, metadata=None):
    return log_event('upsell_clicked', vault_id, user_id, metadata)

def vault_retired(vault_id, user_id, metadata=None):
    return log_event('vault_retired', vault_id, user_id, metadata)

def vault_duplicate_detected(vault_id, user_id=None, metadata=None):
    return log_event('vault_duplicate_detected', vault_id, user_id, metadata)

def vault_rebuild_triggered(vault_id, user_id, metadata=None):
    return log_event('vault_rebuild_triggered', vault_id, user_id, metadata)
