# Refund Causality Explorer

Analyzes refund reasons and patterns, suggests possible causes for admin review. All results are logged for audit.

## Usage

```python
from autonomy.analytics.refund_causality_explorer import explore_refund_causality
result = explore_refund_causality(refunds, sales, reasons)
```

- `refunds`: list of dicts {vault, customer, reason, timestamp}
- `sales`: list of dicts {vault, customer, timestamp}
- `reasons`: list of str (known reason categories)

All results are logged to `/analytics/refund_causality_log.jsonl`.

## Audit & Safety

- No sentient/learning logic.
- Fully deterministic and business-aligned.
