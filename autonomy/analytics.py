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

def get_analytics(filters=None, search=None, time_range=None):
    logfile = "distribution/legal_exports/phase9_empire_audit_log.txt"
    try:
        with open(logfile, "r") as f:
            lines = f.readlines()
    except Exception:
        return {}
    events = [parse_line(l) for l in lines]
    events = [e for e in events if e]
    from autonomy.key_management import load_keys
    key_roles = load_keys()
    # Time range filtering
    if time_range:
        start, end = time_range
        events = [e for e in events if e.get('timestamp') and start <= e['timestamp'] <= end]
    # Regex or substring search
    if search:
        import re
        if search.get('regex'):
            pat = re.compile(search['regex'])
            events = [e for e in events if any(pat.search(str(v)) for v in e.values())]
        elif search.get('substring'):
            sub = search['substring']
            events = [e for e in events if any(sub in str(v) for v in e.values())]
    # Advanced filtering
    if filters:
        events = filter_events(events, filters)
    # Analytics breakdowns
    total_calls = len(events)
    unique_keys = len(set(e['key'] for e in events if e['key']))
    most_active_key = Counter(e['key'] for e in events if e['key']).most_common(1)
    most_active_key = most_active_key[0][0] if most_active_key else None
    most_used_endpoint = Counter(e['endpoint'] for e in events if e['endpoint']).most_common(1)
    most_used_endpoint = most_used_endpoint[0][0] if most_used_endpoint else None
    calls_by_role = defaultdict(int)
    for e in events:
        role = key_roles.get(e['key'], 'unknown')
        calls_by_role[role] += 1
    now = datetime.datetime.now()
    last_24h_calls = sum(1 for e in events if e['timestamp'] and (now - datetime.datetime.fromisoformat(e['timestamp'])).total_seconds() < 86400)
    # Per-key, per-endpoint, per-role, per-status breakdowns
    per_key = get_per_key_endpoint_breakdown(events, key_roles)
    per_role = get_per_role_endpoint_breakdown(events, key_roles)
    per_status = get_per_status_breakdown(events)
    error_rate = get_error_rate(events)
    latency_stats = get_latency_stats(events)
    return {
        'total_calls': total_calls,
        'unique_keys': unique_keys,
        'most_active_key': most_active_key,
        'most_used_endpoint': most_used_endpoint,
        'calls_by_role': dict(calls_by_role),
        'last_24h_calls': last_24h_calls,
        'endpoint_breakdown': get_endpoint_breakdown(events),
        'time_series': get_time_series(events),
        'per_key_endpoint_breakdown': per_key,
        'per_role_endpoint_breakdown': per_role,
        'per_status_breakdown': per_status,
        'error_rate': error_rate,
        'latency_stats': latency_stats,
        'role_time_series': get_role_time_series(events, key_roles),
        'events': events  # for export/search
    }

def get_per_role_endpoint_breakdown(events, key_roles):
    result = {}
    for e in events:
        role = key_roles.get(e.get('key'), 'unknown')
        ep = e.get('endpoint')
        if role and ep:
            if role not in result:
                result[role] = {}
            result[role][ep] = result[role].get(ep, 0) + 1
    return result

def get_per_status_breakdown(events):
    result = {}
    for e in events:
        status = e.get('status')
        ep = e.get('endpoint')
        if status and ep:
            if status not in result:
                result[status] = {}
            result[status][ep] = result[status].get(ep, 0) + 1
    return result

def get_error_rate(events):
    total = len(events)
    errors = sum(1 for e in events if str(e.get('status','')).startswith('4') or str(e.get('status','')).startswith('5'))
    return {'error_count': errors, 'error_rate': errors/total if total else 0}

def get_latency_stats(events):
    from statistics import mean, median, quantiles
    result = {}
    for ep in set(e.get('endpoint') for e in events if e.get('endpoint')):
        latencies = [float(e['latency']) for e in events if e.get('endpoint')==ep and e.get('latency')]
        if latencies:
            result[ep] = {
                'min': min(latencies),
                'max': max(latencies),
                'avg': mean(latencies),
                'median': median(latencies),
                'p95': quantiles(latencies, n=100)[94] if len(latencies)>=20 else None
            }
    return result

def export_events_csv(events):
    import csv
    import io
    if not events:
        return ''
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=sorted(events[0].keys()))
    writer.writeheader()
    for e in events:
        writer.writerow(e)
    return output.getvalue()

def export_events_json(events):
    import json
    return json.dumps(events, indent=2)

def generate_compliance_report(events):
    # Returns a dict summarizing compliance-relevant stats
    error_rate = get_error_rate(events)
    return {
        'total_events': len(events),
        'error_rate': error_rate,
        'unique_keys': len(set(e['key'] for e in events if e.get('key'))),
        'unique_endpoints': len(set(e['endpoint'] for e in events if e.get('endpoint'))),
        'time_range': (events[0]['timestamp'], events[-1]['timestamp']) if events else (None, None)
    }

def filter_events(events, filters):
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

def get_per_key_endpoint_breakdown(events, key_roles):
    result = {}
    for e in events:
        k = e.get('key')
        ep = e.get('endpoint')
        if k and ep:
            if k not in result:
                result[k] = {}
            result[k][ep] = result[k].get(ep, 0) + 1
    return result

def get_role_time_series(events, key_roles):
    days = {}
    for e in events:
        if e.get('timestamp') and e.get('key'):
            role = key_roles.get(e['key'], 'unknown')
            day = e['timestamp'][:10]
            if day not in days:
                days[day] = {}
            days[day][role] = days[day].get(role, 0) + 1
    return days

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
