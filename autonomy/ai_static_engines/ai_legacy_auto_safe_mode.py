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
    """AI Legacy Auto-Safe Mode for AIFOLIO.
    SAFE AI: Static, deterministic, owner-controlled, fully auditable, no adaptive/sentient logic.
    If OWNER is inactive, runs minimal automations to maintain revenue and stability.
    """
    @staticmethod
    def activate_if_inactive(owner_active: bool, automations: list[dict]) -> list[dict]:
        """Activate minimal safe automations if owner is inactive.
        SAFE AI: Static, deterministic, owner-controlled, fully auditable, no adaptive/sentient logic.
        """
        if owner_active:
            return []
        # Only run minimal safe automations
        minimal: list[dict] = [
            a
            for a in automations
            if a.get("type") in ["revenue_maintenance", "basic_sync"]
        ]
        LEGACY_AUTO_LOG.append(
            {"timestamp": datetime.datetime.utcnow().isoformat(), "ran": minimal}
        )
        return minimal

    @staticmethod
    def get_log() -> list[dict]:
        """Get the legacy auto-safe log.
        SAFE AI: Static, deterministic, owner-controlled, fully auditable, no adaptive/sentient logic.
        """
        return LEGACY_AUTO_LOG
