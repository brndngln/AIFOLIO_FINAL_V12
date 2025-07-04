import json
from pathlib import Path
from datetime import datetime, timedelta

VIOLATION_LOG = Path(__file__).parent.parent / 'logs' / 'compliance_violations.json'
SLA_AUDIT_LOG = Path(__file__).parent.parent / 'logs' / 'sla_audit_log.json'

SLA_WINDOWS = {
    'critical': 24,  # hours
    'major': 72,     # hours
    'minor': 168,    # hours
    'info': 720      # hours
}

COLOR_CODES = {
    'ok': 'green',
    'warning': 'orange',
    'danger': 'red',
    'escalated': 'purple'
}

def update_sla_status():
    if not VIOLATION_LOG.exists():
        return []
    with open(VIOLATION_LOG, 'r') as f:
        violations = json.load(f)
    now = datetime.utcnow()
    updated = False
    for v in violations:
        detected = datetime.fromisoformat(v['detected_at'])
        window = SLA_WINDOWS.get(v['severity'], 72)
        due = detected + timedelta(hours=window)
        v['sla_due'] = due.isoformat()
        overdue = now > due
        if v.get('status') == 'resolved':
            v['sla_status'] = 'ok'
            v['sla_color'] = COLOR_CODES['ok']
        elif overdue and not v.get('escalated', False):
            v['sla_status'] = 'escalated'
            v['sla_color'] = COLOR_CODES['escalated']
            v['escalated'] = True
            v.setdefault('sla_history', []).append({'event': 'escalated', 'timestamp': now.isoformat()})
            log_sla_audit(v, 'escalated')
            updated = True
        elif overdue:
            v['sla_status'] = 'danger'
            v['sla_color'] = COLOR_CODES['danger']
        else:
            hours_left = (due - now).total_seconds() / 3600
            if hours_left < 6:
                v['sla_status'] = 'warning'
                v['sla_color'] = COLOR_CODES['warning']
            else:
                v['sla_status'] = 'ok'
                v['sla_color'] = COLOR_CODES['ok']
    if updated:
        with open(VIOLATION_LOG, 'w') as f:
            json.dump(violations, f, indent=2)
    return violations

def log_sla_audit(violation, event):
    log_entry = {
        'doc_id': violation['doc_id'],
        'violation': violation['description'],
        'severity': violation['severity'],
        'event': event,
        'timestamp': datetime.utcnow().isoformat(),
        'status': violation.get('sla_status'),
        'escalated': violation.get('escalated', False)
    }
    if SLA_AUDIT_LOG.exists():
        with open(SLA_AUDIT_LOG, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(log_entry)
    with open(SLA_AUDIT_LOG, 'w') as f:
        json.dump(logs, f, indent=2)
