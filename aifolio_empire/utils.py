import time
import logging
from functools import wraps
from typing import Callable, Any
import re
from threading import Lock


class RateLimiter:
    """Rate limiter implementation."""

    def __init__(self, max_calls: int, period: float):
        """Initialize rate limiter."""
        self.max_calls = max_calls
        self.period = period
        self.calls: list[float] = []
        self.lock = Lock()

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator to apply rate limiting."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with self.lock:
                # Remove old calls
                now = time.time()
                self.calls = [call for call in self.calls if now - call <= self.period]

                # Check if we can make another call
                if len(self.calls) >= self.max_calls:
                    wait_time = self.period - (now - self.calls[0])
                    logging.warning(f"Rate limit hit, waiting {wait_time:.2f}s")
                    time.sleep(wait_time)

                # Add this call
                self.calls.append(now)

            return func(*args, **kwargs)

        return wrapper


class InputValidator:
    """Input validation utilities."""

    @staticmethod
    def validate_niche(niche: str) -> bool:
        """Validate niche name."""
        if not isinstance(niche, str):
            raise ValueError("Niche must be a string")

        if not re.match(r"^[a-zA-Z0-9\s-]+$", niche):
            raise ValueError(
                "Niche can only contain letters, numbers, spaces, and hyphens"
            )

        if len(niche) < 3 or len(niche) > 100:
            raise ValueError("Niche must be between 3 and 100 characters")

        return True

    @staticmethod
    def validate_api_key(api_key: str, provider: str) -> bool:
        """Validate API key format. Returns False for any invalid key or provider."""
        if not isinstance(api_key, str):
            return False
        if provider.lower() == "openai" and not api_key.startswith("sk-"):
            return False
        if provider.lower() == "huggingface" and not api_key.startswith("hf_"):
            return False
        if provider.lower() not in ("openai", "huggingface"):
            return False
        return True

    @staticmethod
    def validate_prompt(prompt: str) -> bool:
        """Validate prompt format. Returns True for valid prompt, False otherwise."""
        if not isinstance(prompt, str):
            return False
        if not prompt.strip():
            return False
        if len(prompt) > 4000:
            return False
        return True


def api_error_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to handle external API errors."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"API error: {str(e)}")
            # OpenAI error handling (only if openai.error exists)
            openai_error = getattr(
                getattr(__import__("openai"), "error", None), "APIError", None
            )
            if openai_error and isinstance(e, openai_error):
                logging.error(f"OpenAI API error: {getattr(e, 'user_message', str(e))}")
                raise ValueError("OpenAI API request failed") from e
            # Generic Hugging Face or other API error
            logging.error(f"External API error: {str(e)}")
            raise ValueError("External API request failed") from e

    return wrapper
