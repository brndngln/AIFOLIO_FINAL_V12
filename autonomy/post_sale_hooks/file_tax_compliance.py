import os
import logging
import requests
import json

import time
from .retry_utils import retry_safe_hook


class file_tax_compliance:
    @staticmethod
    @retry_safe_hook(max_attempts=3, backoff_tier="short")
    def trigger(sale_data):
        """
        Files a tax compliance event for the sale. Uses static rules only. Logs all actions and errors. Retries up to 3 times on failure.
        """
        start = time.time()
        log_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../analytics/tax_compliance.json")
        )
        api_url = os.environ.get("TAX_API_URL")
        try:
            if api_url:
                resp = requests.post(api_url, json=sale_data, timeout=10)
                if resp.status_code == 200:
                    logging.info(
                        f"[AIFOLIO] Tax compliance API success for sale: {sale_data}."
                    )
                else:
                    logging.error(
                        f"[AIFOLIO] Tax API error: {resp.status_code} {resp.text}"
                    )
                    raise RuntimeError(f"Tax API error: {resp.status_code} {resp.text}")
            else:
                if os.path.exists(log_path):
                    with open(log_path, "r+") as f:
                        logs = json.load(f)
                        logs.append(sale_data)
                        f.seek(0)
                        json.dump(logs, f, indent=2)
                else:
                    with open(log_path, "w") as f:
                        json.dump([sale_data], f, indent=2)
                logging.info(
                    f"[AIFOLIO] Tax compliance logged for sale: {sale_data} (no TAX_API_URL)"
                )
        except Exception as e:
            logging.error(f"[AIFOLIO] Exception in tax compliance: {e}")
            raise
        elapsed = time.time() - start
        if elapsed > 2.0:
            logging.warning(
                f"[AIFOLIO][PERF] file_tax_compliance.trigger took {elapsed:.2f}s"
            )
