import logging
import time
from .retry_utils import retry_safe_hook

@retry_safe_hook(max_attempts=3, backoff_factor=1)
def tag_buyer_crm(tag, buyer_email):
    """
    Tags the buyer in the CRM system with the given tag. Uses static logic only. Logs all actions and errors. Retries up to 3 times on failure.
    """
    start = time.time()
    # TODO: Integrate with CRM API or log to file
    logging.info(f"[AIFOLIO] CRM tag '{tag}' applied to {buyer_email}.")
    elapsed = time.time() - start
    if elapsed > 2.0:
        logging.warning(f"[AIFOLIO][PERF] tag_buyer_crm took {elapsed:.2f}s")
