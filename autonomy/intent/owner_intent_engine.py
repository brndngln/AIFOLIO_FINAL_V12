# V80 Owner Intent Engine — Static, SAFE AI, Owner-Controlled
# Tracks and applies owner intent modes: Fully Automate, Oversight, Override
# Learns from last 30 days of actions (static, deterministic, no adaptation)

import datetime


class OwnerIntentEngine:
    _mode = "oversight"
    _history = []

    @staticmethod
    def set_mode(mode):
        assert mode in ["auto", "oversight", "override"]
        OwnerIntentEngine._mode = mode
        OwnerIntentEngine._history.append(
            {
                "event": "set_mode",
                "mode": mode,
                "timestamp": datetime.datetime.utcnow().isoformat(),
            }
        )

    @staticmethod
    def get_mode():
        return OwnerIntentEngine._mode

    @staticmethod
    def record_action(action, approved):
        OwnerIntentEngine._history.append(
            {
                "action": action,
                "approved": approved,
                "timestamp": datetime.datetime.utcnow().isoformat(),
            }
        )

    @staticmethod
    def get_history():
        return list(OwnerIntentEngine._history)
