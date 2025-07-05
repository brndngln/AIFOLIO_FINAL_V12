import os
import logging
import requests

import time
from .retry_utils import retry_safe_hook


@retry_safe_hook(max_attempts=3, backoff_tier="short")
def send_preview_bundle(buyer_email, vault_preview_data):
    """
    Sends a preview bundle email using SendGrid if configured, otherwise logs to file.
    Retries up to 3 times on failure. Logs all actions and errors. Static, non-autonomous logic only.
    """
    start = time.time()
    api_key = os.environ.get("SENDGRID_API_KEY")
    sender = os.environ.get("SENDGRID_FROM_EMAIL", "noreply@aifolio.com")
    subject = "Your AIFOLIO Vault Preview Bundle"
    body = f"Here is your preview bundle: {vault_preview_data}"
    if api_key:
        resp = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "personalizations": [{"to": [{"email": buyer_email}]}],
                "from": {"email": sender},
                "subject": subject,
                "content": [{"type": "text/plain", "value": body}],
            },
            timeout=10,
        )
        if resp.status_code == 202:
            logging.info(f"[AIFOLIO] Preview bundle sent to {buyer_email}.")
        else:
            logging.error(
                f"[AIFOLIO] Failed to send preview bundle: {resp.status_code} {resp.text}"
            )
            raise RuntimeError(f"SendGrid error: {resp.status_code} {resp.text}")
    else:
        logging.warning(
            f"[AIFOLIO] Preview bundle sent to {buyer_email}. (stub, no SENDGRID_API_KEY)"
        )
    elapsed = time.time() - start
    if elapsed > 2.0:
        logging.warning(f"[AIFOLIO][PERF] send_preview_bundle took {elapsed:.2f}s")
