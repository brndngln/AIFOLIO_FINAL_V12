OWNER_LOCK = True
"""
AIFOLIO™ AI Legacy Auto-Safe Mode
Phase 66 — SAFE AI, non-sentient, static, owner-controlled
If OWNER is inactive, runs minimal automations to maintain revenue and stability.
"""
from typing import List, Dict
import datetime

LEGACY_AUTO_LOG = []


class LegacyAutoSafeMode:
    @staticmethod
    def activate_if_inactive(owner_active: bool, automations: List[Dict]) -> List[Dict]:
        if owner_active:
            return []
        # Only run minimal safe automations
        minimal = [
            a
            for a in automations
            if a.get("type") in ["revenue_maintenance", "basic_sync"]
        ]
        LEGACY_AUTO_LOG.append(
            {"timestamp": datetime.datetime.utcnow().isoformat(), "ran": minimal}
        )
        return minimal

    @staticmethod
    def get_log() -> List[Dict]:
        return LEGACY_AUTO_LOG
