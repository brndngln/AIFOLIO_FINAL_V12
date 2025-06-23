"""
SAFE AI Static Module: Drift Detection Monitor
- Compares static output snapshots to detect drift
- Logs drift events for admin review
- No recursion, no adaptive logic
"""
import logging
from datetime import datetime
import os

LOG_PATH = "../../distribution/legal_exports/drift_detection_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

SNAPSHOT_DIR = "../../distribution/legal_exports/snapshots/"


def detect_drift(module_name, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    base_path = os.path.join(SNAPSHOT_DIR, f"{module_name}_base.txt")
    latest_path = os.path.join(SNAPSHOT_DIR, f"{module_name}_latest.txt")
    drift_found = False
    if os.path.exists(base_path) and os.path.exists(latest_path):
        with open(base_path, "r") as f1, open(latest_path, "r") as f2:
            base = f1.read()
            latest = f2.read()
            if base != latest:
                drift_found = True
                event = f"[{timestamp}] DRIFT: {module_name} output drift detected | Triggered by: {triggered_by}"
                logging.info(event)
    if not drift_found:
        logging.info(f"[{timestamp}] DRIFT: No drift detected for {module_name} | Triggered by: {triggered_by}")
    return drift_found
