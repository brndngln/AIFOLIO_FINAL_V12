"""
AIFOLIO™ SAFE AI MODULE: Vault Delivery Monitor
- Static only. No adaptive changes, no recursion.
- Monitors delivery success rates and flags slow vaults.
- Suggest-only: No automated actions.
- All findings are logged for human review.
"""
import json
import logging

LOG_PATH = "../../distribution/legal_exports/vault_delivery_monitor_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

SLOW_THRESHOLD_SECONDS = 300  # 5 minutes

def monitor_deliveries(delivery_log_path):
    with open(delivery_log_path, 'r') as f:
        deliveries = json.load(f)
    slow = [d for d in deliveries if d.get('duration', 0) > SLOW_THRESHOLD_SECONDS]
    for d in slow:
        logging.warning(f"Slow delivery flagged: {d}")
    return slow
