"""
Automated Cashflow Reinvestment Planner — Phase 10+
Static, Charter-Enforced
"""
from typing import Dict

def plan_reinvestment(vaults: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """Static reinvestment plan (SAFE AI, admin approval required)"""
    # Example: allocate 10% of surplus to reinvestment
    plan = {k: v.get("USD", 0) * 0.1 for k, v in vaults.items()}
    return plan
