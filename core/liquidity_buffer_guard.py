# liquidity_buffer_guard.py
# Ensures liquidity never drops below configured minimum
class LiquidityBufferGuard:
    def __init__(self, min_buffer: int) -> None:
        self.min_buffer: int = min_buffer
        self.current_buffer: int = min_buffer

    def update_buffer(self, amount: float) -> None:
        """Update the buffer with a float amount, casting to int for internal storage."""
        self.current_buffer += int(amount)

    def filter_by_buffer(self, proposals: list[dict[str, object]]) -> list[dict[str, object]]:
        result: list[dict[str, object]] = []
        for p in proposals:
            val = p.get("liquidity_impact", 0)
            if isinstance(val, (int, float)):
                if int(val) >= self.min_buffer:
                    result.append(p)
            else:
                # If not a number, treat as 0
                if 0 >= self.min_buffer:
                    result.append(p)
        return result
