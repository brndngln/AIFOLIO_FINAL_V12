"""
SAFE AI Static Module: Loyalty Program Planner
- Suggests static loyalty program plans (table-driven)
- Logs all suggestions for admin review
- No dynamic, learning, or autonomous behavior (static, table-driven only)
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/loyalty_program_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

LOYALTY_PLANS = ["points", "tiered", "cashback"]


def suggest_loyalty_program(triggered_by):
    timestamp = datetime.utcnow().isoformat()
    event = (
        f"[{timestamp}] LOYALTY PROGRAM: {LOYALTY_PLANS} | Triggered by: {triggered_by}"
    )
    logging.info(event)
    return LOYALTY_PLANS
