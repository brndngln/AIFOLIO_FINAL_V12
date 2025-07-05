"""
SAFE AI Static Module: Bias Trend Monitor (Static)
- Scans AI module outputs for static bias patterns (e.g., word/decision frequency)
- Logs findings for admin review
- No loops or self-calling functions; no dynamic or learning logic
"""
import logging
from datetime import datetime
import os
from collections import Counter

LOG_PATH = "../../distribution/legal_exports/bias_trend_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

MODULE_OUTPUTS = ["policy_audit_log.txt", "buyer_receipt_log.txt"]

BIAS_TERMS = ["refund denied", "manual review", "escalate"]


def monitor_bias_trends(triggered_by):
    timestamp = datetime.utcnow().isoformat()
    term_counts = Counter()
    for output_file in MODULE_OUTPUTS:
        path = os.path.join("../../distribution/legal_exports/", output_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    for term in BIAS_TERMS:
                        if term in line:
                            term_counts[term] += 1
    for term, count in term_counts.items():
        event = f"[{timestamp}] BIAS: {term} occurred {count} times | Triggered by: {triggered_by}"
        logging.info(event)
    if not term_counts:
        logging.info(
            f"[{timestamp}] BIAS: No bias terms found. | Triggered by: {triggered_by}"
        )
    return dict(term_counts) or {"result": "No bias terms found."}
