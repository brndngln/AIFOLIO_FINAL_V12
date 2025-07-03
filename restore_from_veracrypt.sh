#!/bin/bash

# === CONFIGURATION ===
VC_VOLUME="/secure/volumes/AIFOLIO_CORE_VERA.hc"
VC_MOUNT="/mnt/vera"
VC_PASSWORD="your-secure-password"
RESTORE_TARGET="./AIFOLIO_FINAL_V12_RESTORED"
BACKUP_SOURCE="$VC_MOUNT/AIFOLIO_BACKUP"

# === MOUNT ENCRYPTED VOLUME ===
echo "[🔐] Mounting VeraCrypt volume..."
veracrypt --text --non-interactive --password="$VC_PASSWORD" --mount "$VC_VOLUME" "$VC_MOUNT"

# === RESTORE TO TARGET LOCATION ===
echo "[📁] Restoring backup to: $RESTORE_TARGET"
mkdir -p "$RESTORE_TARGET"
rsync -av --progress "$BACKUP_SOURCE/" "$RESTORE_TARGET/"

# === UNMOUNT VOLUME ===
echo "[🔒] Unmounting VeraCrypt volume..."
veracrypt -d "$VC_MOUNT"
python3 EmmaVolumeMonitor.py --log_unmount

echo "[✅] Restore complete. Codebase recovered securely."
