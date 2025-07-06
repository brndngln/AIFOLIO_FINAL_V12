import os
import logging
import requests
import json

import time
from .retry_utils import retry_safe_hook


@retry_safe_hook(max_attempts=3, backoff_tier="short")
def fraud_check(buyer_data: dict[str, Any], sale_metadata: dict[str, Any]) -> None:
    """
    Runs a static fraud check on the sale. Flags if 'suspicious' in metadata, logs to file, and POSTs to FRAUD_API_URL if set.
    Logs all actions and errors. Retries up to 3 times on failure. Never uses AI learning or memory.
    """
    start = time.time()
    log_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../analytics/fraud_checks.json")
    )
    result = {
        "buyer_data": buyer_data,
        "sale_metadata": sale_metadata,
        "fraud_flag": False,
    }
    if "suspicious" in str(sale_metadata).lower():
        result["fraud_flag"] = True
    api_url = os.environ.get("FRAUD_API_URL")
    try:
        if api_url:
            resp = requests.post(api_url, json=result, timeout=10)
            if resp.status_code == 200:
                logging.info(
                    f"[AIFOLIO] Fraud API check success for buyer: {buyer_data}."
                )
            else:
                logging.error(
                    f"[AIFOLIO] Fraud API error: {resp.status_code} {resp.text}"
                )
                raise RuntimeError(f"Fraud API error: {resp.status_code} {resp.text}")
        if os.path.exists(log_path):
            with open(log_path, "r+") as f:
                logs = json.load(f)
                logs.append(result)
                f.seek(0)
                json.dump(logs, f, indent=2)
        else:
            with open(log_path, "w") as f:
                json.dump([result], f, indent=2)
        if result["fraud_flag"]:
            logging.warning(
                f"[AIFOLIO] FRAUD FLAGGED for buyer {buyer_data}: {sale_metadata}"
            )
        else:
            logging.info(f"[AIFOLIO] Fraud check passed for buyer {buyer_data}.")
    except Exception as e:
        logging.error(f"[AIFOLIO] Exception in fraud check: {e}")
        raise
    elapsed = time.time() - start
    if elapsed > 2.0:
        logging.warning(f"[AIFOLIO][PERF] fraud_check took {elapsed:.2f}s")
