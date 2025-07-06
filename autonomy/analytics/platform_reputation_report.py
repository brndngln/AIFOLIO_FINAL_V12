"""
AIFOLIO SAFE AI Platform Reputation Report
- Aggregate reviews, static only
"""


from typing import List, Dict, Any

def platform_reputation_report(reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    SAFE AI-compliant: Static platform reputation report. Deterministic, owner-controlled, no adaptive logic.
    """
    avg: float = sum(r["score"] for r in reviews) / len(reviews) if reviews else 0
    return {"average_score": avg, "reviews": reviews}
