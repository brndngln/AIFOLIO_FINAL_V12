"""
AIFOLIO SAFE AI Segment Comparison Reports
- Compares aggregate stats for niches/categories (static)
"""
def segment_comparison(segments):
    # Expects: list of {'segment': str, 'value': int}
    return sorted(segments, key=lambda s: s['value'], reverse=True)
