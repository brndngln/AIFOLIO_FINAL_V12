"""
AIFOLIO™ SAFE AI MODULE: Webhook Latency Monitor
- Static, non-sentient
- Measures webhook response latency and logs results
- No adaptive retries or dynamic routing
"""
import logging
import requests
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/webhook_latency_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

WEBHOOKS = [
    "https://your.webhook.url/refund",
    "https://your.webhook.url/download",
    "https://your.webhook.url/vault_version"
]

def check_webhook_latency():
    results = {}
    for url in WEBHOOKS:
        try:
            start = datetime.utcnow()
            resp = requests.post(url, json={"ping": True}, timeout=5)
            latency = (datetime.utcnow() - start).total_seconds()
            results[url] = latency
            logging.info(f"{datetime.utcnow().isoformat()} {url} {latency}s {resp.status_code}")
        except Exception as e:
            results[url] = str(e)
            logging.warning(f"{datetime.utcnow().isoformat()} {url} ERROR {e}")
    return results
