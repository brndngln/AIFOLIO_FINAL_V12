"""
SAFE AI Static Module: Regional Profitability Map
- Maps profitability by region (static, table-driven)
- Logs all map generations for admin review
- No static or static behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/regional_profitability_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

PROFITABILITY_TABLE = {"us-east-1": 0.25, "eu-west-1": 0.18, "ap-southeast-1": 0.32}


def get_regional_profitability(region, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    profitability = PROFITABILITY_TABLE.get(region, None)
    event = f"[{timestamp}] REGIONAL PROFITABILITY: {region} = {profitability} | Triggered by: {triggered_by}"
    logging.info(event)
    return profitability
