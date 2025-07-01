# liquidity_buffer_guard.py
# Ensures liquidity never drops below configured minimum
class LiquidityBufferGuard:
    def __init__(self, min_buffer):
        self.min_buffer = min_buffer
        self.current_buffer = min_buffer
    def update_buffer(self, amount):
        self.current_buffer += amount
    def filter_by_buffer(self, proposals):
        return [p for p in proposals if p.get('liquidity_impact', 0) >= self.min_buffer]
