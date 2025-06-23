"""
SAFE AI Static Module: Customer Segment Discovery
- Discovers static customer segments (table-driven)
- Logs all discoveries for admin review
- No adaptive or emergent behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/customer_segment_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

SEGMENTS = ["enterprise", "smb", "consumer"]

def discover_customer_segments(triggered_by):
    timestamp = datetime.utcnow().isoformat()
    event = f"[{timestamp}] CUSTOMER SEGMENTS: {SEGMENTS} | Triggered by: {triggered_by}"
    logging.info(event)
    return SEGMENTS
