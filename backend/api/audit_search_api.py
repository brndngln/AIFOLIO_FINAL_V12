from fastapi import APIRouter, Query
from pathlib import Path
import json
from typing import List, Dict, Any, Optional

router = APIRouter()
LOG_PATH = Path(__file__).parent.parent.parent / "logs" / "secret_rotation.json"
ANOMALY_PATH = Path(__file__).parent.parent.parent / "logs" / "usage_anomalies.json"
OVERRIDE_PATH = Path(__file__).parent.parent.parent / "logs" / "override_attempts.json"


@router.get("/api/audit/search")
def search_audit(
    log: str = Query("rotation", enum=["rotation", "anomaly", "override"]),
    q: str = Query("", description="Free-text search"),
    key: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    admin: Optional[str] = Query(None),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
) -> List[Dict[str, Any]]:
    if log == "rotation":
        path = LOG_PATH
    elif log == "anomaly":
        path = ANOMALY_PATH
    else:
        path = OVERRIDE_PATH
    if not path.exists():
        return []
    with open(path, "r") as f:
        data = json.load(f)
    results: List[Dict[str, Any]] = []
    for row in data:
        if q and q.lower() not in json.dumps(row).lower():
            continue
        if key and row.get("key") != key:
            continue
        if status and row.get("status") != status:
            continue
        if admin and row.get("admin_id") != admin:
            continue
        if start and row.get("timestamp", "")[:10] < start:
            continue
        if end and row.get("timestamp", "")[:10] > end:
            continue
        results.append(row)
    return results
