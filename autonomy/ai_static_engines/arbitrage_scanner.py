"""
AI Static Cross-Market Arbitrage Scanner — Phase 10+
Charter-Enforced, Static Only
"""
from typing import Dict, List

def scan_arbitrage_opportunities(markets: Dict[str, float]) -> List[str]:
    """Static scan for arbitrage (SAFE AI only)"""
    # Example: flag price differences > 10%
    results = []
    for m1, v1 in markets.items():
        for m2, v2 in markets.items():
            if m1 != m2 and abs(v1 - v2) / max(v1, v2) > 0.1:
                results.append(f"Arbitrage: {m1} vs {m2}")
    return list(set(results))
