"""
AIFOLIO™ SAFE AI MODULE: Cold Start Minimizer
- Static, non-sentient
- Logs cold start events, suggests pre-warming if needed
- No static or autonomous pre-warming
"""
import logging

LOG_PATH = "../../distribution/legal_exports/cold_start_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

def log_cold_start(event_info):
    logging.info(f"Cold start event: {event_info}")
