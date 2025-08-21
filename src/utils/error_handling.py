"""Error handling utilities for AIFOLIO."""

import logging
import functools
from typing import Any, Callable

class AIFolioError(Exception):
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code or 'UNKNOWN_ERROR'
        super().__init__(self.message)

def handle_errors(default_return: Any = None, log_errors: bool = True):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    logger = logging.getLogger(func.__module__)
                    logger.error(f"Error in {func.__name__}: {str(e)}")
                return default_return
        return wrapper
    return decorator
