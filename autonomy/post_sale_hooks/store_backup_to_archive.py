import os
import shutil
import logging
import json

def store_backup_to_archive(order_id, vault_id):
    """
    Copy a vault file to ARCHIVE_PATH (if set) or log to file. Simulate S3/local archive.
    """
    archive_path = os.environ.get('ARCHIVE_PATH')
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../analytics/backup_archives.json'))
    entry = {'order_id': order_id, 'vault_id': vault_id}
    try:
        if archive_path:
            # Simulate: copy vault file to archive (file path pattern assumed for demo)
            src = f"/vaults/{vault_id}.pdf"
            dst = os.path.join(archive_path, f"{order_id}_{vault_id}.pdf")
            if os.path.exists(src):
                shutil.copy2(src, dst)
                logging.info(f"[AIFOLIO] Vault {vault_id} for order {order_id} archived to {dst}.")
            else:
                logging.warning(f"[AIFOLIO] Source vault file {src} does not exist.")
        if os.path.exists(log_path):
            with open(log_path, 'r+') as f:
                logs = json.load(f)
                logs.append(entry)
                f.seek(0)
                json.dump(logs, f, indent=2)
        else:
            with open(log_path, 'w') as f:
                json.dump([entry], f, indent=2)
        print(f"[AIFOLIO] Backup archived for order {order_id}, vault {vault_id} (ARCHIVE_PATH: {archive_path})")
    except Exception as e:
        logging.error(f"[AIFOLIO] Exception archiving backup: {e}")
