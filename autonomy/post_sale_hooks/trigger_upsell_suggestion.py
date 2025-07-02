import os
import logging
import requests
from .retry_utils import retry_safe_hook

@retry_safe_hook(max_attempts=3, backoff_tier='short')
def trigger_upsell_suggestion(buyer_email, vault_name):
    """
    Suggests an upsell to the buyer after a vault purchase. Retries up to 3 times on failure, logs all exceptions.
    """
    logging.info(f"[AIFOLIO] Upsell suggestion triggered for {buyer_email} on vault '{vault_name}'.")
    api_key = os.environ.get('SENDGRID_API_KEY')
    sender = os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@aifolio.com')
    subject = f"Special Offer: Enhance Your AIFOLIO™ Vault Experience!"
    body = f"Hi! As a thank you for purchasing '{vault_name}', we're offering you an exclusive upgrade. Click here to learn more."
    if api_key:
        try:
            resp = requests.post(
                'https://api.sendgrid.com/v3/mail/send',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'personalizations': [{ 'to': [{ 'email': buyer_email }] }],
                    'from': { 'email': sender },
                    'subject': subject,
                    'content': [{ 'type': 'text/plain', 'value': body }]
                },
                timeout=10
            )
            if resp.status_code == 202:
                logging.info(f"[AIFOLIO] Upsell suggestion email sent to {buyer_email} for vault '{vault_name}'.")
            else:
                logging.error(f"[AIFOLIO] Failed to send upsell suggestion: {resp.status_code} {resp.text}")
        except Exception as e:
            logging.error(f"[AIFOLIO] Exception sending upsell suggestion: {e}")
    else:
        print(f"[AIFOLIO] Upsell suggestion triggered for {buyer_email} on vault '{vault_name}'. (stub, no SENDGRID_API_KEY)")
