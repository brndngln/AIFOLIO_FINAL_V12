import hashlib
import json
import datetime
import os

SIGNATURE_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/hook_signature_log.jsonl'))
os.makedirs(os.path.dirname(SIGNATURE_LOG), exist_ok=True)

def fingerprint_hook_payload(payload):
    payload_json = json.dumps(payload, sort_keys=True)
    sig = hashlib.sha256(payload_json.encode('utf-8')).hexdigest()
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'payload': payload,
        'signature': sig
    }
    with open(SIGNATURE_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return sig

if __name__ == "__main__":
    print(fingerprint_hook_payload({'order_id': '123', 'amount': 49}))
