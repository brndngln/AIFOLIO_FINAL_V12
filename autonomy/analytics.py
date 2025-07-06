"""
Phase 9+ SAFE AI Advanced Analytics (static, SAFE AI compliant)
- Computes analytics from audit log for dashboard analytics panel
- No adaptive logic; all calculations are static
"""
import datetime
import json
from collections import Counter, defaultdict


from typing import Dict, Any, List, Optional, Tuple, Callable, TypedDict, Union

# SAFE AI Compliance: This module is static, deterministic, owner-controlled, and fully auditable. No adaptive or sentient logic is present. All extension points are documented for static analytics only.

class AuditEvent(TypedDict, total=False):
    timestamp: Optional[str]
    key: Optional[str]
    action: Optional[str]
    endpoint: Optional[str]
    status: Optional[str]
    latency: Optional[float]

def parse_line(line: str) -> Optional[AuditEvent]:
    # Example: [2025-06-23T18:01:54.123456] API_KEY_USAGE: key=PHASE9SAFEKEY action=access endpoint=/phase9/foo
    if "API_KEY_USAGE:" not in line:
        return None
    try:
        ts = line.split("]")[0][1:]
        rest = line.split("API_KEY_USAGE: ")[1]
        parts = dict(
            x.split("=")
            for x in rest.replace(" endpoint", ";endpoint")
            .replace(" action", ";action")
            .replace(" key", ";key")
            .split(";")
            if "=" in x
        )
        return {
            "timestamp": ts,
            "key": parts.get("key"),
            "action": parts.get("action"),
            "endpoint": parts.get("endpoint"),
        }
    except Exception:
        return None


def get_analytics(
    filters: Optional[Dict[str, str]] = None,
    search: Optional[Dict[str, str]] = None,
    time_range: Optional[Tuple[str, str]] = None,
) -> Dict[str, Any]:
    logfile = "distribution/legal_exports/phase9_empire_audit_log.txt"
    try:
        with open(logfile, "r") as f:
            lines = f.readlines()
    except Exception:
        return {}
    events: List[AuditEvent] = [e for e in (parse_line(l) for l in lines) if e is not None]
    from autonomy.key_management import load_keys

    key_roles = load_keys()
    # Time range filtering
    if time_range:
        start, end = time_range
        events = [
            e for e in events if e.get("timestamp") is not None and start <= e["timestamp"] <= end
        ]
    # Regex or substring search
    if search:
        import re

        if search.get("regex"):
            pat = re.compile(search["regex"])
            events = [e for e in events if any(pat.search(str(v)) for v in e.values() if v is not None)]
        elif search.get("substring"):
            sub = search["substring"]
            events = [e for e in events if any(sub in str(v) for v in e.values() if v is not None)]
    # Advanced filtering
    if filters:
        events = filter_events(events, filters)
    # Analytics breakdowns
    total_calls = len(events)
    unique_keys = len(set(e["key"] for e in events if e["key"] is not None))
    most_active_key = Counter(e["key"] for e in events if e["key"] is not None).most_common(1)
    unique_keys = len(set(e["key"] for e in events if e["key"]))
    most_active_key = Counter(e["key"] for e in events if e["key"]).most_common(1)
    most_active_key = most_active_key[0][0] if most_active_key else None
    most_used_endpoint = Counter(
        e["endpoint"] for e in events if e["endpoint"]
    ).most_common(1)
    most_used_endpoint = most_used_endpoint[0][0] if most_used_endpoint else None
    calls_by_role: Dict[str, int] = defaultdict(int)
    for e in events:
        role = key_roles.get(e["key"], "unknown")
        calls_by_role[role] += 1
    now = datetime.datetime.now()
    last_24h_calls = sum(
        1 for e in events if (
            e["timestamp"] is not None and (
                (now - datetime.datetime.fromisoformat(e["timestamp"])).total_seconds() < 86400
            )
        )
    )
    # Per-key, per-endpoint, per-role, per-status breakdowns
    per_key = get_per_key_endpoint_breakdown(events, key_roles)
    per_role = get_per_role_endpoint_breakdown(events, key_roles)
    per_status = get_per_status_breakdown(events)
    error_rate = get_error_rate(events)
    latency_stats = get_latency_stats(events)
    return {
        "total_calls": total_calls,
        "unique_keys": unique_keys,
        "most_active_key": most_active_key,
        "most_used_endpoint": most_used_endpoint,
        "calls_by_role": dict(calls_by_role),
        "last_24h_calls": last_24h_calls,
        "endpoint_breakdown": get_endpoint_breakdown(events),
        "time_series": get_time_series(events),
        "per_key_endpoint_breakdown": per_key,
        "per_role_endpoint_breakdown": per_role,
        "per_status_breakdown": per_status,
        "error_rate": error_rate,
        "latency_stats": latency_stats,
        "role_time_series": get_role_time_series(events, key_roles),
        "events": events,  # for export/search
    }


def get_per_role_endpoint_breakdown(
    events: List[AuditEvent], key_roles: Dict[str, str]
) -> Dict[str, Dict[str, int]]:
    result: Dict[str, Dict[str, int]] = {}
    for e in events:
        role = key_roles.get(e.get("key", ""), "unknown")
        ep = e.get("endpoint", None)
        if role and ep:
            if role not in result:
                result[role] = {}
            result[role][ep] = result[role].get(ep, 0) + 1
    return result


def get_per_status_breakdown(events: List[AuditEvent]) -> Dict[str, Dict[str, int]]:
    result: Dict[str, Dict[str, int]] = {}
    for e in events:
        status = e.get("status", None)
        ep = e.get("endpoint", None)
        if status and ep:
            if status not in result:
                result[status] = {}
            result[status][ep] = result[status].get(ep, 0) + 1
    return result


def get_error_rate(events: List[AuditEvent]) -> Dict[str, float]:
    total: int = len(events)
    errors: int = sum(
        1
        for e in events
        if str(e.get("status", "")).startswith("4")
        or str(e.get("status", "")).startswith("5")
    )
    return {"error_count": float(errors), "error_rate": float(errors) / float(total) if total else 0.0}


def get_latency_stats(events: List[AuditEvent]) -> Dict[str, Dict[str, float]]:
    from statistics import mean, median, quantiles

    result: Dict[str, Dict[str, float]] = {}
    for ep in set(e.get("endpoint", None) for e in events if e.get("endpoint", None)):
        if ep is None:
            continue
        latencies: List[float] = [
            float(e["latency"])  # type: ignore
            for e in events
            if e.get("endpoint", None) == ep and e.get("latency", None) is not None
        ]
        if latencies:
            p95: float = quantiles(latencies, n=100)[94] if len(latencies) >= 20 else 0.0
            result[ep] = {
                "min": min(latencies),
                "max": max(latencies),
                "avg": mean(latencies),
                "median": median(latencies),
                "p95": p95,
            }
    return result


def export_events_csv(events: List[AuditEvent]) -> str:
    import csv
    import io

    if not events:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=sorted(events[0].keys()))
    writer.writeheader()
    for e in events:
        writer.writerow(e)
    return output.getvalue()


def export_events_json(events: List[AuditEvent]) -> str:
    return json.dumps(events, indent=2)


def generate_compliance_report(events: List[AuditEvent]) -> Dict[str, Any]:
    # Returns a dict summarizing compliance-relevant stats
    error_rate = get_error_rate(events)
    return {
        "total_events": len(events),
        "error_rate": error_rate,
        "unique_keys": len(set(e["key"] for e in events if e.get("key"))),
        "unique_endpoints": len(
            set(e["endpoint"] for e in events if e.get("endpoint"))
        ),
        "time_range": (events[0]["timestamp"], events[-1]["timestamp"])
        if events
        else (None, None),
    }


def filter_events(events: List[AuditEvent], filters: Dict[str, str]) -> List[AuditEvent]:
    filtered = []
    for e in events:
        match = True
        for k, v in filters.items():
            if e.get(k) != v:
                match = False
                break
        if match:
            filtered.append(e)
    return filtered


def get_per_key_endpoint_breakdown(
    events: List[AuditEvent], key_roles: Dict[str, str]
) -> Dict[str, Dict[str, int]]:
    result: Dict[str, Dict[str, int]] = {}
    for e in events:
        k = e.get("key", None)
        ep = e.get("endpoint", None)
        if k and ep:
            if k not in result:
                result[k] = {}
            result[k][ep] = result[k].get(ep, 0) + 1
    return result


def get_role_time_series(
    events: List[AuditEvent], key_roles: Dict[str, str]
) -> Dict[str, Dict[str, int]]:
    days: Dict[str, Dict[str, int]] = {}
    for e in events:
        if e.get("timestamp", None) and e.get("key", None):
            role = key_roles.get(e["key"], "unknown")
            day = e["timestamp"][:10]
            if day not in days:
                days[day] = {}
            days[day][role] = days[day].get(role, 0) + 1
    return days


def get_endpoint_breakdown(events: List[AuditEvent]) -> Dict[str, int]:
    counts: Counter[str] = Counter(e["endpoint"] for e in events if e.get("endpoint", None))
    return dict(counts)


def get_time_series(events: List[AuditEvent]) -> Dict[str, int]:
    days: Dict[str, int] = defaultdict(int)
    for e in events:
        if e.get("timestamp", None):
            day = e["timestamp"][:10]
            days[day] += 1
    return dict(sorted(days.items()))


def export_csv() -> str:
    logfile = "distribution/legal_exports/phase9_empire_audit_log.txt"
    try:
        with open(logfile, "r") as f:
            lines = f.readlines()
    except Exception:
        return ""
    events = [parse_line(l) for l in lines]
    events = [e for e in events if e]
    # CSV header
    rows = ["timestamp,key,action,endpoint"]
    for e in events:
        rows.append(f"{e['timestamp']},{e['key']},{e['action']},{e['endpoint']}")
    return "\n".join(rows)
