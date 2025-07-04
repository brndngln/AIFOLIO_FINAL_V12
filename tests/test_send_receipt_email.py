import os
import unittest
from unittest.mock import patch
from autonomy.post_sale_hooks.send_receipt_email import send_receipt_email

class TestSendReceiptEmail(unittest.TestCase):
    @patch('requests.post')
    def test_sendgrid_success(self, mock_post):
        mock_post.return_value.status_code = 202
        os.environ['SENDGRID_API_KEY'] = 'fakekey'
        send_receipt_email('order1', 'user@example.com')
        del os.environ['SENDGRID_API_KEY']

    def test_log_only(self):
        if 'SENDGRID_API_KEY' in os.environ:
            del os.environ['SENDGRID_API_KEY']
        send_receipt_email('order2', 'user2@example.com')

if __name__ == '__main__':
    unittest.main()
