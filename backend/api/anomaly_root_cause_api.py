from fastapi import APIRouter, Query
from typing import List, Dict, Any
from backend.ai.anomaly_root_cause import analyze_all


router = APIRouter()


@router.get("/api/anomaly/root_cause")
def root_cause_all() -> List[Dict[str, Any]]:
    return analyze_all()


@router.get("/api/anomaly/root_cause_one")
def root_cause_one(idx: int = Query(0)) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = analyze_all()
    if 0 <= idx < len(results):
        return results[idx]
    return {}
