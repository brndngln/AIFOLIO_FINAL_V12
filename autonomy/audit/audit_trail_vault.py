# V80 Audit Trail Vault — Static, SAFE AI, Owner-Controlled
# Tracks all actions, rollbacks, change history, and backup snapshots

import datetime


class AuditTrailVault:
    _log = []
    _snapshots = []

    @staticmethod
    def record(action, details=None):
        AuditTrailVault._log.append(
            {
                "action": action,
                "details": details,
                "timestamp": datetime.datetime.utcnow().isoformat(),
            }
        )

    @staticmethod
    def snapshot(state):
        AuditTrailVault._snapshots.append(
            {"state": state, "timestamp": datetime.datetime.utcnow().isoformat()}
        )
        AuditTrailVault.record("snapshot", {"state": state})

    @staticmethod
    def get_log():
        return list(AuditTrailVault._log)

    @staticmethod
    def get_snapshots():
        return list(AuditTrailVault._snapshots)

    @staticmethod
    def rollback(snapshot_index):
        if 0 <= snapshot_index < len(AuditTrailVault._snapshots):
            AuditTrailVault.record("rollback", {"to": snapshot_index})
            return AuditTrailVault._snapshots[snapshot_index]["state"]
        return None
