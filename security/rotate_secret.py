import os
import sys
import json
import time
from datetime import datetime
from secrets import token_urlsafe
from vault_injector import store_secret, fetch_secret
from audit_logger import log_rotation_event
from reload_handler import hot_reload_config

ROTATION_KEYS = [
    'OPENAI_API_KEY', 'HUGGINGFACE_API_KEY', 'GUMROAD_API_KEY',
    'REDIS_TOKEN', 'INTERNAL_WEBHOOK_TOKEN'
]
ROTATION_ATTEMPTS = 3

# --- SECRET ROTATION LOGIC ---
def rotate_key(key):
    # Vendor API call or fallback to secure random
    if key == 'OPENAI_API_KEY':
        # TODO: requests.post() to OpenAI API for key rotation
        new_secret = token_urlsafe(64)
    else:
        new_secret = token_urlsafe(64)
    # Store in vault
    store_secret(key, new_secret)
    return new_secret

def verify_key_injected(key, secret):
    # Fetch from vault and compare
    return fetch_secret(key) == secret

def backup_env():
    ts = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    env_path = os.path.join(os.path.dirname(__file__), '../.env')
    bak_path = os.path.join(os.path.dirname(__file__), f'../.env.bak-{ts}')
    if os.path.exists(env_path):
        with open(env_path, 'r') as src, open(bak_path, 'w') as dst:
            dst.write(src.read())
    return bak_path

def rotate_all():
    results = []
    backup_env()
    for key in ROTATION_KEYS:
        attempt = 0
        success = False
        while attempt < ROTATION_ATTEMPTS and not success:
            try:
                new_secret = rotate_key(key)
                if verify_key_injected(key, new_secret):
                    log_rotation_event(key, 'SUCCESS')
                    success = True
                else:
                    attempt += 1
                    log_rotation_event(key, 'VERIFY_FAIL')
            except Exception as e:
                attempt += 1
                log_rotation_event(key, 'FAIL', error=str(e))
        if not success:
            # Fallback to last known good
            log_rotation_event(key, 'FALLBACK_LAST_KNOWN')
        results.append({'key': key, 'success': success})
    hot_reload_config()
    return results

if __name__ == '__main__':
    rotate_all()
