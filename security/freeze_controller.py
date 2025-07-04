import redis
import os
from datetime import datetime
import json

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
r = redis.from_url(REDIS_URL)
FREEZE_KEY = 'aifolio:rotations_enabled'
LOG_PATH = os.path.join(os.path.dirname(__file__), '../logs/override_attempts.json')

# Set freeze flag (True = enabled, False = frozen)
def set_rotation_enabled(enabled: bool, admin_id=None):
    r.set(FREEZE_KEY, json.dumps({'enabled': enabled, 'timestamp': datetime.utcnow().isoformat(), 'admin_id': admin_id}))

def get_rotation_enabled():
    val = r.get(FREEZE_KEY)
    if not val:
        return True
    try:
        data = json.loads(val)
        return data.get('enabled', True)
    except Exception:
        return True

def log_override_attempt(event):
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(event)
        with open(LOG_PATH, 'w') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f'[FreezeController] Failed to log override: {e}')
