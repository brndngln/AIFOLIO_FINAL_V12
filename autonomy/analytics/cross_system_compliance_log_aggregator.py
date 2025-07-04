"""
AIFOLIO SAFE AI Cross-System Compliance Log Aggregator
- Static, aggregate, no profiling
"""
def cross_system_compliance_log_aggregator(logs):
    # Expects: list of {'system': str, 'compliance_events': int}
    agg = {}
    for l in logs:
        agg[l['system']] = agg.get(l['system'], 0) + l['compliance_events']
    return {'compliance_aggregate': agg}
