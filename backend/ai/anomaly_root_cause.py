import json
from pathlib import Path
from datetime import datetime, timedelta

ANOMALY_PATH = Path(__file__).parent.parent / 'logs' / 'usage_anomalies.json'
USAGE_PATH = Path(__file__).parent.parent / 'logs' / 'usage_metrics.json'
ROTATION_PATH = Path(__file__).parent.parent / 'logs' / 'secret_rotation.json'
OVERRIDE_PATH = Path(__file__).parent.parent / 'logs' / 'override_attempts.json'

# Deterministic, SAFE AI-compliant root cause analysis
# No adaptive or sentient logic; only static, explainable heuristics

def analyze_anomaly(anomaly):
    key = anomaly.get('key')
    timestamp = anomaly.get('timestamp')
    # Find related usage pattern
    with open(USAGE_PATH, 'r') as f:
        usage = json.load(f)
    window = [d for d in usage.get(key, {}) if abs((datetime.fromisoformat(d) - datetime.fromisoformat(timestamp[:10])).days) <= 3]
    pattern = {d: usage[key][d] for d in window}
    # Check for recent manual overrides
    with open(OVERRIDE_PATH, 'r') as f:
        overrides = json.load(f)
    recent_override = any(o for o in overrides if o.get('key') == key and o.get('timestamp', '')[:10] in window)
    # Check for recent secret rotations
    with open(ROTATION_PATH, 'r') as f:
        rotations = json.load(f)
    recent_rotation = any(r for r in rotations if r.get('key') == key and r.get('timestamp', '')[:10] in window)
    # Static rules for root cause
    if recent_override:
        cause = 'Manual override likely triggered spike.'
    elif recent_rotation:
        cause = 'Recent secret rotation may have affected usage.'
    elif max(pattern.values(), default=0) > 2 * (sum(pattern.values())/max(1,len(pattern))):
        cause = 'Sudden usage surge without admin intervention.'
    else:
        cause = 'No clear root cause detected.'
    return {
        'anomaly': anomaly,
        'pattern': pattern,
        'recent_override': recent_override,
        'recent_rotation': recent_rotation,
        'root_cause': cause
    }

def analyze_all():
    with open(ANOMALY_PATH, 'r') as f:
        anomalies = json.load(f)
    return [analyze_anomaly(a) for a in anomalies]
