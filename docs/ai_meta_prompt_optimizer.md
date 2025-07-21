# AI Meta-Prompt Optimizer

AIFOLIO™ logs and suggests meta-prompt improvements for higher conversions, lower refunds, and better readability, always requiring human review.

## Features

- Continuously logs and suggests meta-prompt improvements
- Considers conversion rate, refund rate, readability
- Changes only go live after human review
- Logs all suggestions in `/analytics/ai_meta_prompt_optimizer_log.jsonl`
- Strictly non-sentient, deterministic logic

## Usage

```python
from autonomy.pipeline.ai_meta_prompt_optimizer import optimize_meta_prompt
suggestion = optimize_meta_prompt("Get the best out of AIFOLIO!", 0.12, 0.25, 7.5)
print(suggestion)
```

## Audit & Safety

- All suggestions require human review before going live
- All logs are exportable for audit
- No sentient, learning, or autonomous logic is present

---

_See `ai_meta_prompt_optimizer.py` for implementation details and extension points._
