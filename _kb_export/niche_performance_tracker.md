# Niche Performance Tracker

AIFOLIO™ tracks sales, refunds, and quality by niche, with profitability prediction and audit logging.

## Features

- Tracks PDF sales and refunds by niche
- AI content scoring — quality rating per niche
- Niche profitability predictor (trend-based)
- Logs all events in `/analytics/niche_performance_log.jsonl`
- Strictly non-sentient, deterministic logic

## Usage

```python
from autonomy.pipeline.niche_performance_tracker import log_niche_sale, aggregate_niche_stats, predict_niche_profitability
log_niche_sale('Marketing', 'prod_1', 49, refund=False, quality_score=9)
stats = aggregate_niche_stats()
prediction = predict_niche_profitability('Marketing')
print(stats)
print(prediction)
```

## Audit & Safety

- All sales and refunds are logged by niche
- Profitability is predicted based on real data
- No sentient, learning, or autonomous logic is present

---

_See `niche_performance_tracker.py` for implementation details and extension points._
