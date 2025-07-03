"""
SAFE AI Risk Contagion Firewall — Phase 10+
Static, Charter-Enforced
"""
from typing import Dict

def check_risk_contagion(vaults: Dict[str, Dict[str, float]]) -> bool:
    """Detect static risk contagion between brands (SAFE AI, static only)"""
    # Example: if any brand vault drops below threshold, flag risk
    for brand, balances in vaults.items():
        for currency, amount in balances.items():
            if amount < 10000:
                return True
    return False
