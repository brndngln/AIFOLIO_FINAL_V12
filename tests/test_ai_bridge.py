import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import hashlib
from aifolio_empire.ai_bridge import AIBridge, APIKeyManager
from aifolio_empire.utils import InputValidator

class TestAPIKeyManager(unittest.TestCase):
    def setUp(self):
        self.key_manager = APIKeyManager()
        
    def test_api_key_validation(self):
        """Test API key validation and storage."""
        # Valid OpenAI key
        valid_openai_key = "sk-test_1234567890"
        self.key_manager.set_openai_key(valid_openai_key)
        self.assertIsNotNone(self.key_manager.get_openai_key())
        
        # Valid Hugging Face key
        valid_hf_key = "hf_1234567890"
        self.key_manager.set_huggingface_key(valid_hf_key)
        self.assertIsNotNone(self.key_manager.get_huggingface_key())
        
        # Invalid keys
        invalid_keys = [
            "",  # Empty
            "invalid-key",  # Invalid format
            "sk-" * 1000,  # Too long
            123,  # Not a string
        ]
        
        for key in invalid_keys:
            with self.assertRaises(ValueError):
                self.key_manager.set_openai_key(key)
            with self.assertRaises(ValueError):
                self.key_manager.set_huggingface_key(key)
    
    def test_key_expiration(self):
        """Test API key expiration."""
        valid_key = "sk-test_1234567890"
        self.key_manager.set_openai_key(valid_key)
        
        # Key should be valid immediately after setting
        self.assertIsNotNone(self.key_manager.get_openai_key())
        
        # Mock time to be 1 hour and 1 minute in the future
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.now() + timedelta(hours=1, minutes=1)
            with self.assertRaises(ValueError):
                self.key_manager.get_openai_key()

class TestAIBridge(unittest.TestCase):
    def setUp(self):
        self.bridge = AIBridge()
        
    def test_secure_api_key(self):
        """Test secure API key hashing."""
        key = "sk-test_1234567890"
        hashed_key = secure_api_key(key, 'openai')
        self.assertNotEqual(key, hashed_key)
        self.assertEqual(len(hashed_key), 64)  # SHA256 hash length
        
    def test_input_validation(self):
        """Test input validation for generation."""
        valid_prompt = "This is a valid prompt"
        invalid_prompts = [
            "" * 4001,  # Too long
            None,  # Not a string
            123,  # Not a string
        ]
        
        for prompt in invalid_prompts:
            with self.assertRaises(ValueError):
                self.bridge._generate_with_openai(prompt, 100, 0.7)
                
    def test_rate_limiting(self):
        """Test rate limiting."""
        # Mock rate limiter to always block
        with patch('aifolio_empire.ai_bridge.openai_rate_limiter') as mock_limiter:
            mock_limiter.side_effect = Exception("Rate limit exceeded")
            with self.assertRaises(Exception):
                self.bridge._generate_with_openai("Test prompt", 100, 0.7)
                
    def test_response_validation(self):
        """Test response validation."""
        # Mock OpenAI response
        with patch('openai.ChatCompletion.create') as mock_create:
            # Valid response
            mock_create.return_value = MagicMock(
                choices=[MagicMock(message=MagicMock(content="Valid response"))]
            )
            response = self.bridge._generate_with_openai("Test prompt", 100, 0.7)
            self.assertIn("text", response)
            
            # Invalid response - no choices
            mock_create.return_value = MagicMock(choices=[])
            with self.assertRaises(ValueError):
                self.bridge._generate_with_openai("Test prompt", 100, 0.7)
                
            # Invalid response - too long
            mock_create.return_value = MagicMock(
                choices=[MagicMock(message=MagicMock(content="a" * 8001))]
            )
            with self.assertRaises(ValueError):
                self.bridge._generate_with_openai("Test prompt", 100, 0.7)
                
    def test_error_handling(self):
        """Test error handling."""
        # Mock API error
        with patch('openai.ChatCompletion.create') as mock_create:
            mock_create.side_effect = Exception("API error")
            with self.assertRaises(Exception):
                self.bridge._generate_with_openai("Test prompt", 100, 0.7)
                
        # Mock invalid temperature
        with self.assertRaises(ValueError):
            self.bridge._generate_with_openai("Test prompt", 100, -0.1)
            
        with self.assertRaises(ValueError):
            self.bridge._generate_with_openai("Test prompt", 100, 1.1)
                
    def test_logging(self):
        """Test logging in API calls."""
        with patch('logging.Logger.info') as mock_info:
            self.bridge._generate_with_openai("Test prompt", 100, 0.7)
            mock_info.assert_called()
            
        with patch('logging.Logger.error') as mock_error:
            with self.assertRaises(Exception):
                self.bridge._generate_with_openai(None, 100, 0.7)
            mock_error.assert_called()

class TestInputValidator(unittest.TestCase):
    def test_validate_niche(self):
        """Test niche validation."""
        valid_niches = [
            "digital marketing",
            "AI programming",
            "web3 development"
        ]
        
        for niche in valid_niches:
            self.assertTrue(InputValidator.validate_niche(niche))
            
        invalid_niches = [
            "",  # Empty
            "invalid@niche",  # Invalid characters
            "a" * 101,  # Too long
            123,  # Not a string
        ]
        
        for niche in invalid_niches:
            with self.assertRaises(ValueError):
                InputValidator.validate_niche(niche)
    
    def test_validate_api_key(self):
        """Test API key validation."""
        valid_keys = [
            ("sk-1234567890", "openai"),
            ("hf_1234567890", "huggingface")
        ]
        
        for key, provider in valid_keys:
            self.assertTrue(InputValidator.validate_api_key(key, provider))
            
        invalid_keys = [
            ("invalid-key", "openai"),
            ("invalid-key", "huggingface"),
            ("sk-1234567890", "invalid"),
            (123, "openai")  # Not a string
        ]
        
        for key, provider in invalid_keys:
            with self.assertRaises(ValueError):
                InputValidator.validate_api_key(key, provider)

if __name__ == '__main__':
    unittest.main()
