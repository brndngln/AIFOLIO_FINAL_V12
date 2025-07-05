import os
import unittest
from unittest.mock import patch
from autonomy.post_sale_hooks.file_tax_compliance import file_tax_compliance


class TestFileTaxCompliance(unittest.TestCase):
    @patch("requests.post")
    def test_tax_api_success(self, mock_post):
        mock_post.return_value.status_code = 200
        os.environ["TAX_API_URL"] = "http://fakeapi/tax"
        file_tax_compliance.trigger({"order": "test"})
        mock_post.assert_called_once()
        del os.environ["TAX_API_URL"]

    def test_log_only(self):
        if "TAX_API_URL" in os.environ:
            del os.environ["TAX_API_URL"]
        file_tax_compliance.trigger({"order": "test2"})


if __name__ == "__main__":
    unittest.main()
