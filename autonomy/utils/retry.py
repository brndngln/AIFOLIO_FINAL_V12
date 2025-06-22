import functools
import time

def retry_safe(_func=None, *, max_attempts=3, backoff_factor=0.1):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tries = max_attempts
            delay = backoff_factor
            for i in range(tries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[RETRY] Attempt {i+1} failed: {e}")
                    time.sleep(delay * (2 ** i))
            print(f"[RETRY] All attempts failed for {func.__name__}")
        return wrapper
    if _func is None:
        return decorator_retry
    else:
        return decorator_retry(_func)
