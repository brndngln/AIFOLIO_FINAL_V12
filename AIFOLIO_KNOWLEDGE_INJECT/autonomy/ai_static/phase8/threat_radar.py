"""
SAFE AI Static Module: Threat Radar
- Warns on static legal/market threats (from static table)
- Logs all threat checks for admin review
- No static or static behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/threat_radar_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

THREAT_TABLE = {
    "legal": ["pending regulation"],
    "finance": ["market volatility"],
    "education": ["policy change"],
}


def check_threats(market, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    threats = THREAT_TABLE.get(market, [])
    event = f"[{timestamp}] THREAT RADAR: {market} -> {threats} | Triggered by: {triggered_by}"
    logging.info(event)
    return threats
