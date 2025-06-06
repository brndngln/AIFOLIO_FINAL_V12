import time
import logging
from functools import wraps
from typing import Callable, Any, Optional
import re
from datetime import datetime, timedelta
from threading import Lock

class RateLimiter:
    """Rate limiter implementation."""
    
    def __init__(self, max_calls: int, period: float):
        """Initialize rate limiter."""
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = Lock()
    
    def __call__(self, func: Callable) -> Callable:
        """Decorator to apply rate limiting."""
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
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
            
        if not re.match(r'^[a-zA-Z0-9\s-]+$', niche):
            raise ValueError("Niche can only contain letters, numbers, spaces, and hyphens")
            
        if len(niche) < 3 or len(niche) > 100:
            raise ValueError("Niche must be between 3 and 100 characters")
            
        return True
    
    @staticmethod
    def validate_api_key(api_key: str, provider: str) -> bool:
        """Validate API key format."""
        if not isinstance(api_key, str):
            raise ValueError("API key must be a string")
            
        if provider.lower() == 'openai' and not api_key.startswith('sk-'):
            raise ValueError("Invalid OpenAI API key format")
            
        if provider.lower() == 'huggingface' and not api_key.startswith('hf_'):
            raise ValueError("Invalid Hugging Face API key format")
            
        return True
    
    @staticmethod
    def validate_prompt(prompt: str) -> bool:
        """Validate prompt content."""
        if not isinstance(prompt, str):
            raise ValueError("Prompt must be a string")
            
        if len(prompt) > 4000:  # Maximum token limit for most models
            raise ValueError("Prompt is too long")
            
        return True

def api_error_handler(func: Callable) -> Callable:
    """Decorator to handle external API errors."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"API error: {str(e)}")
            # Add specific error handling for different API providers
            if isinstance(e, openai.error.APIError):
                logging.error(f"OpenAI API error: {e.user_message}")
                raise ValueError("OpenAI API request failed") from e
            elif isinstance(e, Exception):  # Add specific Hugging Face error handling
                logging.error(f"Hugging Face API error: {str(e)}")
                raise ValueError("Hugging Face API request failed") from e
            raise
    
    return wrapper
