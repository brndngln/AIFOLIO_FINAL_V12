# Fail-Safe Email + Receipt Delivery

AIFOLIO™ ensures all emails and receipts are delivered reliably using multi-channel fallback and full audit logging.

## Features

- Primary: Postmark API (with webhooks)
- Secondary: SMTP2GO or SendGrid fallback
- Admin alerts via Telegram (Slack optional)
- AI typo corrector for customer email fields
- Full retry logic and monitoring
- All attempts and results logged in `/analytics/failsafe_email_log.jsonl`
- Strictly non-sentient, deterministic logic

## Usage

```python
from autonomy.pipeline.failsafe_email_delivery import send_email
send_email('user@example.com', 'Test Subject', 'Test Body')
```

## Audit & Safety

- All delivery attempts are logged
- If all channels fail, admin is alerted via Telegram
- No sentient, learning, or autonomous logic is present

---

_See `failsafe_email_delivery.py` for implementation details and extension points._
