"""
AIFOLIO™ SAFE AI MODULE: Synthetic Monitoring Bot
- Static, non-sentient
- Periodically checks system endpoints and logs status
- No adaptive or autonomous remediation
"""
import logging
import requests
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/synthetic_monitor_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

ENDPOINTS = [
    "http://localhost:8000/api/policy_audit_log",
    "http://localhost:8000/api/gdpr_ccpa_audit_log",
    "http://localhost:8000/api/webhook_events"
]

def run_synthetic_checks():
    results = {}
    for url in ENDPOINTS:
        try:
            resp = requests.get(url, timeout=5)
            results[url] = resp.status_code
            logging.info(f"{datetime.utcnow().isoformat()} {url} {resp.status_code}")
        except Exception as e:
            results[url] = str(e)
            logging.warning(f"{datetime.utcnow().isoformat()} {url} ERROR {e}")
    return results
