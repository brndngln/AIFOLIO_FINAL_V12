import json
import datetime
import os

LIFECYCLE_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), 'vault_lifecycle_analytics_log.jsonl'))
os.makedirs(os.path.dirname(LIFECYCLE_LOG), exist_ok=True)

# --- Vault Lifecycle Analytics ---
import logging
logger = logging.getLogger(__name__)

def log_vault_lifecycle_event(event_type: str, vault_id: str, details: dict) -> None:
    """Audit log vault lifecycle event (static, SAFE AI-compliant). Extension: real analytics pipeline."""
    event = {
        'event_type': event_type,
        'vault_id': vault_id,
        'details': details,
        'timestamp': datetime.datetime.now().isoformat()
    }
    logger.info(f"Vault lifecycle event: {event}")
    # Static: append to local log file for audit trail
    with open(LIFECYCLE_LOG, 'a') as f:
        f.write(json.dumps(event) + '\n')

def get_static_lifecycle_summary() -> dict:
    """Return static, deterministic lifecycle analytics summary. Extension: real analytics pipeline."""
    logger.info("Returning static vault lifecycle analytics summary.")
    return {
        'total_vaults_created': 42,
        'total_vaults_archived': 5,
        'average_lifetime_days': 120,
        'most_active_vault': 'vault_001',
        'last_event_time': datetime.datetime.now().isoformat()
    }

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
