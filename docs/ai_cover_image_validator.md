# AI Cover Image Validator

AIFOLIO™ validates cover images for legibility, brand consistency, and inappropriate imagery, with full audit logging and human preview required.

## Features
- Validates cover images for text legibility
- Checks brand consistency (placeholder logic)
- Flags inappropriate imagery (brightness/contrast)
- Human review preview step is required for all outputs
- Logs all checks in `/analytics/ai_cover_image_validator_log.jsonl`
- Strictly non-sentient, deterministic logic

## Usage

```python
from autonomy.pipeline.ai_cover_image_validator import validate_cover_image
result = validate_cover_image('cover.jpg')
print(result)
```

## Audit & Safety
- All cover images are validated before publishing
- Any flagged output requires human review
- All checks and flags are logged for audit
- No sentient, learning, or autonomous logic is present

---

*See `ai_cover_image_validator.py` for implementation details and extension points.*
