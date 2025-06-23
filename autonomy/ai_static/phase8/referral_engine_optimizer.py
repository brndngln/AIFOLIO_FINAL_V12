"""
SAFE AI Static Module: Referral Engine Optimizer
- Suggests static referral program optimizations (table-driven)
- Logs all suggestions for admin review
- No static or static behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/referral_engine_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

REFERRAL_PLANS = ["invite_bonus", "tiered_referral", "seasonal_campaign"]

def suggest_referral_engine(triggered_by):
    timestamp = datetime.utcnow().isoformat()
    event = f"[{timestamp}] REFERRAL ENGINE: {REFERRAL_PLANS} | Triggered by: {triggered_by}"
    logging.info(event)
    return REFERRAL_PLANS
