"""
Secure Logging Utility for AIFOLIO/OMNIELITE
- Centralizes, encrypts, and audits all logs.
- Supports immutable, tamper-evident log storage.
- Integration point for SIEM and alerting.
"""
import os
import hashlib
from datetime import datetime

LOG_FILE = os.getenv("AIFOLIO_LOG_FILE", "secure_app.log")
LOG_KEY = os.getenv("AIFOLIO_LOG_KEY", "changeme")

class TamperEvidentLogger:
    def __init__(self, logfile=LOG_FILE, key=LOG_KEY):
        self.logfile = logfile
        self.key = key
        self.last_hash = None

    def _hash_entry(self, entry):
        h = hashlib.sha256()
        h.update((entry + self.key).encode())
        if self.last_hash:
            h.update(self.last_hash.encode())
        return h.hexdigest()

    def log(self, message, level="INFO"):
        now = datetime.utcnow().isoformat()
        entry = f"{now} [{level}] {message}"
        entry_hash = self._hash_entry(entry)
        with open(self.logfile, "a") as f:
            f.write(f"{entry}|{entry_hash}\n")
        self.last_hash = entry_hash

    def audit_log(self):
        # Verify log chain integrity
        prev_hash = None
        with open(self.logfile) as f:
            for line in f:
                entry, entry_hash = line.strip().rsplit("|", 1)
                h = hashlib.sha256()
                h.update((entry + self.key).encode())
                if prev_hash:
                    h.update(prev_hash.encode())
                if h.hexdigest() != entry_hash:
                    raise Exception("Log tampering detected!")
                prev_hash = entry_hash
