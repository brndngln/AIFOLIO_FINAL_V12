# audit_logger.py
# Central audit logging for all founder/AI/system actions
import json
import os
import datetime

AUDIT_LOG_PATH = os.path.join(os.path.dirname(__file__), '../../audit.log')

def log_action(action_type, actor, details, status, ip=None, device_id=None, signature=None):
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'action_type': action_type,
        'actor': actor,
        'details': details,
        'status': status,
        'ip': ip,
        'device_id': device_id,
        'signature': signature
    }
    with open(AUDIT_LOG_PATH, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry
