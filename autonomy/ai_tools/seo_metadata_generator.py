import json
import datetime
import os

SEO_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/seo_metadata_generator_log.jsonl'))
os.makedirs(os.path.dirname(SEO_LOG), exist_ok=True)

# --- AI Static SEO Metadata Generator ---
def generate_seo_metadata(title, description, keywords=None):
    meta = {
        'title': title.strip().capitalize(),
        'description': description.strip()[:160],
        'keywords': keywords or []
    }
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'input': {'title': title, 'description': description, 'keywords': keywords},
        'output': meta
    }
    with open(SEO_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return meta
