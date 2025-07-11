#!/bin/bash
# Encrypted backup and disaster recovery script
BACKUP_DIR=backup_$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
# Backup backend and frontend
cp -r ../backend $BACKUP_DIR/
cp -r ../frontend $BACKUP_DIR/
# Encrypt backup (stub: replace with gpg or cloud KMS)
tar czf $BACKUP_DIR.tar.gz $BACKUP_DIR
# Remove plain backup
rm -rf $BACKUP_DIR
