"""
AIFOLIO SAFE AI Segment Reporting
- Shows aggregate trends for niches (static, non-sentient)
"""
def segment_report(segment_stats):
    # Expects: {'segment': str, 'values': [int]}
    if not segment_stats['values']:
        return {'segment': segment_stats['segment'], 'trend': 'no data'}
    trend = 'rising' if segment_stats['values'][-1] > segment_stats['values'][0] else 'falling' if segment_stats['values'][-1] < segment_stats['values'][0] else 'stable'
    return {'segment': segment_stats['segment'], 'trend': trend, 'start': segment_stats['values'][0], 'end': segment_stats['values'][-1]}
