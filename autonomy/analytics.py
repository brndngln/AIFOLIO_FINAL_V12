"""
Phase 9+ SAFE AI Advanced Analytics (static, SAFE AI compliant)
- Computes analytics from audit log for dashboard analytics panel
- No adaptive logic; all calculations are static
"""
import datetime
import json
from collections import Counter, defaultdict

def parse_line(line):
    # Example: [2025-06-23T18:01:54.123456] API_KEY_USAGE: key=PHASE9SAFEKEY action=access endpoint=/phase9/foo
    if 'API_KEY_USAGE:' not in line:
        return None
    try:
        ts = line.split(']')[0][1:]
        rest = line.split('API_KEY_USAGE: ')[1]
        parts = dict(x.split('=') for x in rest.replace(' endpoint',';endpoint').replace(' action',';action').replace(' key',';key').split(';') if '=' in x)
        return {'timestamp': ts, 'key': parts.get('key'), 'action': parts.get('action'), 'endpoint': parts.get('endpoint')}
    except Exception:
        return None

def get_analytics():
    logfile = "distribution/legal_exports/phase9_empire_audit_log.txt"
    try:
        with open(logfile, "r") as f:
            lines = f.readlines()
    except Exception:
        return {}
    events = [parse_line(l) for l in lines]
    events = [e for e in events if e]
    total_calls = len(events)
    unique_keys = len(set(e['key'] for e in events if e['key']))
    most_active_key = Counter(e['key'] for e in events if e['key']).most_common(1)
    most_active_key = most_active_key[0][0] if most_active_key else None
    most_used_endpoint = Counter(e['endpoint'] for e in events if e['endpoint']).most_common(1)
    most_used_endpoint = most_used_endpoint[0][0] if most_used_endpoint else None
    calls_by_role = defaultdict(int)
    from autonomy.key_management import load_keys
    key_roles = load_keys()
    for e in events:
        role = key_roles.get(e['key'], 'unknown')
        calls_by_role[role] += 1
    now = datetime.datetime.now()
    last_24h_calls = sum(1 for e in events if e['timestamp'] and (now - datetime.datetime.fromisoformat(e['timestamp'])).total_seconds() < 86400)
    return {
        'total_calls': total_calls,
        'unique_keys': unique_keys,
        'most_active_key': most_active_key,
        'most_used_endpoint': most_used_endpoint,
        'calls_by_role': dict(calls_by_role),
        'last_24h_calls': last_24h_calls,
        'endpoint_breakdown': get_endpoint_breakdown(events),
        'time_series': get_time_series(events)
    }

def get_endpoint_breakdown(events):
    counts = Counter(e['endpoint'] for e in events if e and e['endpoint'])
    return dict(counts)

def get_time_series(events):
    days = defaultdict(int)
    for e in events:
        if e and e['timestamp']:
            day = e['timestamp'][:10]
            days[day] += 1
    return dict(sorted(days.items()))

def export_csv():
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
