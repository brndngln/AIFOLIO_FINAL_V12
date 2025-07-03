"""
AIFOLIO SAFE AI Drift Detector
- Static, detects drift in static AI outputs
"""
def ai_drift_detector(historical_outputs, current_outputs):
    # Expects: lists of outputs
    drift = [i for i, (h, c) in enumerate(zip(historical_outputs, current_outputs)) if h != c]
    return {'drift_indices': drift}
