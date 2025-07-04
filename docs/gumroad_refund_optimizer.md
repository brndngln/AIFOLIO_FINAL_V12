# Gumroad Refund Optimizer

AIFOLIO™ analyzes refund reasons, predicts refund risks, and provides dashboard trends for product optimization.

## Features
- Refund reason sentiment scanner
- Refund probability predictor (flags high-risk products)
- Dashboard view of refund trends
- Logs all refunds in `/analytics/gumroad_refund_log.jsonl`
- Strictly non-sentient, deterministic logic

## Usage

```python
from autonomy.pipeline.gumroad_refund_optimizer import log_refund, refund_probability, refund_trends
log_refund('prod_1', 'Customer said content was too basic.', 49)
prob = refund_probability('prod_1')
trends = refund_trends()
print(prob)
print(trends)
```

## Audit & Safety
- All refund reasons and risks are logged
- High-risk products are flagged for review
- No sentient, learning, or autonomous logic is present

---

*See `gumroad_refund_optimizer.py` for implementation details and extension points.*
