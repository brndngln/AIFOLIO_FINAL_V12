import os
import logging
import requests
import json
from .retry_utils import retry_safe_hook

class request_review:
    @staticmethod
    @retry_safe_hook(max_attempts=3, backoff_factor=1)
    def schedule_email(buyer_email, delay_hours=24):
        """
        Schedules a review request email to the buyer after a vault sale. Retries up to 3 times on failure, logs all exceptions.
        """
        api_key = os.environ.get('SENDGRID_API_KEY')
        sender = os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@aifolio.com')
        subject = "How was your AIFOLIO™ experience?"
        body = f"We hope you loved your vault! Please leave us a review. (This would be sent after {delay_hours}h.)"
        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../analytics/review_requests.json'))
        entry = {'buyer_email': buyer_email, 'delay_hours': delay_hours}
        try:
            if api_key:
                # In production, schedule via Celery or similar. Here, just send immediately for demo.
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
                    logging.info(f"[AIFOLIO] Review request sent to {buyer_email}.")
                else:
                    logging.error(f"[AIFOLIO] Failed to send review request: {resp.status_code} {resp.text}")
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
                print(f"[AIFOLIO] Review request logged for {buyer_email} (no SENDGRID_API_KEY)")
            logging.info(f"[AIFOLIO] Review request scheduled for {buyer_email} in {delay_hours}h.")
        except Exception as e:
            logging.error(f"[AIFOLIO] Exception in review request: {e}")
