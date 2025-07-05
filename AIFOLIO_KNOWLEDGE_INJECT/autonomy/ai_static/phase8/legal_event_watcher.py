"""
SAFE AI Static Module: Legal Event Watcher
- Flags upcoming legal changes in relevant markets (table-driven)
- Logs all detections for admin review
- No static or static behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/legal_event_watch_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

LEGAL_EVENTS = {
    "us": ["CCPA 2026 update"],
    "eu": ["GDPR 2025 revision"],
    "apac": ["PDPA 2025 expansion"],
}


def watch_legal_events(region, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    events = LEGAL_EVENTS.get(region, [])
    event = (
        f"[{timestamp}] LEGAL EVENT: {region} = {events} | Triggered by: {triggered_by}"
    )
    logging.info(event)
    return events
