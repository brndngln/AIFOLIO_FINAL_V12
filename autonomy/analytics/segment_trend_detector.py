"""
AIFOLIO SAFE AI Segment Trend Detector (static, non-sentient)
- Detects static sales trends (rise/fall) for segments
- No prediction, only raw stats
"""
def detect_trend(segment_stats):
    # Expects segment_stats as list of (date, value)
    if len(segment_stats) < 2:
        return "No trend data."
    if segment_stats[-1][1] > segment_stats[0][1]:
        return "Rising"
    elif segment_stats[-1][1] < segment_stats[0][1]:
        return "Falling"
    return "Stable"
