import json
import datetime
import os
import re

DESC_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/vault_description_optimizer_log.jsonl'))
os.makedirs(os.path.dirname(DESC_LOG), exist_ok=True)

# --- AI-Driven Vault Description Optimizer (Static, Non-Autonomous) ---
def optimize_description(description):
    # Example: Remove double spaces, capitalize first letter, ensure period at end
    orig = description
    desc = re.sub(r' +', ' ', description.strip())
    if desc and not desc[0].isupper():
        desc = desc[0].upper() + desc[1:]
    if desc and not desc.endswith('.'):
        desc += '.'
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'original': orig,
        'optimized': desc
    }
    with open(DESC_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return desc
