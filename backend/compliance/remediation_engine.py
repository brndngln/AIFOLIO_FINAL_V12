import json
from pathlib import Path
from datetime import datetime

VIOLATION_LOG = Path(__file__).parent.parent / 'logs' / 'compliance_violations.json'
REMEDIATION_LOG = Path(__file__).parent.parent / 'logs' / 'remediation_log.json'

REMEDIATION_LIBRARY = {
    'FDA': 'Add substantiation or disclaimer for FDA claims.',
    'FTC': 'Add required legal disclaimers.',
    'Copyright': 'Verify asset ownership or remove copyrighted content.',
    'GDPR': 'Ensure GDPR-compliant data handling and privacy notices.',
    'HIPAA': 'Remove or anonymize PHI, add HIPAA notice.',
    'Gumroad': 'Add a clear refund policy.',
    'Amazon': 'Remove unsubstantiated claims.',
    'Other': 'Consult compliance officer.'
}

def suggest_remediation(violation):
    law = violation.get('law', 'Other')
    context = violation.get('description', '')
    base = REMEDIATION_LIBRARY.get(law, REMEDIATION_LIBRARY['Other'])
    return f"{base} Context: {context}"

def apply_remediation(idx, admin_id):
    if not VIOLATION_LOG.exists():
        return {'success': False, 'error': 'No violations'}
    with open(VIOLATION_LOG, 'r') as f:
        violations = json.load(f)
    if idx is None or idx >= len(violations):
        return {'success': False, 'error': 'Invalid index'}
    v = violations[idx]
    if v.get('status') == 'resolved':
        return {'success': False, 'error': 'Already resolved'}
    fix = suggest_remediation(v)
    v['remediation'] = fix
    v['status'] = 'resolved'
    v.setdefault('fix_history', []).append({'fix': fix, 'by': admin_id, 'timestamp': datetime.utcnow().isoformat()})
    with open(VIOLATION_LOG, 'w') as f:
        json.dump(violations, f, indent=2)
    # Log remediation
    log_entry = {
        'violation_idx': idx,
        'admin_id': admin_id,
        'fix': fix,
        'timestamp': datetime.utcnow().isoformat()
    }
    if REMEDIATION_LOG.exists():
        with open(REMEDIATION_LOG, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(log_entry)
    with open(REMEDIATION_LOG, 'w') as f:
        json.dump(logs, f, indent=2)
    return {'success': True, 'fix': fix, 'violation': v}

def rollback_remediation(idx):
    if not VIOLATION_LOG.exists():
        return {'success': False, 'error': 'No violations'}
    with open(VIOLATION_LOG, 'r') as f:
        violations = json.load(f)
    if idx is None or idx >= len(violations):
        return {'success': False, 'error': 'Invalid index'}
    v = violations[idx]
    if not v.get('fix_history'):
        return {'success': False, 'error': 'No fix history'}
    v['status'] = 'open'
    v['remediation'] = None
    v['fix_history'].append({'rollback': True, 'timestamp': datetime.utcnow().isoformat()})
    with open(VIOLATION_LOG, 'w') as f:
        json.dump(violations, f, indent=2)
    return {'success': True, 'violation': v}
