import hashlib
import datetime
import json
import os

FINGERPRINT_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/ai_prompt_fingerprint_log.jsonl'))
os.makedirs(os.path.dirname(FINGERPRINT_LOG), exist_ok=True)

def fingerprint_prompt(prompt):
    return hashlib.sha256(prompt.encode('utf-8')).hexdigest()

def log_fingerprint(prompt, user='admin'):
    fp = fingerprint_prompt(prompt)
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'prompt': prompt,
        'fingerprint': fp,
        'user': user
    }
    with open(FINGERPRINT_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return fp

if __name__ == "__main__":
    prompt = "Write a professional summary for AIFOLIO."
    print(fingerprint_prompt(prompt))
    print(log_fingerprint(prompt))
