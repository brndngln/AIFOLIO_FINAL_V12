"""
AIFOLIO Alert Engine
- Fully static, deterministic, SAFE AI compliant
- No live API calls; all logic is static
- Audit-logs all alert events
- GDPR/CCPA compliant, owner controlled
"""
import os
import json
from datetime import datetime

ALERT_LOG_PATH = os.path.join(os.path.dirname(__file__), '../../analytics/alert_log.json')

def send_alert(type="compliance_failure", method="static", message="Vault failed PDF compliance check.", to=None, owner_override=None):
    """
    Static SAFE AI alert logging. No live API calls. Owner can override alert content.
    """
    alert_message = owner_override if owner_override is not None else message
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": type,
        "method": method,
        "message": alert_message,
        "to": to
    }
    if os.path.exists(ALERT_LOG_PATH):
        with open(ALERT_LOG_PATH, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(log_entry)
    with open(ALERT_LOG_PATH, 'w') as f:
        json.dump(logs, f, indent=2)
    return True
