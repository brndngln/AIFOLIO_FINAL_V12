import json
import datetime
import os

DUPLICATE_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/duplicate_content_scanner_log.jsonl'))
os.makedirs(os.path.dirname(DUPLICATE_LOG), exist_ok=True)

# --- AI Duplicate Content Scanner ---
def scan_for_duplicates(content_list):
    seen = {}
    duplicates = []
    for idx, content in enumerate(content_list):
        if content in seen:
            duplicates.append({'index': idx, 'original_index': seen[content]})
        else:
            seen[content] = idx
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'duplicates': duplicates
    }
    with open(DUPLICATE_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return duplicates
