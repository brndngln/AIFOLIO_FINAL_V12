from ai_logic.vault_revenue_optimizer import VaultRevenueOptimizer
from typing import Dict, Any
import pytest

def test_optimize_applies_static_strategies():
    vault = {"id": "V1001", "revenue_optimized": False}
    strategies = ["static_bundle", "fixed_discount"]
    optimizer = VaultRevenueOptimizer()
    result = optimizer.optimize(vault, strategies)
    assert result["applied_strategies"] == strategies
    assert result["revenue_optimized"] is True
    assert result["id"] == "V1001"
    # Ensure no adaptive or sentient logic
    assert "ai" not in result and "adaptive" not in result
