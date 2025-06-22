import unittest
from autonomy.ai_tools import vault_formatter, review_analyzer, audit_compliance

class TestVaultFormatter(unittest.TestCase):
    def test_format_title(self):
        self.assertEqual(vault_formatter.format_title('the quick brown fox'), 'The Quick Brown Fox')
        self.assertEqual(vault_formatter.format_title('  a tale of two cities  '), 'A Tale of Two Cities')
        self.assertEqual(vault_formatter.format_title(''), '')
    def test_format_description(self):
        self.assertEqual(vault_formatter.format_description('hello world'), 'Hello world.')
        self.assertEqual(vault_formatter.format_description('Already good.'), 'Already good.')
        self.assertEqual(vault_formatter.format_description(''), '')

class TestReviewAnalyzer(unittest.TestCase):
    def test_analyze_review_spelling(self):
        out = review_analyzer.analyze_review('Th1s is g00d!')
        self.assertIn('spelling', out['flags'])
    def test_analyze_review_banned(self):
        out = review_analyzer.analyze_review('This is a scam and fraud!')
        self.assertIn('banned', out['flags'])
    def test_analyze_review_sentiment(self):
        out = review_analyzer.analyze_review('This is bad and awful')
        self.assertIn('negative', out['flags'])

class TestAuditCompliance(unittest.TestCase):
    def test_check_vault_metadata_compliant(self):
        meta = {'vault_id': 'v1', 'title': 'T', 'description': 'D', 'creator_email': 'a@b.com', 'created_at': '2025-01-01'}
        out = audit_compliance.check_vault_metadata(meta)
        self.assertTrue(out['compliant'])
    def test_check_vault_metadata_missing(self):
        meta = {'vault_id': 'v1', 'title': '', 'description': 'D', 'creator_email': 'a@b.com', 'created_at': '2025-01-01'}
        out = audit_compliance.check_vault_metadata(meta)
        self.assertIn('title', out['missing'])
        self.assertFalse(out['compliant'])
    def test_check_vault_metadata_invalid(self):
        meta = {'vault_id': 'v1', 'title': 'T', 'description': 'D', 'creator_email': 'notanemail', 'created_at': '2025-01-01'}
        out = audit_compliance.check_vault_metadata(meta)
        self.assertIn('creator_email', out['invalid'])
        self.assertFalse(out['compliant'])

if __name__ == '__main__':
    unittest.main()
