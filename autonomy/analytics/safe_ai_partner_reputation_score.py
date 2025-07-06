"""
AIFOLIO SAFE AI Partner Reputation Score
- Manual, static, admin-reviewed
"""


from typing import List, Dict, TypedDict

class PartnerScore(TypedDict):
    partner: str
    score: int

class ReputationScores(TypedDict):
    reputation_scores: List[PartnerScore]

def partner_reputation_score(partners: List[PartnerScore]) -> ReputationScores:
    # Expects: list of {'partner': str, 'score': int}
    return {"reputation_scores": partners}
