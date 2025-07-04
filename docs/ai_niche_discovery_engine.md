# AI Niche Discovery Engine

AIFOLIO™ analyzes trends to suggest new, declining, and emerging micro-niches, with full audit logging.

## Features
- Background task that analyzes sales and refund trends
- Suggests new, declining, and emerging micro-niches
- Logs all discoveries in `/analytics/ai_niche_discovery_log.jsonl`
- Strictly non-sentient, deterministic logic

## Usage

```python
from autonomy.pipeline.ai_niche_discovery_engine import discover_niches
entry = discover_niches('../../analytics/niche_performance_log.jsonl', '../../analytics/gumroad_refund_log.jsonl')
print(entry)
```

## Audit & Safety
- All discoveries are logged for audit
- No sentient, learning, or autonomous logic is present

---

*See `ai_niche_discovery_engine.py` for implementation details and extension points.*
