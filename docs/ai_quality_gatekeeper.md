# AI Quality Gatekeeper

AIFOLIO™ blocks low-quality or risky AI outputs from being published, with full audit and human review.

## Features
- Reviews every new product/output before publishing
- Scores grammar, factuality, style, readability, legal flags
- Blocks any output with low scores or legal risks
- Logs all reviews and blocks in `/analytics/ai_quality_gatekeeper_log.jsonl`
- Strictly non-sentient, deterministic logic

## Usage

```python
from autonomy.pipeline.ai_quality_gatekeeper import score_output
result = score_output("AIFOLIO is a trusted, compliant platform.")
print(result)
```

## Audit & Safety
- All outputs are scored before publishing
- Any blocked output requires human review
- All reviews and blocks are logged for audit
- No sentient, learning, or autonomous logic is present

---

*See `ai_quality_gatekeeper.py` for implementation details and extension points.*
