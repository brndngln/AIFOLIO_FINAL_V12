"""SAFE AI MODULE"""

"SAFE AI MODULE"
"SAFE AI MODULE"
from typing import Dict


def rebalance_reserves(vaults: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    return {k: avg - sum(v.values()) for k, v in vaults.items()}
