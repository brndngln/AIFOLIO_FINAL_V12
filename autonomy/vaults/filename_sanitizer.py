import os
import re
import json
from datetime import datetime

OWNER_LOCK = True

SANITIZER_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../analytics/filename_sanitizer_log.json")
)
os.makedirs(os.path.dirname(SANITIZER_LOG), exist_ok=True)

BRAND_PREFIX = "AIFOLIO"

JUNK_PATTERNS = [
    r"finalcopy\d*",
    r"untitled",
    r"copy\(\d+\)",
    r"document",
    r"temp",
    r"copy",
    r"final",
    r"\s+",
    r"_+",
    r"-+",
    r"\.+",
    r"\(\d+\)",
]


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9 ]", "", title)
    slug = re.sub(r"\s+", "_", slug).strip("_")
    return slug


def sanitize_filename(title: str, ext: str = "pdf") -> str:
    slug = slugify(title)
    filename = f"{BRAND_PREFIX}_{slug}.{ext}"
    for pat in JUNK_PATTERNS:
        filename = re.sub(pat, "", filename, flags=re.IGNORECASE)
    filename = re.sub(r"_+", "_", filename)
    filename = filename.strip("_")
    return filename


def enforce_safe_filename(
    filepath: str, vault_title: str, metadata_path: str = None
) -> str:
    """
    Rename file if needed, update metadata, log changes.
    """
    dirname, oldname = os.path.split(filepath)
    ext = oldname.split(".")[-1]
    safe_name = sanitize_filename(vault_title, ext)
    safe_path = os.path.join(dirname, safe_name)
    log_entry = {
        "old": oldname,
        "new": safe_name,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "unchanged" if oldname == safe_name else "renamed",
    }
    if oldname != safe_name:
        os.rename(filepath, safe_path)
        if metadata_path and os.path.exists(metadata_path):
            with open(metadata_path, "r+") as f:
                meta = json.load(f)
                meta["pdf_filename"] = safe_name
                f.seek(0)
                json.dump(meta, f, indent=2)
                f.truncate()
        log_entry["status"] = "renamed"
    with open(SANITIZER_LOG, "a") as log:
        log.write(json.dumps(log_entry) + "\n")
    return safe_path
