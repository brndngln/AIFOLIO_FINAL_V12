import json
import datetime
import os

ADAPTIVE_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/adaptive_api_retry_tuner_log.jsonl'))
os.makedirs(os.path.dirname(ADAPTIVE_LOG), exist_ok=True)

# --- Adaptive API Retry Tuner (Safe, Non-Sentient) ---
def get_retry_intervals(error_history):
    # error_history: list of {'timestamp', 'error'}
    base = [60, 300, 900]
    if not error_history:
        return base
    recent_errors = [e for e in error_history if (datetime.datetime.utcnow() - datetime.datetime.fromisoformat(e['timestamp'].replace('Z',''))).total_seconds() < 3600]
    n = len(recent_errors)
    # If many recent errors, increase backoff
    if n >= 5:
        intervals = [min(b*2, 3600) for b in base]
    elif n >= 2:
        intervals = [int(b*1.5) for b in base]
    else:
        intervals = base
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'recent_errors': n,
        'intervals': intervals
    }
    with open(ADAPTIVE_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return intervals
