"""
SAFE AI Static Module: Black Box Anomaly Detector
- Scans AI module outputs for outlier values or unexpected results
- Static, no recursion or adaptive logic
- Logs anomalies for admin review
"""
import logging
from datetime import datetime
import os

LOG_PATH = "../../distribution/legal_exports/black_box_anomaly_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

MODULE_OUTPUTS = [
    "vault_processing_output.txt",
    "market_analysis_output.txt"
]

THRESHOLDS = {
    "vault_processing_output.txt": 1000,  # Example static threshold
    "market_analysis_output.txt": 500
}


def detect_anomalies(triggered_by):
    timestamp = datetime.utcnow().isoformat()
    anomalies = []
    for output_file in MODULE_OUTPUTS:
        path = os.path.join("../../distribution/legal_exports/", output_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    try:
                        value = int(line.strip())
                        if value > THRESHOLDS[output_file]:
                            anomaly = f"[{timestamp}] ANOMALY: {output_file} | Value: {value} | Triggered by: {triggered_by}"
                            anomalies.append(anomaly)
                            logging.info(anomaly)
                    except Exception:
                        continue
    if not anomalies:
        logging.info(f"[{timestamp}] ANOMALY: No anomalies found. | Triggered by: {triggered_by}")
    return anomalies or ["No anomalies found."]
