import os
import unittest
from unittest.mock import patch
from autonomy.post_sale_hooks.push_to_dashboard_analytics import (
    push_to_dashboard_analytics,
)


class TestPushToDashboardAnalytics(unittest.TestCase):
    @patch("requests.post")
    def test_dashboard_api_success(self, mock_post):
        mock_post.return_value.status_code = 200
        os.environ["DASHBOARD_ANALYTICS_URL"] = "http://fake/dashboard"
        push_to_dashboard_analytics("order1")
        del os.environ["DASHBOARD_ANALYTICS_URL"]

    def test_log_only(self):
        if "DASHBOARD_ANALYTICS_URL" in os.environ:
            del os.environ["DASHBOARD_ANALYTICS_URL"]
        push_to_dashboard_analytics("order2")


if __name__ == "__main__":
    unittest.main()
