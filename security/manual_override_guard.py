import os
<<<<<<< HEAD
import json
=======
>>>>>>> omni_repair_backup_20250704_1335
from datetime import datetime
from mfa_verifier import verify_mfa_token
from freeze_controller import log_override_attempt

LOG_PATH = os.path.join(os.path.dirname(__file__), '../logs/override_attempts.json')

# Attempts per admin (in-memory for demo, use Redis for prod)
_attempts = {}

# Call this before allowing manual rotation
def check_manual_override(admin_id, token, ip):
    global _attempts
    now = datetime.utcnow().isoformat()
    status = 'FAIL'
    lockout = False
    if not verify_mfa_token(admin_id, token):
        _attempts.setdefault(admin_id, []).append(now)
        # Only keep last 10 attempts
        _attempts[admin_id] = _attempts[admin_id][-10:]
        # Lockout if >3 fails in last 15min
        recent = [t for t in _attempts[admin_id] if (datetime.fromisoformat(now) - datetime.fromisoformat(t)).total_seconds() < 900]
        if len(recent) > 3:
            lockout = True
        log = {
            'admin_id': admin_id,
            'timestamp': now,
            'ip': ip,
            'mfa_status': 'FAIL',
            'lockout': lockout
        }
        log_override_attempt(log)
        return False, lockout
    # Success
    _attempts[admin_id] = []
    log = {
        'admin_id': admin_id,
        'timestamp': now,
        'ip': ip,
        'mfa_status': 'SUCCESS',
        'lockout': False
    }
    log_override_attempt(log)
    return True, False
