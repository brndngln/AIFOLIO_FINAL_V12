from typing import Dict, Any, Optional
import logging


class ConfigManager:
    """Configuration manager with proper validation."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize with configuration dictionary."""
        self._config = config
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate configuration values."""
        # Validate API keys
        if not self._config.get("OPENAI_API_KEY") and not self._config.get(
            "HUGGINGFACE_API_KEY"
        ):
            raise ValueError("At least one API key must be configured")

        # Validate numeric values
        if not 1 <= self._config.get("MAX_CONCURRENT", 5) <= 50:
            raise ValueError("MAX_CONCURRENT must be between 1 and 50")

        if not 30 <= self._config.get("CACHE_TTL", 300) <= 3600:
            raise ValueError("CACHE_TTL must be between 30s and 1h")

        if not 500 <= self._config.get("MEMORY_LIMIT", 1000) <= 5000:
            raise ValueError("MEMORY_LIMIT must be between 500 and 5000")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get a configuration value with optional default."""
        return self._config.get(key, default)

    def validate_api_keys(self) -> bool:
        """Validate API key formats."""
        openai_key = self._config.get("OPENAI_API_KEY")
        huggingface_key = self._config.get("HUGGINGFACE_API_KEY")

        if openai_key and not openai_key.startswith("sk-"):
            logging.warning("OpenAI API key doesn't match expected format")
            return False

        if huggingface_key and not huggingface_key.startswith("hf_"):
            logging.warning("Hugging Face API key doesn't match expected format")
            return False

        return True

    def as_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return self._config.copy()
