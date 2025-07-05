import os
import shutil
import datetime

ANALYTICS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics")
)
BACKUP_DIR = os.path.join(ANALYTICS_DIR, "backups")

os.makedirs(BACKUP_DIR, exist_ok=True)


def backup_analytics_files():
    """Backup all analytics JSON files to backups/ with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    for fname in os.listdir(ANALYTICS_DIR):
        if fname.endswith(".json"):
            src = os.path.join(ANALYTICS_DIR, fname)
            dst = os.path.join(BACKUP_DIR, f"{fname}.{timestamp}.bak")
            shutil.copy2(src, dst)
    print(f"[AIFOLIO] Analytics files backed up to {BACKUP_DIR}.")


# Stub for offsite/cloud sync (S3, GDrive, etc.)
def sync_to_cloud():
    print(
        "[AIFOLIO][STUB] Offsite/cloud sync not yet implemented. Add S3/GDrive logic here."
    )


if __name__ == "__main__":
    backup_analytics_files()
    sync_to_cloud()
