"""SAFE AI MODULE"""

ct = None  # TODO: Define ct
rates = {}  # TODO: Define rates

"SAFE AI MODULE"
"SAFE AI MODULE"
from typing import Dict


def harmonize_taxes(revenue: Dict[str, float]) -> Dict[str, float]:
    return {k: v * rates.get(k, 0.21) for k, v in revenue.items()}
