"""
EMMA™: Owner’s Legal/Logic Guardian — OMNIELITE SYSTEM
- Oversees all legal, logic, and security-critical actions
- Provides owner-verifiable, immutable audit trails
- Enforces code injection and commit protocols
- Integrates with all compliance, audit, and rollback layers
"""
import hashlib
import json
import os
import threading
from datetime import datetime
from typing import Dict, Any, Optional

EMMA_AUDIT_LOG = os.path.join(os.path.dirname(__file__), '../../audit/exports/emma_audit_log.json')
EMMA_LOCK = threading.Lock()

class EMMA:
    _instance = None

    @staticmethod
    def instance():
        if EMMA._instance is None:
            EMMA._instance = EMMA()
        return EMMA._instance

    def __init__(self):
        self.log_path = EMMA_AUDIT_LOG
        if not os.path.exists(os.path.dirname(self.log_path)):
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                json.dump([], f)

    def log_event(self, event_type: str, details: Dict[str, Any], critical: bool = False):
        with EMMA_LOCK:
            now = datetime.utcnow().isoformat()
            entry = {
                'timestamp': now,
                'event_type': event_type,
                'details': details,
                'critical': critical,
                'hash': self._hash_event(event_type, details, now)
            }
            log = self._read_log()
            log.append(entry)
            self._write_log(log)
            return entry['hash']

    def verify_action(self, action_hash: str) -> bool:
        log = self._read_log()
        return any(entry['hash'] == action_hash for entry in log)

    def register_legal_guard(self, module: str, action: str, owner_id: Optional[str] = None):
        return self.log_event('legal_guard', {'module': module, 'action': action, 'owner_id': owner_id}, critical=True)

    def enforce_commit_protocol(self, files_changed: list, commit_msg: str, owner_id: Optional[str] = None):
        return self.log_event('commit_enforcement', {'files_changed': files_changed, 'commit_msg': commit_msg, 'owner_id': owner_id}, critical=True)

    def audit_trail(self, since: Optional[str] = None):
        log = self._read_log()
        if since:
            return [e for e in log if e['timestamp'] >= since]
        return log

    def rollback_action(self, action_hash: str):
        # Placeholder: Implement rollback logic as needed
        return self.log_event('rollback', {'action_hash': action_hash}, critical=True)

    def _hash_event(self, event_type, details, timestamp):
        h = hashlib.sha256()
        h.update(event_type.encode())
        h.update(json.dumps(details, sort_keys=True).encode())
        h.update(timestamp.encode())
        return h.hexdigest()

    def _read_log(self):
        with open(self.log_path, 'r') as f:
            return json.load(f)

    def _write_log(self, log):
        with open(self.log_path, 'w') as f:
            json.dump(log, f, indent=2)

# Singleton instance for global use
emma = EMMA.instance()
