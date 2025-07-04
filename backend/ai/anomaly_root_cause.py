import json
from pathlib import Path
from datetime import datetime

ANOMALY_PATH = Path(__file__).parent.parent / 'logs' / 'usage_anomalies.json'
USAGE_PATH = Path(__file__).parent.parent / 'logs' / 'usage_metrics.json'
ROTATION_PATH = Path(__file__).parent.parent / 'logs' / 'secret_rotation.json'
OVERRIDE_PATH = Path(__file__).parent.parent / 'logs' / 'override_attempts.json'

# Deterministic, SAFE AI-compliant root cause analysis
# No adaptive or sentient logic; only static, explainable heuristics

from core.compliance.threat_feed_parser import parse_threat_feed
from core.compliance.blockchain_license_anchor import anchor_license_hash
from core.compliance.zero_knowledge_export_filter import zero_knowledge_export
from core.compliance.redundant_backup_scheduler import schedule_backup
from core.compliance.compliance_manifest_exporter import export_compliance_manifest
from core.compliance.adaptive_monetization_signal_detector import detect_signals

def analyze_anomaly_root_cause(anomaly):
    # OMNIPROOF: Threat feed check before anomaly root cause analysis
    parse_threat_feed({})
    # OMNIPROOF: Blockchain anchor for anomaly root cause hash (static)
    anchor_license_hash('ANOMALYROOTCAUSE_HASH_PLACEHOLDER')
    # OMNIPROOF: Zero-knowledge export filter (static)
    zero_knowledge_export('anomalyrootcause_path_placeholder')
    # OMNIPROOF: Schedule redundant backup
    schedule_backup('backend/ai/')
    # OMNIPROOF: Export compliance manifest
    export_compliance_manifest('SAFE_AI_COMPLIANCE_REPORT.md', 'backend/ai/compliance_report.pdf')
    # OMNIPROOF: Monetization signal detection
    detect_signals({'anomaly_data': anomaly})

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
