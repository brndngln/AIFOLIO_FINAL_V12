#!/bin/bash

# === CONFIGURATION ===
VC_VOLUME="/secure/volumes/AIFOLIO_CORE_VERA.hc"
VC_MOUNT="/mnt/vera"
VC_PASSWORD="your-secure-password"  # 🔐 Consider prompting or using a secret manager
SOURCE_DIR="./AIFOLIO_FINAL_V12"
BACKUP_TARGET="$VC_MOUNT/AIFOLIO_BACKUP"

# === MOUNT ENCRYPTED VOLUME ===
echo "[🔐] Mounting VeraCrypt volume..."
veracrypt --text --non-interactive --password="$VC_PASSWORD" --mount "$VC_VOLUME" "$VC_MOUNT"

# === SYNC CODEBASE TO VERA ===
echo "[📁] Syncing project files to encrypted backup..."
rsync -av --progress --exclude=".git" --exclude-from="$SOURCE_DIR/.gitignore" "$SOURCE_DIR/" "$BACKUP_TARGET/"

# === UNMOUNT VOLUME ===
echo "[🔒] Unmounting VeraCrypt volume..."
veracrypt -d "$VC_MOUNT"

echo "[✅] Backup complete and securely stored in VeraCrypt volume."
