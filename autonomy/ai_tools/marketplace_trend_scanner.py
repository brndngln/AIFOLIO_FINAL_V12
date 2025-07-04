import json
import datetime
import os
import requests

TREND_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/marketplace_trend_scanner_log.jsonl'))
os.makedirs(os.path.dirname(TREND_LOG), exist_ok=True)

# --- Marketplace Trend Scanner (SAFE AI, Read-Only) ---
def scan_gumroad_trends(api_url='https://api.gumroad.com/v2/products'):
    try:
        resp = requests.get(api_url)
        data = resp.json()
        # Example: Count most common tags/titles
        tag_counts = {}
        for p in data.get('products', []):
            tags = p.get('tags', [])
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        status = 'ok'
    except Exception as e:
        top_tags = []
        status = f'error: {e}'
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'top_tags': top_tags,
        'status': status
    }
    with open(TREND_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return top_tags, status
