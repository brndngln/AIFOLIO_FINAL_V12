"""Input validation utilities for AIFOLIO."""

import re
from typing import Any

class ValidationError(Exception):
    pass

class InputValidator:
    @staticmethod
    def validate_string(value: Any, max_length: int = 1000) -> str:
        if not isinstance(value, str):
            raise ValidationError(f"Expected string, got {type(value)}")
        if len(value) > max_length:
            raise ValidationError(f"String too long (max {max_length} characters)")
        return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', value).strip()
    
    @staticmethod
    def validate_email(email: str) -> str:
        email = InputValidator.validate_string(email, max_length=254)
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Invalid email format")
        return email.lower()
    
    @staticmethod
    def validate_integer(value: Any, min_value: int = None, max_value: int = None) -> int:
        try:
            value = int(value)
            if min_value is not None and value < min_value:
                raise ValidationError(f"Value must be at least {min_value}")
            if max_value is not None and value > max_value:
                raise ValidationError(f"Value must be at most {max_value}")
            return value
        except ValueError:
            raise ValidationError("Invalid integer format")
