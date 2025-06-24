"""
SAFE AI Phase 9+ Key Management Backend
- Static, auditable, SAFE AI-compliant key management functions
- No dynamic or adaptive logic; all changes are logged
"""
import os
import json
import datetime

KEYS_FILE = "distribution/legal_exports/phase9_api_keys.json"
KEY_ROTATION_LOG = "distribution/legal_exports/phase9_api_key_rotation.log"

DEFAULT_KEYS = {
    "PHASE9SAFEKEY": "admin",
    "PHASE9VIEWER": "viewer",
    "PHASE9AUDITOR": "auditor",
    "PHASE9MAINTAINER": "maintainer",
    "PHASE9DISABLED": "disabled"
}

def load_keys():
    if not os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, "w") as f:
            json.dump(DEFAULT_KEYS, f)
    with open(KEYS_FILE, "r") as f:
        return json.load(f)

def save_keys(keys):
    with open(KEYS_FILE, "w") as f:
        json.dump(keys, f)

def log_key_action(action, key, role):
    with open(KEY_ROTATION_LOG, "a") as f:
        f.write(f"[{datetime.datetime.now().isoformat()}] {action}: {key} as {role}\n")

def add_key(key, role):
    keys = load_keys()
    keys[key] = role
    save_keys(keys)
    log_key_action("ADD_KEY", key, role)
    return True

def remove_key(key):
    keys = load_keys()
    if key in keys:
        role = keys[key]
        del keys[key]
        save_keys(keys)
        log_key_action("REMOVE_KEY", key, role)
        return True
    return False

def list_keys():
    return load_keys()
