import os
import unittest
from unittest.mock import patch
from autonomy.post_sale_hooks.notify_internal_channels import notify_internal_channels


class TestNotifyInternalChannels(unittest.TestCase):
    @patch("requests.post")
    def test_slack_success(self, mock_post):
        mock_post.return_value.status_code = 200
        os.environ["SLACK_WEBHOOK_URL"] = "http://fake/slack"
        notify_internal_channels("order1")
        del os.environ["SLACK_WEBHOOK_URL"]

    @patch("requests.post")
    def test_discord_success(self, mock_post):
        mock_post.return_value.status_code = 204
        os.environ["DISCORD_WEBHOOK_URL"] = "http://fake/discord"
        notify_internal_channels("order2")
        del os.environ["DISCORD_WEBHOOK_URL"]

    def test_stub(self):
        if "SLACK_WEBHOOK_URL" in os.environ:
            del os.environ["SLACK_WEBHOOK_URL"]
        if "DISCORD_WEBHOOK_URL" in os.environ:
            del os.environ["DISCORD_WEBHOOK_URL"]
        notify_internal_channels("order3")


if __name__ == "__main__":
    unittest.main()
