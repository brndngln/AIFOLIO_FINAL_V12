import unittest
from unittest.mock import patch
from aifolio_empire.utils import RateLimiter, InputValidator
import time
from typing import Any


class TestRateLimiter(unittest.TestCase):
    def setUp(self) -> None:
        self.limiter = RateLimiter(max_calls=5, period=1)  # 5 calls per second

    def test_rate_limiting(self) -> None:
        # Test that it allows max_calls in the period
        for _ in range(5):
            self.limiter(lambda: None)()

        # Test that it blocks additional calls
        time.time()
        with patch("time.sleep") as mock_sleep:
            self.limiter(lambda: None)()
            self.assertTrue(mock_sleep.called)

        # Verify sleep duration
        sleep_duration = mock_sleep.call_args[0][0]
        self.assertGreaterEqual(sleep_duration, 0.99)


class TestInputValidator(unittest.TestCase):
    def test_validate_niche(self) -> None:
        # Valid cases
        from typing import Any
        valid_niches: list[str] = ["digital marketing", "AI programming", "web3 development"]
        for niche in valid_niches:
            self.assertTrue(InputValidator.validate_niche(niche))

        # Invalid cases
        invalid_niches: list[Any] = [
            "",  # Too short
            "a" * 101,  # Too long
            "invalid@niche",  # Invalid characters
            123,  # Not a string
        ]
        for niche in invalid_niches:
            if not isinstance(niche, str):
                with self.assertRaises(Exception):
                    InputValidator.validate_niche(str(niche))
            else:
                with self.assertRaises(ValueError):
                    InputValidator.validate_niche(niche)

    def test_validate_api_key(self) -> None:
        # Valid cases
        valid_keys = [("sk-1234567890", "openai"), ("hf_1234567890", "huggingface")]
        for key, provider in valid_keys:
            self.assertTrue(InputValidator.validate_api_key(key, provider))

        # Invalid cases
        invalid_keys: list[tuple[Any, Any]] = [
            ("invalid-key", "openai"),
            ("invalid-key", "huggingface"),
            ("sk-1234567890", "invalid"),
            (123, "openai"),  # Not a string
        ]
        for key, provider in invalid_keys:
            if isinstance(key, str):
                self.assertFalse(InputValidator.validate_api_key(key, provider))
            else:
                with self.assertRaises(Exception):
                    InputValidator.validate_api_key(key, provider)

    def test_validate_prompt(self) -> None:
        # Valid case
        valid_prompt = "This is a test prompt that should be valid."
        self.assertTrue(InputValidator.validate_prompt(valid_prompt))

        # Invalid cases
        invalid_prompts: list[Any] = [
            "" * 4000,  # Too int
            123,  # Not a string
            None,  # Not a string
        ]
        for prompt in invalid_prompts:
            if isinstance(prompt, str):
                self.assertFalse(InputValidator.validate_prompt(prompt))
            else:
                with self.assertRaises(Exception):
                    InputValidator.validate_prompt(prompt)


if __name__ == "__main__":
    unittest.main()
