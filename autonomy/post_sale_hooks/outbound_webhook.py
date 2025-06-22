import os
import logging
import requests
import time
from .retry_utils import retry_safe_hook

def get_webhook_urls():
    """
    Returns a list of webhook URLs from env var POST_SALE_WEBHOOK_URLS (comma-separated) or empty list.
    """
    urls = os.environ.get('POST_SALE_WEBHOOK_URLS', '')
    return [u.strip() for u in urls.split(',') if u.strip()]

@retry_safe_hook(max_attempts=3, backoff_factor=1)
def post_sale_event_to_webhooks(event_name, payload):
    """
    Posts the given event payload to all configured outbound webhooks. Retries on failure, logs all outcomes.
    Never blocks main flow.
    """
    urls = get_webhook_urls()
    for url in urls:
        start = time.time()
        try:
            resp = requests.post(url, json={"event": event_name, "payload": payload}, timeout=10)
            if resp.status_code in (200, 201, 202):
                logging.info(f"[AIFOLIO] Outbound webhook success: {url} event={event_name}")
            else:
                logging.error(f"[AIFOLIO] Outbound webhook failed: {url} code={resp.status_code} body={resp.text}")
        except Exception as e:
            logging.error(f"[AIFOLIO] Exception posting to webhook {url}: {e}")
        elapsed = time.time() - start
        if elapsed > 2.0:
            logging.warning(f"[AIFOLIO][PERF] Outbound webhook {url} took {elapsed:.2f}s")
