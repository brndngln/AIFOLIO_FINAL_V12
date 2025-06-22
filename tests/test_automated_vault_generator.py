import unittest
from unittest.mock import patch
from aifolio_empire.profit_engines.automated_vault_generator import AutomatedVaultGenerator

class TestAutomatedVaultGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = AutomatedVaultGenerator()
        
    def test_generate_plausible_text_valid(self):
        """Test valid text generation."""
        text_types = ['title', 'problem', 'promise', 'cta', 'gumroad_hook', 'gumroad_benefit']
        lengths = ['short', 'medium', 'long']
        
        for text_type in text_types:
            for length in lengths:
                result = self.generator._generate_plausible_text("Test Niche", text_type, length)
                self.assertIsInstance(result, str)
                self.assertIn("Test Niche", result)
                
    def test_generate_plausible_text_invalid_niche(self):
        """Test invalid niche input."""
        invalid_niches = ["", "invalid@niche", "a" * 101, 123]
        
        for niche in invalid_niches:
            with self.assertRaises(ValueError):
                self.generator._generate_plausible_text(niche, "title")
                
    def test_generate_plausible_text_invalid_type(self):
        """Test invalid text type."""
        invalid_types = ["invalid", "", None, 123]
        
        for text_type in invalid_types:
            with self.assertRaises(ValueError):
                self.generator._generate_plausible_text("Test Niche", text_type)
                
    def test_generate_plausible_text_invalid_length(self):
        """Test invalid length parameter."""
        invalid_lengths = ["invalid", "", None, 123]
        
        for length in invalid_lengths:
            with self.assertRaises(ValueError):
                self.generator._generate_plausible_text("Test Niche", "title", length)
                
    def test_generate_simulated_outline(self):
        """Test outline generation."""
        outline = self.generator._generate_simulated_outline("Test Niche")
        self.assertIsInstance(outline, list)
        self.assertTrue(3 <= len(outline) <= 10)  # Based on MAX_OUTLINE_POINTS
        
        # Check that all outline points contain the niche
        for point in outline:
            self.assertIsInstance(point, str)
            self.assertIn("Test Niche", point)
            
    def test_vault_limits(self):
        """Test vault operational limits."""
        from aifolio_empire.profit_engines.automated_vault_generator import VaultConfig
        
        # Test valid limits
        VaultConfig.validate_all()
        
        # Test invalid limits
        with patch.object(VaultConfig, 'MAX_OUTLINE_POINTS', 2):
            with self.assertRaises(ValueError):
                VaultConfig.validate_all()
                
        with patch.object(VaultConfig, 'MAX_CTA_VARIATIONS', 6):
            with self.assertRaises(ValueError):
                VaultConfig.validate_all()
                
        with patch.object(VaultConfig, 'MAX_PDF_PROMPT_SECTIONS', 11):
            with self.assertRaises(ValueError):
                VaultConfig.validate_all()
                
    def test_error_handling(self):
        """Test error handling in text generation."""
        with patch('random.choice', side_effect=Exception("Test error")):
            with self.assertRaises(Exception):
                self.generator._generate_plausible_text("Test Niche", "title")
                
    def test_logging(self):
        """Test logging in text generation."""
        with patch('logging.Logger.info') as mock_info:
            self.generator._generate_plausible_text("Test Niche", "title")
            mock_info.assert_called()
            
        with patch('logging.Logger.error') as mock_error:
            with self.assertRaises(ValueError):
                self.generator._generate_plausible_text(123, "title")
            mock_error.assert_called()

if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()
