import os
import json
from pathlib import Path

def load_audit_logs(log_dir='./ai_core/EmmaLogs/'):
    logs = []
    for fname in Path(log_dir).glob('*.log.enc'):
        logs.append(fname.name)
    return logs

def load_intrusion_alerts(alert_file='./ai_core/EmmaLogs/intrusion_alerts.log'):
    if not os.path.exists(alert_file):
        return []
    with open(alert_file, 'r') as f:
        return f.readlines()

def load_vault_index(index_file='ai_core/EmmaLogs/EmmaVaultIndex.json'):
    if not os.path.exists(index_file):
        return {}
    with open(index_file, 'r') as f:
        return json.load(f)

def dashboard_status():
    return {
        'audit_logs': load_audit_logs(),
        'intrusion_alerts': load_intrusion_alerts(),
        'vault_index': load_vault_index(),
    }

if __name__ == '__main__':
    import pprint
    pprint.pprint(dashboard_status())
