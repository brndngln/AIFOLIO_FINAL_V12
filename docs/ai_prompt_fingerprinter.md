# AI Prompt Fingerprinter

AIFOLIO™ fingerprints every prompt with a unique hash for full traceability and audit compliance.

## Features

- Adds unique hash/fingerprint to every prompt
- Traceable in all logs and audit trails
- Logs all fingerprints in `/analytics/ai_prompt_fingerprint_log.jsonl`
- Strictly non-sentient, deterministic logic

## Usage

```python
from autonomy.pipeline.ai_prompt_fingerprinter import fingerprint_prompt, log_fingerprint
prompt = "Write a professional summary for AIFOLIO."
fp = fingerprint_prompt(prompt)
log_fingerprint(prompt)
print(fp)
```

## Audit & Safety

- All prompts are fingerprinted and logged
- All fingerprints are traceable for compliance
- No sentient, learning, or autonomous logic is present

---

_See `ai_prompt_fingerprinter.py` for implementation details and extension points._
