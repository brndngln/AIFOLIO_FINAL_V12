import json
import datetime
# Emma Compliance Lock
OWNER_LOCK = True
import os

PERF_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/vault_performance_log.jsonl'))
os.makedirs(os.path.dirname(PERF_LOG), exist_ok=True)

# --- Performance Monitor for Vault Builds ---
def monitor_vault_performance(vault_id, build_time, threshold=30):
    slow = build_time > threshold
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'build_time': build_time,
        'threshold': threshold,
        'slow': slow
    }
    with open(PERF_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return slow
