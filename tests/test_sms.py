import unittest
from unittest.mock import MagicMock, patch
from src.utils import normalize_phone
from src.services import SMSService


class TestUtils(unittest.TestCase):
    def test_normalize_phone(self):
        # Good cases
        self.assertEqual(normalize_phone("09171234567"), "+639171234567")
        self.assertEqual(normalize_phone("639171234567"), "+639171234567")
        self.assertEqual(normalize_phone("+639171234567"), "+639171234567")
        self.assertEqual(normalize_phone("9171234567"), "+639171234567")

        # Bad/Edge cases - should just clean basic chars or return as is
        self.assertEqual(normalize_phone("123"), "123")
        self.assertEqual(normalize_phone("abc"), "")


class TestSMSService(unittest.TestCase):
    def setUp(self):
        # Reset singleton for testing
        SMSService._instance = None
        self.service = SMSService.get_instance()
        # Mock repo and settings
        self.service.repo = MagicMock()
        self.service.contact_repo = MagicMock()
        self.service.settings = MagicMock()
        self.service.settings.SMS_API_KEY = "test_key"
        self.service.settings.SMS_API_BASE_URL = "http://test-url"

    def test_rate_limit(self):
        # We can mock time.sleep to speed up tests or just test logic
        # For simplicity, let's just ensure it calls sleep if we force time
        with patch("time.sleep") as mock_sleep, patch("time.time") as mock_time:
            # First call sets time
            mock_time.return_value = 1000
            self.service._wait_for_rate_limit()
            mock_sleep.assert_not_called()

            # Second call immediately after (time hasn't changed enough)
            mock_time.return_value = 1005  # 5 seconds later
            self.service._wait_for_rate_limit()
            # Should sleep for roughly 5 seconds (10 - 5)
            mock_sleep.assert_called()

    async def test_send_sms_dry_run(self):
        # Verify dry run doesn't hit API
        result = await self.service.send_sms("09171234567", "Hello", dry_run=True)
        self.assertIn("Dry run success", result)
        self.service.repo.log.assert_not_called()


if __name__ == "__main__":
    unittest.main()
