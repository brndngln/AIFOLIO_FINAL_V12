# Lifetime Value Estimator

Estimates LTV per customer, logs all calculations for audit.

## Usage
```python
from autonomy.analytics.lifetime_value_estimator import estimate_lifetime_value
result = estimate_lifetime_value(sales, refunds, customer_id)
```
- `sales`: list of dicts {customer, amount, timestamp}
- `refunds`: list of dicts {customer, amount, timestamp}
- `customer_id`: str

All results are logged to `/analytics/lifetime_value_log.jsonl`.

## Audit & Safety
- No sentient/learning logic.
- Fully deterministic and business-aligned.
