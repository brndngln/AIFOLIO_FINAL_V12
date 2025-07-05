"""
SAFE AI Static Module: Seasonal Campaign Optimizer
- Suggests static seasonal campaign plans (table-driven)
- Logs all suggestions for admin review
- No dynamic, learning, or autonomous behavior (static, table-driven only)
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/seasonal_campaign_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

SEASONAL_CAMPAIGNS = ["spring_sale", "back_to_school", "holiday_special"]


def optimize_seasonal_campaigns(triggered_by):
    timestamp = datetime.utcnow().isoformat()
    event = f"[{timestamp}] SEASONAL CAMPAIGN: {SEASONAL_CAMPAIGNS} | Triggered by: {triggered_by}"
    logging.info(event)
    return SEASONAL_CAMPAIGNS
