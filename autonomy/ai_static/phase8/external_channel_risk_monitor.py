"""
SAFE AI Static Module: External Channel Risk Monitor
- Flags social/reputation risks from static sources (table-driven)
- Logs all detections for admin review
- No adaptive or emergent behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/external_channel_risk_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

RISK_TABLE = {
    "twitter": "medium",
    "reddit": "high",
    "linkedin": "low"
}

def monitor_external_channel(channel, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    risk = RISK_TABLE.get(channel, "unknown")
    event = f"[{timestamp}] EXTERNAL CHANNEL RISK: {channel} = {risk} | Triggered by: {triggered_by}"
    logging.info(event)
    return risk
