"""
AIFOLIO™ AI Personal Empire Companion
Phase 70 — SAFE AI, non-sentient, static, owner-controlled
Generates “Daily Empire Brief” for the owner dashboard.
"""
from typing import Dict
import datetime

DAILY_BRIEF_LOG = []

class PersonalEmpireCompanion:
    @staticmethod
    def generate_brief(today_automations: int, revenue: float, pending: int, risks: int) -> Dict:
        brief = {
            'date': datetime.datetime.utcnow().date().isoformat(),
            'automated': today_automations,
            'revenue': revenue,
            'pending_items': pending,
            'risk_alerts': risks
        }
        DAILY_BRIEF_LOG.append({
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'brief': brief
        })
        return brief

    @staticmethod
    def get_log() -> list:
        return DAILY_BRIEF_LOG
