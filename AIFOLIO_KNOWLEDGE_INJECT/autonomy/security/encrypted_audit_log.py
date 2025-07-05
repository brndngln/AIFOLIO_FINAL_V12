import os
import json
import datetime
from cryptography.fernet import Fernet

AUDIT_LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../logs/"))
AUDIT_LOG_FILE = os.path.join(AUDIT_LOG_DIR, "audit_log_encrypted.jsonl")
KEY_FILE = os.path.join(AUDIT_LOG_DIR, "audit_log.key")
os.makedirs(AUDIT_LOG_DIR, exist_ok=True)


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key


def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()


def log_audit_event(event):
    key = load_key()
    fernet = Fernet(key)
    entry = {"timestamp": datetime.datetime.utcnow().isoformat() + "Z", "event": event}
    enc = fernet.encrypt(json.dumps(entry).encode("utf-8"))
    with open(AUDIT_LOG_FILE, "ab") as f:
        f.write(enc + b"\n")
    return True


def daily_backup():
    import shutil

    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    backup_file = os.path.join(AUDIT_LOG_DIR, f"audit_log_encrypted_{today}.bak")
    shutil.copy2(AUDIT_LOG_FILE, backup_file)
    return backup_file


if __name__ == "__main__":
    log_audit_event({"action": "test", "user": "admin"})
    print("Backup:", daily_backup())
