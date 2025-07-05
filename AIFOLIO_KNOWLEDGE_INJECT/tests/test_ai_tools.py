import unittest
from autonomy.ai_tools import vault_formatter, review_analyzer, audit_compliance


class TestVaultFormatter(unittest.TestCase):
    def test_format_title(self):
        self.assertEqual(
            vault_formatter.format_title("the quick brown fox"), "The Quick Brown Fox"
        )
        self.assertEqual(
            vault_formatter.format_title("  a tale of two cities  "),
            "A Tale of Two Cities",
        )
        self.assertEqual(vault_formatter.format_title(""), "")

    def test_format_description(self):
        self.assertEqual(
            vault_formatter.format_description("hello world"), "Hello world."
        )
        self.assertEqual(
            vault_formatter.format_description("Already good."), "Already good."
        )
        self.assertEqual(vault_formatter.format_description(""), "")


class TestReviewAnalyzer(unittest.TestCase):
    def test_analyze_review_spelling(self):
        out = review_analyzer.analyze_review("Th1s is g00d!")
        self.assertIn("spelling", out["flags"])

    def test_analyze_review_banned(self):
        out = review_analyzer.analyze_review("This is a scam and fraud!")
        self.assertIn("banned", out["flags"])

    def test_analyze_review_sentiment(self):
        out = review_analyzer.analyze_review("This is bad and awful")
        self.assertIn("negative", out["flags"])


class TestAuditCompliance(unittest.TestCase):
    def test_vault_registry_entry_required_fields(self):
        """
        Ensure all required fields are present in a vault registry entry and compliance checker flags missing/invalid fields.
        """
        # Simulate a complete registry entry
        complete_entry = {
            "vault_id": "v_test",
            "title": "Test Vault",
            "description": "A vault for testing.",
            "niche": "testing",
            "creator_email": "test@example.com",
            "created_at": "2025-01-01",
            "icon": "🧪",
            "component": "TEST_COMPONENT",
            "event_types": ["VAULT_CREATED"],
            "compliance_profile": "global",
            "notification_channels": ["email"],
            "founder_controlled": False,
        }
        # Should be compliant
        out = audit_compliance.check_vault_metadata(complete_entry)
        self.assertTrue(out["compliant"])
        # Remove 'niche' and check
        entry_missing_niche = complete_entry.copy()
        del entry_missing_niche["niche"]
        out2 = audit_compliance.check_vault_metadata(entry_missing_niche)
        self.assertIn("niche", out2.get("missing", []))
        self.assertFalse(out2["compliant"])
        # Remove 'description' and check
        entry_missing_desc = complete_entry.copy()
        del entry_missing_desc["description"]
        out3 = audit_compliance.check_vault_metadata(entry_missing_desc)
        self.assertIn("description", out3.get("missing", []))
        self.assertFalse(out3["compliant"])

    def test_check_vault_metadata_compliant(self):
        meta = {
            "vault_id": "v1",
            "title": "T",
            "description": "D",
            "creator_email": "a@b.com",
            "created_at": "2025-01-01",
            "niche": "test-niche",
        }
        out = audit_compliance.check_vault_metadata(meta)
        self.assertTrue(out["compliant"])

    def test_check_vault_metadata_missing(self):
        meta = {
            "vault_id": "v1",
            "title": "",
            "description": "D",
            "creator_email": "a@b.com",
            "created_at": "2025-01-01",
        }
        out = audit_compliance.check_vault_metadata(meta)
        self.assertIn("title", out["missing"])
        self.assertFalse(out["compliant"])

    def test_check_vault_metadata_invalid(self):
        meta = {
            "vault_id": "v1",
            "title": "T",
            "description": "D",
            "creator_email": "notanemail",
            "created_at": "2025-01-01",
        }
        out = audit_compliance.check_vault_metadata(meta)
        self.assertIn("creator_email", out["invalid"])
        self.assertFalse(out["compliant"])


if __name__ == "__main__":
    unittest.main()
