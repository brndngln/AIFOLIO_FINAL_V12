# AI_reinvestment_logicsuite.py
# Applies billionaire filter, ROI, and priority logic to reinvestment proposals
from typing import List, Dict, Any

class AIReinvestmentLogicSuite:
    def rank_and_filter(self, proposals: List[Dict[str, Any]], brain_profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filters and ranks reinvestment proposals based on ROI, saturation, and billionaire logic.
        Args:
            proposals: List of proposal dicts with 'roi', 'saturated', 'growth', and 'cost'.
            brain_profiles: List of billionaire brain profile dicts (unused in logic, but required for interface).
        Returns:
            List of filtered and ranked proposal dicts.
        """
        # Only allow ROI >= 6 and not saturated
        filtered = [
            p
            for p in proposals
            if p.get("roi", 0) >= 6 and not p.get("saturated", False)
        ]
        # Apply billionaire logic: sort by ROI, growth, and cost
        return sorted(filtered, key=lambda p: (-p["roi"], -p["growth"], p["cost"]))
