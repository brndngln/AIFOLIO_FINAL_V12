import os
import json
import logging
import requests

import time
from .retry_utils import retry_safe_hook


@retry_safe_hook(max_attempts=3, backoff_tier="short")
def affiliate_attribution(buyer_email, referral_data):
    """
    Handles affiliate attribution for the sale. Uses static logic only. Logs all actions and errors. Retries up to 3 times on failure.
    """
    start = time.time()
    log_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../analytics/affiliate_attribution.json"
        )
    )
    entry = {"buyer_email": buyer_email, "referral_data": referral_data}
    try:
        if os.path.exists(log_path):
            with open(log_path, "r+") as f:
                logs = json.load(f)
                logs.append(entry)
                f.seek(0)
                json.dump(logs, f, indent=2)
        else:
            with open(log_path, "w") as f:
                json.dump([entry], f, indent=2)
        logging.info(f"[AIFOLIO] Affiliate attribution logged for {buyer_email}.")
    except Exception as e:
        logging.error(f"[AIFOLIO] Failed to log affiliate attribution: {e}")
        raise
    api_url = os.environ.get("AFFILIATE_API_URL")
    if api_url:
        try:
            resp = requests.post(api_url, json=entry, timeout=10)
            if resp.status_code == 200:
                logging.info(f"[AIFOLIO] Affiliate engine notified for {buyer_email}.")
            else:
                logging.error(
                    f"[AIFOLIO] Affiliate API error: {resp.status_code} {resp.text}"
                )
                raise RuntimeError(
                    f"Affiliate API error: {resp.status_code} {resp.text}"
                )
        except Exception as e:
            logging.error(f"[AIFOLIO] Exception posting to affiliate API: {e}")
            raise
    else:
        logging.warning(
            f"[AIFOLIO] Affiliate attribution for {buyer_email} | Referral: {referral_data}. (stub, no AFFILIATE_API_URL)"
        )
    elapsed = time.time() - start
    if elapsed > 2.0:
        logging.warning(f"[AIFOLIO][PERF] affiliate_attribution took {elapsed:.2f}s")
