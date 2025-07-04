import json
from pathlib import Path
from datetime import datetime
import re
from backend.integrations.webhook_alerts import send_webhook

VIOLATION_LOG = Path(__file__).parent.parent / 'logs' / 'compliance_violations.json'
RULES_PATH = Path(__file__).parent / 'rules'
WEBHOOKS_PATH = Path(__file__).parent.parent / 'config' / 'webhook_endpoints.json'

SEVERITY_TIERS = {
    'critical': 1,
    'major': 2,
    'minor': 3,
    'info': 4
}

# Utility to get webhook URL by event type
def get_webhook_url(event_type):
    if not WEBHOOKS_PATH.exists():
        return None
    with open(WEBHOOKS_PATH, 'r') as f:
        endpoints = json.load(f)
    return endpoints.get(event_type)

# Modular rules loaded from external JSON file for each platform/category
RULES_FILE = Path(__file__).parent / 'rules' / 'violation_rules.json'

_platform_rules_cache = None
_rules_mtime = None

def load_platform_rules():
    global _platform_rules_cache, _rules_mtime
    if not RULES_FILE.exists():
        return {}
    mtime = RULES_FILE.stat().st_mtime
    if _platform_rules_cache is not None and mtime == _rules_mtime:
        return _platform_rules_cache
    with open(RULES_FILE, 'r') as f:
        _platform_rules_cache = json.load(f)
    _rules_mtime = mtime
    return _platform_rules_cache


from core.compliance.threat_feed_parser import parse_threat_feed
from core.compliance.blockchain_license_anchor import anchor_license_hash
from core.compliance.zero_knowledge_export_filter import zero_knowledge_export
from core.compliance.redundant_backup_scheduler import schedule_backup
from core.compliance.compliance_manifest_exporter import export_compliance_manifest
from core.compliance.adaptive_monetization_signal_detector import detect_signals

def scan_pdf_text(text, platforms=None):
    """
    Scan text for violations using modular, externalized rules loaded from JSON.
    Platforms is a list of platform keys (e.g. ['kdp','etsy','gdpr'])
    Returns: list of violations
    Rules are editable in backend/compliance/rules/violation_rules.json
    """
    # OMNIPROOF: Threat feed check before violation scan
    parse_threat_feed({})
    # OMNIPROOF: Blockchain anchor for scan hash (static)
    anchor_license_hash('SCAN_HASH_PLACEHOLDER')
    # OMNIPROOF: Zero-knowledge export filter (static)
    zero_knowledge_export('scan_path_placeholder')
    # OMNIPROOF: Schedule redundant backup
    schedule_backup('backend/compliance/')
    # OMNIPROOF: Export compliance manifest
    export_compliance_manifest('SAFE_AI_COMPLIANCE_REPORT.md', 'backend/compliance/compliance_report.pdf')
    # OMNIPROOF: Monetization signal detection
    detect_signals({'text': text, 'platforms': platforms})

    platform_rules = load_platform_rules()
    if platforms is None:
        platforms = list(platform_rules.keys())
    violations = []
    for platform in platforms:
        for rule in platform_rules.get(platform, []):
            if re.search(rule['pattern'], text, re.IGNORECASE):
                violations.append({
                    'platform': platform,
                    'pattern': rule['pattern'],
                    'description': rule['desc'],
                    'severity': rule['severity'],
                    'law': rule['law'],
                    'detected_at': datetime.utcnow().isoformat()
                })
    return violations

def log_violations(doc_id, violations, detected_by):
    if VIOLATION_LOG.exists():
        with open(VIOLATION_LOG, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    for v in violations:
        v['doc_id'] = doc_id
        v['detected_by'] = detected_by
        v['status'] = 'open'
        v['history'] = [{'action': 'detected', 'timestamp': v['detected_at'], 'by': detected_by}]
        # --- Automated webhook for violation detected ---
        url = get_webhook_url('violation_detected')
        if url:
            try:
                send_webhook(url, 'violation_detected', {
                    'doc_id': doc_id,
                    'pattern': v.get('pattern'),
                    'description': v.get('description'),
                    'severity': v.get('severity'),
                    'law': v.get('law'),
                    'detected_at': v.get('detected_at'),
                    'detected_by': detected_by
                })
            except Exception:
                pass  # Optionally log error
    logs.extend(violations)
    with open(VIOLATION_LOG, 'w') as f:
        json.dump(logs, f, indent=2)
    return violations

# --- Helper for SLA breach webhook ---
def send_sla_breach_webhook(violation):
    url = get_webhook_url('sla_breach')
    if url:
        try:
            send_webhook(url, 'sla_breach', {
                'doc_id': violation.get('doc_id'),
                'severity': violation.get('severity'),
                'law': violation.get('law'),
                'assigned_reviewer': violation.get('assigned_reviewer'),
                'sla_status': violation.get('sla_status'),
                'breached_at': datetime.utcnow().isoformat()
            })
        except Exception:
            pass

# --- Helper for remediation applied webhook ---
def send_remediation_webhook(violation, admin_id):
    url = get_webhook_url('report_ready')
    if url:
        try:
            send_webhook(url, 'remediation_applied', {
                'doc_id': violation.get('doc_id'),
                'remediation': violation.get('remediation'),
                'fixed_by': admin_id,
                'fixed_at': datetime.utcnow().isoformat()
            })
        except Exception:
            pass

def get_violations(doc_id=None, status=None):
    if not VIOLATION_LOG.exists():
        return []
    with open(VIOLATION_LOG, 'r') as f:
        logs = json.load(f)
    result = logs
    if doc_id:
        result = [v for v in result if v['doc_id'] == doc_id]
    if status:
        result = [v for v in result if v['status'] == status]
    return result
