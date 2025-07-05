import os
import logging
import requests
from .retry_utils import retry_safe_hook


@retry_safe_hook(max_attempts=3, backoff_tier="short")
def send_confirmation_email(buyer_email, vault_name):
    """
    Sends a confirmation email to the buyer using SendGrid if configured, otherwise prints a stub message.
    Retries up to 3 times on failure, logs all exceptions, and writes final failures to logs/failed_hooks.log.
    """
    api_key = os.environ.get("SENDGRID_API_KEY")
    sender = os.environ.get("SENDGRID_FROM_EMAIL", "noreply@aifolio.com")
    subject = f"Your AIFOLIO Vault '{vault_name}' is Ready!"
    body = f"Thank you for your purchase! Your vault '{vault_name}' is now available."
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
            logging.info(
                f"[AIFOLIO] Confirmation email sent to {buyer_email} for vault '{vault_name}'."
            )
        else:
            logging.error(
                f"[AIFOLIO] Failed to send confirmation email: {resp.status_code} {resp.text}"
            )
            raise RuntimeError(f"SendGrid error: {resp.status_code} {resp.text}")
    else:
        logging.warning(
            f"[AIFOLIO] Confirmation email sent to {buyer_email} for vault '{vault_name}'. (stub, no SENDGRID_API_KEY)"
        )
