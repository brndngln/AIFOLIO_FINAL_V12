import re
import json
import datetime
import os

LIMITER_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/vocab_scope_limiter_log.jsonl'))
os.makedirs(os.path.dirname(LIMITER_LOG), exist_ok=True)

# Example: block undesired topics/words
BLOCKED_PATTERNS = [r'(?i)crypto', r'(?i)gambling', r'(?i)adult', r'(?i)politics', r'(?i)violence']

def check_vocabulary_scope(text):
    blocked = [pat for pat in BLOCKED_PATTERNS if re.search(pat, text)]
    safe = not blocked
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'text': text,
        'blocked_patterns': blocked,
        'safe': safe
    }
    with open(LIMITER_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return safe, blocked

if __name__ == "__main__":
    print(check_vocabulary_scope('This is about crypto and gambling.'))
