"""
SAFE AI Static Module: Customer Satisfaction Sentiment Map
- Maps static customer satisfaction sentiment (table-driven)
- Logs all maps for admin review
- No static or static behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/customer_satisfaction_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

SATISFACTION_MAP = {"vault1": "high", "vault2": "medium", "vault3": "low"}


def map_customer_satisfaction(vault_id, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    satisfaction = SATISFACTION_MAP.get(vault_id, "unknown")
    event = f"[{timestamp}] CUSTOMER SATISFACTION: {vault_id} = {satisfaction} | Triggered by: {triggered_by}"
    logging.info(event)
    return satisfaction
