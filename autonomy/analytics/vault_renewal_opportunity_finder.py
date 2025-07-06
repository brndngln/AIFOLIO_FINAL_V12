"""
AIFOLIO SAFE AI Vault Renewal Opportunity Finder
- Static, aggregate, flags vaults with renewal potential
"""


from typing import List, Dict, Any
import datetime

def vault_renewal_opportunity(vaults: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    SAFE AI-compliant: Static vault renewal opportunity finder. Deterministic, owner-controlled, no adaptive logic.
    """
    today = datetime.datetime.now().date()
    flagged = [
        v
        for v in vaults
        if (
            today - datetime.datetime.strptime(v["last_renewal"], "%Y-%m-%d").date()
        ).days > 365
        and v["revenue"] > 0
    ]
    return {"renewal_candidates": flagged}
