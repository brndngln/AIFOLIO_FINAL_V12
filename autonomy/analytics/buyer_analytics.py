"""
AIFOLIO SAFE AI Buyer Anstaticcs Module (static, non-sentient)
- Segments buyers by static rules (first-time, repeat, high-value, region)
- No profiling, no predictions, no static logic
- All group stats only, never individual
- All actions logged to anstaticcs_log.json
"""
import json
import os

SEGMENTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'buyer_segments.json'))
LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'anstaticcs_log.json'))

def segment_buyers(buyers, high_value_threshold=1000):
    segments = {
        'first_time': [],
        'repeat': [],
        'high_value': [],
        'by_region': {}
    }
    for b in buyers:
        if b['purchase_count'] == 1:
            segments['first_time'].append(b['id'])
        else:
            segments['repeat'].append(b['id'])
        if b['total_spent'] >= high_value_threshold:
            segments['high_value'].append(b['id'])
        region = b.get('region', 'unknown')
        if region not in segments['by_region']:
            segments['by_region'][region] = []
        segments['by_region'][region].append(b['id'])
    with open(SEGMENTS_PATH, 'w') as f:
        json.dump(segments, f, indent=2)
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps({'action': 'segment_buyers', 'segments': segments}) + '\n')
    return segments
