import os
import zipfile
import json
import datetime

HEALTH_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/asset_health_checker_log.jsonl"
    )
)
os.makedirs(os.path.dirname(HEALTH_LOG), exist_ok=True)


# --- AI Broken Link & Asset Health Checker (Static, Non-Learning) ---
def check_pdf_assets(pdf_path):
    # Placeholder: In production, use PyPDF2 or fitz to extract links/images
    # Here, just check file exists and is non-empty
    exists = os.path.exists(pdf_path)
    size = os.path.getsize(pdf_path) if exists else 0
    status = "ok" if exists and size > 0 else "missing or empty"
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "file": pdf_path,
        "status": status,
    }
    with open(HEALTH_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return status


def check_zip_assets(zip_path):
    # Checks for missing/corrupted files in a zip archive
    if not os.path.exists(zip_path):
        status = "missing zip"
        files = []
    else:
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                files = z.namelist()
            status = "ok"
        except Exception as e:
            status = f"corrupt: {e}"
            files = []
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "file": zip_path,
        "status": status,
        "files": files,
    }
    with open(HEALTH_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return status, files
