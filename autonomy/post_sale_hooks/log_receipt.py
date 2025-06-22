import os
import json
import logging
from .retry_utils import retry_safe_hook

@retry_safe_hook(max_attempts=3, backoff_factor=1)
def log_receipt_to_db(receipt_data):
    """
    Logs the sale receipt to the database. Retries up to 3 times on failure, logs all exceptions.
    """
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../analytics/receipts.json'))
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r+') as f:
                logs = json.load(f)
                logs.append(receipt_data)
                f.seek(0)
                json.dump(logs, f, indent=2)
        else:
            with open(log_path, 'w') as f:
                json.dump([receipt_data], f, indent=2)
        logging.info(f"[AIFOLIO] Receipt logged: {receipt_data}.")
    except Exception as e:
        logging.error(f"[AIFOLIO] Failed to log receipt: {e}")
