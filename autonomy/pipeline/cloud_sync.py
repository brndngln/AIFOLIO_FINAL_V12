import os
import glob
import datetime

# Google Drive
try:
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
except ImportError:
    GoogleAuth = GoogleDrive = None

# Dropbox
try:
    import dropbox
except ImportError:
    dropbox = None

ANALYTICS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics'))
VAULTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../vaults'))
PROMPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../prompts'))
COVERS_DIR = os.path.abspath(os.path.dirname(__file__), '../../covers'))
PDFS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pdfs'))

# Utility to collect all files for backup
BACKUP_TARGETS = [ANALYTICS_DIR, VAULTS_DIR, PROMPTS_DIR, COVERS_DIR, PDFS_DIR]

def collect_files():
    files = []
    for d in BACKUP_TARGETS:
        if os.path.exists(d):
            for root, _, filenames in os.walk(d):
                for f in filenames:
                    files.append(os.path.join(root, f))
    return files

# Google Drive backup

def backup_to_gdrive():
    if GoogleAuth is None or GoogleDrive is None:
        print("[AIFOLIO][ERROR] PyDrive not installed. Skipping Google Drive backup.")
        return
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    files = collect_files()
    for f in files:
        file_drive = drive.CreateFile({'title': os.path.basename(f)})
        file_drive.SetContentFile(f)
        file_drive.Upload()
        print(f"[AIFOLIO][GDRIVE] Uploaded: {f}")

# Dropbox backup

def backup_to_dropbox(token=None):
    if dropbox is None:
        print("[AIFOLIO][ERROR] Dropbox SDK not installed. Skipping Dropbox backup.")
        return
    token = token or os.environ.get('DROPBOX_TOKEN')
    if not token:
        print("[AIFOLIO][ERROR] Dropbox token not set.")
        return
    dbx = dropbox.Dropbox(token)
    files = collect_files()
    for f in files:
        with open(f, 'rb') as fh:
            dbx.files_upload(fh.read(), f"/AIFOLIO_BACKUP/{os.path.relpath(f, start=os.path.dirname(__file__))}", mode=dropbox.files.WriteMode.overwrite)
        print(f"[AIFOLIO][DROPBOX] Uploaded: {f}")

if __name__ == "__main__":
    # Example usage: python cloud_sync.py gdrive|dropbox
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'gdrive':
        backup_to_gdrive()
    elif len(sys.argv) > 1 and sys.argv[1] == 'dropbox':
        backup_to_dropbox()
    else:
        print("Usage: python cloud_sync.py [gdrive|dropbox]")
