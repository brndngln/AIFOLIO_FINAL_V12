# Encrypted Audit Log

All audit events are logged in end-to-end encrypted format using Fernet symmetric encryption. Daily backups are created automatically.

## Usage

```python
from autonomy.security.encrypted_audit_log import log_audit_event, daily_backup
log_audit_event({'action': 'test', 'user': 'admin'})
backup_file = daily_backup()
```

- Audit logs are stored in `/logs/audit_log_encrypted.jsonl`
- Encryption key is stored in `/logs/audit_log.key`
- Backups are named by date in `/logs/`

## Audit & Safety

- No sentient/learning logic.
- Fully deterministic and business-aligned.
- Follows best practices for data protection.
