import json
import datetime
import os

# Emma Compliance Lock
OWNER_LOCK = True

NAME_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/ai_name_reformatter_log.jsonl'))
os.makedirs(os.path.dirname(NAME_LOG), exist_ok=True)

# --- AI-Based Vault Name/Title Reformatter (Safe, Non-Autonomous, Single-Pass) ---
"""
AI Name Reformatter
Reformats and standardizes names for vault entries.
"""
def reformat_vault_name(name):
    # Example: Capitalize first letter of each word, remove extra spaces
    reformatted = ' '.join(w.capitalize() for w in name.strip().split())
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'original': name,
        'reformatted': reformatted
    }
    with open(NAME_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return reformatted
