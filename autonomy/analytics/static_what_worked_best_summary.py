"""
AIFOLIO SAFE AI "What Worked Best" Summary Engine (static)
- Summarizes top-performing vaults, segments, campaigns (static only)
- No optimization, no sentience, no adaptive logic
"""
def what_worked_best(stats):
    # Expects: {'vaults': [{'id': str, 'revenue': int}], 'segments': [{'name': str, 'growth': int}]}
    top_vault = max(stats['vaults'], key=lambda v: v['revenue']) if stats.get('vaults') else None
    top_segment = max(stats['segments'], key=lambda s: s['growth']) if stats.get('segments') else None
    return {'top_vault': top_vault, 'top_segment': top_segment}
