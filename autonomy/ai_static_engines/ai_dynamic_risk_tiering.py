"""
AIFOLIO™ AI Dynamic Risk Tiering
Phase 63 — SAFE AI, non-sentient, static, owner-controlled
Assigns low/med/high risk to automations; enables auto-approve for low risk.
"""
from typing import List, Dict
import datetime

RISK_TIER_LOG = []

class DynamicRiskTiering:
    @staticmethod
    def assign_risk(automation: Dict) -> str:
        # Example: statically assign risk by type
        if automation.get('type') in ['metadata_update', 'visual_update']:
            return 'low'
        if automation.get('type') in ['pricing_sync', 'routine_report']:
            return 'medium'
        return 'high'

    @staticmethod
    def log_tier(automation: Dict, risk: str):
        RISK_TIER_LOG.append({
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'automation': automation,
            'risk': risk
        })

    @staticmethod
    def get_log() -> List[Dict]:
        return RISK_TIER_LOG
