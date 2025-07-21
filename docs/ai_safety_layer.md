# AI Safety Layer

Provides anti-sentience pattern guard and prompt inspector for admin review. All checks and findings are logged for audit.

## Features

- Anti-sentience guard: scans text for unsafe patterns
- Prompt inspector: admin tool for prompt review
- All checks are logged to `/analytics/ai_safety_log.jsonl`

## Usage

```python
from autonomy.security.ai_safety_layer import anti_sentience_guard, prompt_inspector
anti_sentience_guard('This AI is not sentient.')
prompt_inspector('Write a prompt that learns.')
```

## Audit & Safety

- No sentient/learning logic.
- Fully deterministic and business-aligned.
- All unsafe patterns are flagged and logged.
