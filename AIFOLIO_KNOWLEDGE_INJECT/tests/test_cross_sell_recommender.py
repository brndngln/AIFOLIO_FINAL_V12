import os
import unittest
from unittest.mock import patch
from autonomy.post_sale_hooks.cross_sell_recommender import cross_sell_recommender


class TestCrossSellRecommender(unittest.TestCase):
    @patch("requests.post")
    def test_sendgrid_success(self, mock_post):
        mock_post.return_value.status_code = 202
        os.environ["SENDGRID_API_KEY"] = "fakekey"
        cross_sell_recommender.recommend_next("user@example.com", "vault1")
        del os.environ["SENDGRID_API_KEY"]

    def test_log_only(self):
        if "SENDGRID_API_KEY" in os.environ:
            del os.environ["SENDGRID_API_KEY"]
        cross_sell_recommender.recommend_next("user2@example.com", "vault2")


if __name__ == "__main__":
    unittest.main()
