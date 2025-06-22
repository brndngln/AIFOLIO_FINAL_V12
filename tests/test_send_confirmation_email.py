import os
import unittest
from autonomy.post_sale_hooks.send_confirmation_email import send_confirmation_email

class TestSendConfirmationEmail(unittest.TestCase):
    def test_stub_no_sendgrid(self):
        os.environ.pop('SENDGRID_API_KEY', None)
        send_confirmation_email('test@example.com', 'TestVault')
        # Should print stub message, not raise

    def test_sendgrid_invalid(self):
        os.environ['SENDGRID_API_KEY'] = 'invalid_key'
        os.environ['SENDGRID_FROM_EMAIL'] = 'noreply@aifolio.com'
        send_confirmation_email('test@example.com', 'TestVault')
        # Should log error, not raise

if __name__ == '__main__':
    unittest.main()
