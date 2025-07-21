# Backup & Disaster Recovery Policy

## 1. Backup Strategy

- Encrypted, automated daily backups of all code, DB, and user data
- Backups stored in geographically distributed locations
- Backups tested monthly for integrity and restorability

## 2. Disaster Recovery

- Recovery time objective (RTO): 4 hours
- Recovery point objective (RPO): 1 hour
- Documented, tested DR playbooks and scripts

## 3. Roles & Responsibilities

- Security/DevOps team owns backup and DR
- All DR tests and incidents documented and reviewed

---

See scripts/backup_and_dr.sh for implementation.
