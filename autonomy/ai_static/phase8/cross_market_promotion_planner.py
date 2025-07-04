"""
SAFE AI Static Module: Cross-Market Promotion Planner
- Suggests static cross-market promotion plans (table-driven)
- Logs all suggestions for admin review
- No dynamic, learning, or autonomous behavior (static, table-driven only)
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/cross_market_promo_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

PROMO_PLANS = ["bundle_offer", "joint_webinar", "affiliate_campaign"]

def plan_cross_market_promotions(triggered_by):
    timestamp = datetime.utcnow().isoformat()
    event = f"[{timestamp}] CROSS MARKET PROMO: {PROMO_PLANS} | Triggered by: {triggered_by}"
    logging.info(event)
    return PROMO_PLANS
