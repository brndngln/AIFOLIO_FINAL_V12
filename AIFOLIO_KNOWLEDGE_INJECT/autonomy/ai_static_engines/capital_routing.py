"""
SAFE AI Capital Routing Engine — Phase 10+
Static, Charter-Enforced
"""
from typing import Dict


class CapitalRouter:
    """Static routing of capital across brands/vaults (SAFE, no adaptive logic)"""

    def __init__(self, vaults: Dict[str, Dict[str, float]]):
        self.vaults = vaults

    def route(
        self, from_brand: str, to_brand: str, amount: float, currency: str
    ) -> bool:
        if self.vaults[from_brand][currency] >= amount:
            self.vaults[from_brand][currency] -= amount
            self.vaults[to_brand][currency] = (
                self.vaults[to_brand].get(currency, 0) + amount
            )
            return True
        return False
