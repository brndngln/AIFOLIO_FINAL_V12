import json
import datetime
import os

TIMESTAMP_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/audit_timestamp_log.jsonl'))
os.makedirs(os.path.dirname(TIMESTAMP_LOG), exist_ok=True)

def inject_audit_timestamp(output):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    stamped = f"{output}\n<!-- AUDIT_TIMESTAMP: {now} -->"
    entry = {
        'timestamp': now,
        'output': output,
        'stamped': stamped
    }
    with open(TIMESTAMP_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return stamped

if __name__ == "__main__":
    print(inject_audit_timestamp('Your PDF vault is ready!'))
