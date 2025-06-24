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

# --- Key Metadata Management ---
META_FILE = "distribution/legal_exports/phase9_api_key_meta.json"

def load_key_meta():
    if not os.path.exists(META_FILE):
        with open(META_FILE, "w") as f:
            json.dump({}, f)
    with open(META_FILE, "r") as f:
        return json.load(f)

def save_key_meta(meta):
    with open(META_FILE, "w") as f:
        json.dump(meta, f)

def get_key_meta():
    return load_key_meta()

def set_key_meta(key, meta_update):
    meta = load_key_meta()
    m = meta.get(key, {})
    m.update(meta_update)
    meta[key] = m
    save_key_meta(meta)
    log_key_action("UPDATE_META", key, str(meta_update))
    return True

def increment_key_usage(key):
    meta = load_key_meta()
    m = meta.get(key, {})
    m['usage'] = m.get('usage', 0) + 1
    m['last_used'] = datetime.datetime.now().isoformat()
    meta[key] = m
    save_key_meta(meta)
    return True

def rotate_key(key):
    meta = load_key_meta()
    m = meta.get(key, {})
    m['rotated'] = True
    meta[key] = m
    save_key_meta(meta)
    log_key_action("ROTATE_KEY", key, str(m))
    return True

def bulk_import_keys(key_role_list):
    keys = load_keys()
    for item in key_role_list:
        k, r = item.get('key'), item.get('role', 'viewer')
        if k:
            keys[k] = r
            log_key_action("BULK_IMPORT", k, r)
    save_keys(keys)
    return True

def bulk_export_keys():
    return load_keys()
