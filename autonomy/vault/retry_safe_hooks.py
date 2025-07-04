import time
<<<<<<< HEAD
import logging
=======
>>>>>>> omni_repair_backup_20250704_1335
import functools
# Emma Compliance Lock
OWNER_LOCK = True
import os
<<<<<<< HEAD
import json
=======
>>>>>>> omni_repair_backup_20250704_1335
import datetime

ERROR_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs/error.log'))
os.makedirs(os.path.dirname(ERROR_LOG), exist_ok=True)

def retry_safe_hook(max_attempts=3, backoff=[60, 300, 900]):
    """
    Decorator to retry a function with exponential backoff. Logs all exceptions. Never blocks main vault flow.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts+1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    ts = datetime.datetime.utcnow().isoformat() + 'Z'
                    with open(ERROR_LOG, 'a') as f:
                        f.write(f"[{ts}] {func.__name__} failed attempt {attempt}/{max_attempts}: {e}\n")
                    if attempt < max_attempts:
                        delay = backoff[min(attempt-1, len(backoff)-1)]
                        time.sleep(delay)
                    else:
                        f.write(f"[{ts}] {func.__name__} FINAL FAILURE after {max_attempts} attempts.\n")
        return wrapper
    return decorator
