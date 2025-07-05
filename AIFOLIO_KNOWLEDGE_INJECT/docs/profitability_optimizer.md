# Profitability Optimizer Dashboard

Computes vault-level and overall ROI, logs all calculations for full auditability.

## Usage
```python
from autonomy.analytics.profitability_optimizer import compute_profitability
result = compute_profitability(sales, refunds, costs)
```
- `sales`: list of dicts {vault, amount, timestamp}
- `refunds`: list of dicts {vault, amount, timestamp}
- `costs`: dict {vault: cost}

All results are logged to `/analytics/profitability_optimizer_log.jsonl`.

## Audit & Safety
- No sentient/learning logic.
- Fully deterministic and business-aligned.
