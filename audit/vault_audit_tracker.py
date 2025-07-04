# PHASE 91–110: Vault Audit Tracker — Static, SAFE AI, Owner-Controlled
# Logs and snapshots all results, actions, and phase checkpoints for full rollback

import datetime
from aifolio_ai_bots_backend.agents.agent_utils import encrypt_audit_log_entry

class VaultAuditTracker:
    _log = []
    _snapshots = []

    @staticmethod
    def record(action, details=None):
        entry = {
            'action': action,
            'details': details,
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'SAFE_AI_COMPLIANT': True,
            'OWNER_CONTROLLED': True,
            'NON_SENTIENT': True
        }
        VaultAuditTracker._log.append(entry)
        encrypted_log = encrypt_audit_log_entry(entry)
        with open("ai_bots_audit.log", "a") as f:
            f.write(encrypted_log + "\n")

    @staticmethod
    def snapshot(state):
        snap = {
            'state': state,
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'SAFE_AI_COMPLIANT': True,
            'OWNER_CONTROLLED': True,
            'NON_SENTIENT': True
        }
        VaultAuditTracker._snapshots.append(snap)
        VaultAuditTracker.record('snapshot', {'state': state})
        encrypted_log = encrypt_audit_log_entry(snap)
        with open("ai_bots_audit.log", "a") as f:
            f.write(encrypted_log + "\n")

    @staticmethod
    def get_log():
        return list(VaultAuditTracker._log)

    @staticmethod
    def get_snapshots():
        return list(VaultAuditTracker._snapshots)
