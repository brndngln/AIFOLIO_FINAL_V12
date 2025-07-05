# AI_reinvestment_logicsuite.py
# Applies billionaire filter, ROI, and priority logic to reinvestment proposals
class AIReinvestmentLogicSuite:
    def rank_and_filter(self, proposals, brain_profiles):
        # Only allow ROI >= 6 and not saturated
        filtered = [
            p
            for p in proposals
            if p.get("roi", 0) >= 6 and not p.get("saturated", False)
        ]
        # Apply billionaire logic: sort by ROI, growth, and cost
        return sorted(filtered, key=lambda p: (-p["roi"], -p["growth"], p["cost"]))
