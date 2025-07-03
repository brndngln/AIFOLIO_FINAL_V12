import os
import unittest
from unittest.mock import patch
from autonomy.post_sale_hooks.request_review import request_review

class TestRequestReview(unittest.TestCase):
    @patch('requests.post')
    def test_sendgrid_success(self, mock_post):
        mock_post.return_value.status_code = 202
        os.environ['SENDGRID_API_KEY'] = 'fakekey'
        request_review.schedule_email('user@example.com', delay_hours=1)
        del os.environ['SENDGRID_API_KEY']

    def test_log_only(self):
        if 'SENDGRID_API_KEY' in os.environ:
            del os.environ['SENDGRID_API_KEY']
        request_review.schedule_email('user2@example.com', delay_hours=1)

if __name__ == '__main__':
    unittest.main()
