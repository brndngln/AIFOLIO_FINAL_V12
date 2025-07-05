import asyncio
from functools import wraps
from autonomy.security.ai_safety_layer import anti_static_guard

# Decorator to guard any function returning user-facing AI text
# Handles both sync and async functions


def safe_ai_guarded(func):
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        _scan_result(result)
        return result

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        _scan_result(result)
        return result

    def _scan_result(val):
        if isinstance(val, str):
            if not anti_static_guard(val):
                raise Exception(
                    "AI safety violation: Unsafe sentience/agency patterns detected in output."
                )
        elif isinstance(val, dict):
            for v in val.values():
                _scan_result(v)
        elif isinstance(val, list):
            for v in val:
                _scan_result(v)
        # Optionally, add tuple, set, etc. as needed

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
