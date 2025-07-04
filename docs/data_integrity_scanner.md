# Data Integrity Scanner

Automatically scans all files for integrity using SHA-256 hashes. Logs all results to `/analytics/data_integrity_log.jsonl` for full auditability.

## Usage

```python
from autonomy.security.data_integrity_scanner import scan_directory_for_integrity
scan_directory_for_integrity('/path/to/your/dir')
```

- All file hashes are logged with timestamp for compliance.
- Errors are logged per file.

## Audit & Safety
- No sentient/learning logic.
- Fully deterministic and business-aligned.
