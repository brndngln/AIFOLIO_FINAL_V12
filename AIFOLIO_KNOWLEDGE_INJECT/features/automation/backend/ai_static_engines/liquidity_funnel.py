"""SAFE AI MODULE"""

"SAFE AI MODULE"
"SAFE AI MODULE"
from typing import Dict


def calculate_liquidity_funnel(vaults: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    return {k: v.get("USD", 0) * 0.05 for k, v in vaults.items()}
