"""
AIFOLIO SAFE AI Platform Reputation Report
- Aggregate reviews, static only
"""


def platform_reputation_report(reviews):
    # Expects: list of {'review': str, 'score': int}
    avg = sum(r["score"] for r in reviews) / len(reviews) if reviews else 0
    return {"average_score": avg, "reviews": reviews}
