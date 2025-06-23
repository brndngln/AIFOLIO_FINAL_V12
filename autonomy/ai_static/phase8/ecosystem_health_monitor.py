"""
SAFE AI Static Module: Ecosystem Health Monitor
- Tracks static market/industry health indicators
- Logs all monitoring for admin review
- No static or static behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/ecosystem_health_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

HEALTH_INDICATORS = {
    "legal": "stable",
    "finance": "growing",
    "education": "volatile"
}

def monitor_ecosystem_health(market, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    health = HEALTH_INDICATORS.get(market, "unknown")
    event = f"[{timestamp}] ECOSYSTEM HEALTH: {market} = {health} | Triggered by: {triggered_by}"
    logging.info(event)
    return health
