# Cloud Sync & Backup Guide

AIFOLIO™ supports automatic backup of vault data, AI prompts, covers, and PDFs to Google Drive or Dropbox.

## Setup
- Install dependencies:
  - `pip install pydrive dropbox`
- Set credentials:
  - For Google Drive: Follow [PyDrive auth guide](https://pythonhosted.org/PyDrive/quickstart.html)
  - For Dropbox: Set `DROPBOX_TOKEN` env variable

## Usage

```bash
python autonomy/pipeline/cloud_sync.py gdrive   # Backup all data to Google Drive
python autonomy/pipeline/cloud_sync.py dropbox  # Backup all data to Dropbox
```

Backups include:
- /analytics/
- /vaults/
- /prompts/
- /covers/
- /pdfs/

---

**All backups are manual or can be scheduled via cron/CI. Future versions will support automated scheduling and incremental backup.**
