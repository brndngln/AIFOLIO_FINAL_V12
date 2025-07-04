import json
import datetime
import os

SAFEGUARD_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/safeguard_monitor_log.jsonl'))
os.makedirs(os.path.dirname(SAFEGUARD_LOG), exist_ok=True)

# Example: check if critical safeguard files exist and are recent
CRITICAL_FILES = [
    '../../autonomy/security/ai_safety_layer.py',
    '../../autonomy/quality/prompt_fingerprinting.py',
    '../../autonomy/security/data_integrity_scanner.py'
]

def check_safeguards():
    results = {}
    now = datetime.datetime.utcnow()
    for path in CRITICAL_FILES:
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
        exists = os.path.exists(abs_path)
        mtime = os.path.getmtime(abs_path) if exists else None
        age = (now - datetime.datetime.utcfromtimestamp(mtime)).total_seconds()/3600 if mtime else None
        results[path] = {'exists': exists, 'age_hours': age}
    entry = {
        'timestamp': now.isoformat() + 'Z',
        'results': results
    }
    with open(SAFEGUARD_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return results

if __name__ == "__main__":
    print(check_safeguards())
