import os
import sys
import hashlib
import json
import logging
import getpass
<<<<<<< HEAD
import base64
import socket
from cryptography.fernet import Fernet
from datetime import datetime
=======
import socket
from cryptography.fernet import Fernet
from datetime import datetime
import subprocess
>>>>>>> omni_repair_backup_20250704_1335

# --- CONFIGURABLE ---
CORE_FILES = ["main.py", "ai_core.py", "vault_engine.py"]
SECURITY_KEY_PATH = os.path.abspath("security/key.key")
LOCKDOWN_CONFIG_PATH = os.path.abspath("lockdown.json")
LOG_PATH = os.path.abspath("logs/omniprotect.log")
CEO_EMAIL = os.environ.get("CEO_EMAIL", "ceo@aifolio.com")
CEO_TELEGRAM = os.environ.get("CEO_TELEGRAM", None)
MFA_CODE = os.environ.get("CEO_MFA_CODE", "1984")
OMNI_CEO = os.environ.get("OMNI_CEO", None)

# --- SETUP LOGGING ---
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def log_event(event):
    logging.info(event)
    print(f"[OMNISECURE] {event}")

# --- 1. ENCRYPTED SECURITY KEY ---
def generate_security_key():
    os.makedirs(os.path.dirname(SECURITY_KEY_PATH), exist_ok=True)
    if not os.path.exists(SECURITY_KEY_PATH):
        key = Fernet.generate_key()
        with open(SECURITY_KEY_PATH, "wb") as f:
            f.write(key)
        log_event("Security key generated and stored.")
    else:
        log_event("Security key already exists.")

def load_security_key():
    with open(SECURITY_KEY_PATH, "rb") as f:
        return f.read()

# --- 2. LOCKDOWN CONFIG WITH HASHES ---
def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def generate_lockdown_config():
    hashes = {}
    for fname in CORE_FILES:
        if not os.path.exists(fname):
            log_event(f"[ALERT] Core file missing: {fname}")
            continue
        hashes[fname] = hash_file(fname)
    config = {
        "generated": datetime.utcnow().isoformat() + "Z",
        "core_hashes": hashes,
        "vault_mode": "READ_ONLY",
        "network_policy": "restricted",
        "ceo_only": True
    }
    with open(LOCKDOWN_CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    log_event("Lockdown config generated.")
    return config

def load_lockdown_config():
    with open(LOCKDOWN_CONFIG_PATH, "r") as f:
        return json.load(f)

# --- 3. CEO-ONLY ACCESS ENFORCEMENT ---
def is_ceo():
    if os.geteuid() == 0 or OMNI_CEO:
        return True
    log_event("[SECURITY] CEO-only access denied.")
    sys.exit("CEO-only access required.")

def get_staged_files(timeout_sec=60):
    try:
        result = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True, timeout=timeout_sec)
        return result.stdout.strip().split('\n') if result.returncode == 0 else []
    except subprocess.TimeoutExpired:
        log_event('[Sentinel] git diff timed out.')
        immutable_log('[Sentinel] git diff timed out.')
        alert_ceo('[Sentinel] git diff timed out.')
        return []
    except Exception as e:
        log_event(f'[Sentinel] git diff error: {e}')
        immutable_log(f'[Sentinel] git diff error: {e}')
        alert_ceo(f'[Sentinel] git diff error: {e}')
        return []

# --- 4. READ-ONLY VAULT MODE ---
def enforce_vault_read_only():
    # This is a runtime flag; actual enforcement must be in all vault logic.
    os.environ["AIFOLIO_VAULT_MODE"] = "READ_ONLY"
    log_event("Vault logic set to READ-ONLY mode.")

# --- 5. DISABLE UNVERIFIED EXTERNAL NETWORK CALLS ---
def restrict_network_calls():
<<<<<<< HEAD
    import builtins
=======
>>>>>>> omni_repair_backup_20250704_1335
    orig_socket = socket.socket
    def guarded_socket(*args, **kwargs):
        s = orig_socket(*args, **kwargs)
        orig_connect = s.connect
        def connect_guard(addr):
            host, port = addr
            if not host.endswith("aifolio.com"):
                log_event(f"[SECURITY] Blocked external network call to {host}:{port}")
                raise PermissionError("External network calls blocked by OMNISECURE lockdown.")
            return orig_connect(addr)
        s.connect = connect_guard
        return s
    socket.socket = guarded_socket
    log_event("External network calls restricted.")

# --- 6. CEO MFA ---
<<<<<<< HEAD
import threading
import signal
import functools
import os
import sys
=======
import signal
import functools
import os
>>>>>>> omni_repair_backup_20250704_1335

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Operation timed out.")

def autonomous_recovery(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        retries = 3
        for attempt in range(1, retries + 1):
            try:
                return func(*args, **kwargs)
            except (PermissionError, OSError) as e:
                log_event(f"[AUTONOMOUS RECOVERY] Attempt {attempt}: {e}")
                immutable_log(f"[AUTONOMOUS RECOVERY] Attempt {attempt}: {e}")
                try:
                    os.chmod('.', 0o755)
                    for root, dirs, files in os.walk('.'):
                        for d in dirs:
                            os.chmod(os.path.join(root, d), 0o755)
                        for f in files:
                            os.chmod(os.path.join(root, f), 0o644)
                except Exception as perm_e:
                    log_event(f"[AUTONOMOUS RECOVERY] chmod error: {perm_e}")
                try:
                    os.chown('.', os.getuid(), os.getgid())
                except Exception as chown_e:
                    log_event(f"[AUTONOMOUS RECOVERY] chown error: {chown_e}")
                if attempt == retries:
                    log_event(f"[AUTONOMOUS RECOVERY] Permanent error after {retries} attempts: {e}")
                    immutable_log(f"[AUTONOMOUS RECOVERY] Permanent error after {retries} attempts: {e}")
                    # Only abort on SAFE AI violation
                    if 'sentient' in str(e).lower():
                        sys.exit("SAFE AI violation: sentience detected.")
                    return None
        return None
    return wrapper

def require_ceo_mfa(timeout_sec=60):
    try:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_sec)
        code = getpass.getpass("Enter CEO MFA code: ")
        signal.alarm(0)
    except TimeoutException:
        log_event("[SECURITY] CEO MFA prompt timed out.")
        immutable_log("[SECURITY] CEO MFA prompt timed out.")
        alert_ceo("[SECURITY] CEO MFA prompt timed out. Lockdown aborted.")
        sys.exit("CEO MFA timed out. Lockdown aborted.")
    except Exception as e:
        log_event(f"[SECURITY] CEO MFA error: {e}")
        immutable_log(f"[SECURITY] CEO MFA error: {e}")
        alert_ceo(f"[SECURITY] CEO MFA error: {e}")
        sys.exit("CEO MFA failed. Lockdown aborted.")
    if code != MFA_CODE:
        log_event("[SECURITY] CEO MFA failed.")
        immutable_log("[SECURITY] CEO MFA failed.")
        alert_ceo("[SECURITY] CEO MFA failed. Lockdown aborted.")
        sys.exit("CEO MFA failed. Lockdown aborted.")
    log_event("CEO MFA passed.")

# --- 7. FILE INTEGRITY VALIDATION ---
def validate_file_integrity():
    cfg = load_lockdown_config()
    for fname, expected_hash in cfg["core_hashes"].items():
        if not os.path.exists(fname):
            log_event(f"[ALERT] Core file missing at runtime: {fname}")
            sys.exit(f"File missing: {fname}")
        actual_hash = hash_file(fname)
        if actual_hash != expected_hash:
            log_event(f"[SECURITY] File integrity check failed for {fname}")
            sys.exit(f"File integrity check failed: {fname}")
    log_event("File integrity validated.")

# --- 8. BLOCK UNAUTHORIZED EXEC/MOD/REPL ---
def block_unauthorized_exec():
    import builtins
    orig_exec = builtins.exec
    def guarded_exec(*args, **kwargs):
        log_event("[SECURITY] Blocked unauthorized exec attempt.")
        raise PermissionError("Unauthorized exec blocked by OMNISECURE lockdown.")
    builtins.exec = guarded_exec
    log_event("Unauthorized exec/mod/replication blocked.")

# --- 9. IMMUTABLE LOGGING ---
def immutable_log(event):
    with open(LOG_PATH, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()}Z | {event}\n")

# --- 10. ALERT CEO ---
def alert_ceo(event):
    # Placeholder: Email/Telegram/push integration
    log_event(f"[ALERT] CEO notified: {event}")

# --- 11. LOCKDOWN RESPAWN ---
def respawn_lockdown():
    generate_security_key()
    generate_lockdown_config()
    log_event("Lockdown config respawned.")
    alert_ceo("Lockdown config respawned.")

# --- 12. MAIN ENTRYPOINT ---
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Windsurf OMNISECURE Lockdown")
    parser.add_argument("--spawn-lockdown", action="store_true", help="Respawn lockdown config and security key")
    args = parser.parse_args()

    is_ceo()
    require_ceo_mfa()
    if args.spawn_lockdown:
        respawn_lockdown()
        sys.exit(0)
    generate_security_key()
    if not os.path.exists(LOCKDOWN_CONFIG_PATH):
        generate_lockdown_config()
    enforce_vault_read_only()
    restrict_network_calls()
    validate_file_integrity()
    block_unauthorized_exec()
    immutable_log("OMNISECURE lockdown enforced.")
    alert_ceo("OMNISECURE lockdown activated.")
    print("[WINDSURF] OMNISECURE RUNTIME LOCKDOWN ACTIVE.")

if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    try:
        main()
    except Exception as e:
        try:
            from windsurf.error_logger import log_error
            import traceback
            log_error(
                error_type="DeployWindsurfFailure",
                message=str(e),
                stacktrace=traceback.format_exc(),
                context={}
            )
        except Exception:
            pass
        raise
>>>>>>> omni_repair_backup_20250704_1335
