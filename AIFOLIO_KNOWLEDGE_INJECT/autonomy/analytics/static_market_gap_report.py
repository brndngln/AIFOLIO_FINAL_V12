"""
AIFOLIO SAFE AI Static Market Gap Report
- Aggregate, static, manual input
"""


def static_market_gap_report(gaps):
    # Expects: list of {'gap': str, 'size': int}
    return {"market_gaps": gaps}
