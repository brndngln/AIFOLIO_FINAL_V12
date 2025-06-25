"""
AIFOLIO™ AI Owner Intent Engine
Phase 67 — SAFE AI, non-sentient, static, owner-controlled
Predicts and auto-accepts repeating owner actions.
"""
from typing import List, Dict
import datetime

INTENT_LOG = []

class OwnerIntentEngine:
    @staticmethod
    def predict_intent(history: List[Dict]) -> List[str]:
        # Find actions the owner always accepts
        freq = {}
        for h in history:
            k = h.get('action')
            if h.get('accepted'):
                freq[k] = freq.get(k, 0) + 1
        likely = [k for k, v in freq.items() if v > 2]  # Example: 3+ times
        return likely

    @staticmethod
    def auto_accept(actions: List[str]):
        INTENT_LOG.append({
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'auto_accepted': actions
        })

    @staticmethod
    def get_log() -> List[Dict]:
        return INTENT_LOG
