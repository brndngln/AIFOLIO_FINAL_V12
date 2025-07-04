# 🔐 AIFOLIO Encrypted Backup System

- **Encrypted volume:** `AIFOLIO_CORE_VERA.hc`
- **Location:** `/secure/volumes/`
- **Backup Script:** `sync_to_veracrypt.sh`
- **Restore Script:** `restore_from_veracrypt.sh`
- **Not tracked in Git.** `.gitignore` protected.
- All changes pushed to GitHub exclude encrypted or backup files.

## Usage

1. Edit the scripts to add your VeraCrypt password or use environment variables for security.
2. Run `sync_to_veracrypt.sh` to back up your project to the encrypted volume.
3. Run `restore_from_veracrypt.sh` to restore from the encrypted backup.

## Security
- VeraCrypt volumes and backup directories are locked out of version control.
- See `.gitignore` for enforced patterns.
- All backup and restore actions should be logged/audited for compliance.
