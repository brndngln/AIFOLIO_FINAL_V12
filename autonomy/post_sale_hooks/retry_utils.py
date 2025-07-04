import time
import logging
import functools
from typing import Callable

logger = logging.getLogger("post_sale_hooks")

FAILED_HOOKS_LOG = "logs/failed_hooks.log"

def retry_safe_hook(max_attempts=3, backoff_tier='short'):
    """
    Decorator to retry a function with multi-tiered exponential backoff.
    Tiers:
        - short: 1m → 5m → 15m
        - medium: 1h → 2h → 4h
        - int: 1d → 2d
    Logs all failures and attempts to logs/failed_hooks.log.
    Args:
        max_attempts: int, number of attempts
        backoff_tier: str, one of 'short', 'medium', 'int'
    Note:
        Only 'max_attempts' and 'backoff_tier' are valid arguments. 'backoff_factor' is not supported.
    """
    tier_map = {
        'short': [60, 300, 900],
        'medium': [3600, 7200, 14400],
        'int': [86400, 172800]
    }
    delays = tier_map.get(backoff_tier, [60, 300, 900])
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"[HOOK RETRY] {func.__name__} failed on attempt {attempt}: {e}")
                    with open(FAILED_HOOKS_LOG, "a") as f:
                        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {func.__name__} attempt {attempt}/{max_attempts} failed: {e}\n")
                if attempt < max_attempts:
                    delay = delays[min(attempt - 1, len(delays) - 1)]
                    logger.info(f"[HOOK RETRY] {func.__name__} sleeping for {delay} seconds before retry {attempt + 1}")
                    with open(FAILED_HOOKS_LOG, "a") as f:
                        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {func.__name__} sleeping {delay}s before retry {attempt + 1}\n")
                    time.sleep(delay)
                else:
                    with open(FAILED_HOOKS_LOG, "a") as f:
                        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {func.__name__} failed after {max_attempts} attempts. FINAL FAILURE.\n")
        return wrapper
    return decorator
