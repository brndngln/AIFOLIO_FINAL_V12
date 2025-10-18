# Multi-language Support

AIFOLIO™ supports multi-language generation, spell/grammar checking, and false friend detection, with audit logging for every output.

## Features

- Full multi-language generation
- AI grammar and spell checker for each language
- False friend detector (translation errors)
- All outputs fingerprinted and audit-logged
- Strictly non-sentient, deterministic logic

## Usage

```python
from autonomy.pipeline.multi_language_support import check_language
entry = check_language('Este es un actual problema.', lang='es')
print(entry)
```

## Audit & Safety

- All outputs are checked for spelling and translation errors
- All checks are logged for audit
- No sentient, learning, or autonomous logic is present

---

_See `multi_language_support.py` for implementation details and extension points._
