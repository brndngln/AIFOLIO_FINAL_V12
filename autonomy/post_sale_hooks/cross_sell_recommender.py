import os
import logging
import requests
import json

import os
import logging
import requests
import json
import time
from .retry_utils import retry_safe_hook

class cross_sell_recommender:
    @staticmethod
    @retry_safe_hook(max_attempts=3, backoff_factor=1)
    def recommend_next(buyer_email, current_vault=None):
        """
        Generate a cross-sell offer and send via email (SendGrid if configured), or log to file.
        Uses static rule-based logic (e.g., offers a fixed discount).
        Logs all actions and errors. Retries up to 3 times on failure.
        """
        start = time.time()
        offer = f"Special offer: Get 20% off on your next AIFOLIO™ vault!"
        api_key = os.environ.get('SENDGRID_API_KEY')
        sender = os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@aifolio.com')
        subject = "Unlock More Value with AIFOLIO™!"
        body = f"Hi! As a valued customer, here's a cross-sell offer for you. {offer}"
        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../analytics/cross_sell_offers.json'))
        entry = {'buyer_email': buyer_email, 'offer': offer, 'current_vault': current_vault}
        try:
            if api_key:
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
                    logging.info(f"[AIFOLIO] Cross-sell offer sent to {buyer_email}.")
                else:
                    logging.error(f"[AIFOLIO] Failed to send cross-sell offer: {resp.status_code} {resp.text}")
            else:
                if os.path.exists(log_path):
                    with open(log_path, 'r+') as f:
                        logs = json.load(f)
                        logs.append(entry)
                        f.seek(0)
                        json.dump(logs, f, indent=2)
                else:
                    with open(log_path, 'w') as f:
                        json.dump([entry], f, indent=2)
                print(f"[AIFOLIO] Cross-sell offer logged for {buyer_email} (no SENDGRID_API_KEY)")
        except Exception as e:
            logging.error(f"[AIFOLIO] Exception in cross-sell recommender: {e}")
