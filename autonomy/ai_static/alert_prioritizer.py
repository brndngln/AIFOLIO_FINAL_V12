"""
AIFOLIO™ SAFE AI MODULE: Alert Prioritizer
- Static only. No recursion, no autonomous retry loops.
- Prioritizes failed emails/SMS for retry queue.
- All actions are logged for human review.
"""
import json
import logging

LOG_PATH = "../../distribution/legal_exports/alert_prioritizer_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)


def prioritize_alerts(alert_log_path):
    with open(alert_log_path, 'r') as f:
        alerts = json.load(f)
    failed = [a for a in alerts if a.get('status') == 'failed']
    # Sort by timestamp, most recent first
    failed.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
    logging.info(f"Prioritized {len(failed)} failed alerts.")
    return failed
