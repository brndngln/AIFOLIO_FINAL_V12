# AI Output Normalizer

AIFOLIO™ ensures every AI output is checked for tone, reading level, brand guidelines, legal-safe phrasing, and spelling, with full audit logging.

## Features

- Checks tone (professional, friendly, neutral, authoritative)
- Checks reading level (Flesch-Kincaid grade)
- Checks brand guideline terms
- Checks for legal-safe phrasing
- Spell checks all outputs
- Flags any issues for human review
- Logs all normalizations and flags in `/analytics/ai_output_normalizer_log.jsonl`
- Strictly non-sentient, deterministic logic

## Usage

```python
from autonomy.pipeline.ai_output_normalizer import normalize_output
result = normalize_output("AIFOLIO is a reliable, trusted platform. For informational purposes only.")
print(result)
```

## Audit & Safety

- All outputs are checked before publishing
- Any flagged output requires human review
- All checks and flags are logged for audit
- No sentient, learning, or autonomous logic is present

---

_See `ai_output_normalizer.py` for implementation details and extension points._
