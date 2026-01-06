import unittest
from etl import format_name, split_email_data, clean_mobile

class TestLogic(unittest.TestCase):
    def test_name_formatting(self):
        # Checks if 'malisha' becomes 'Malisha'
        self.assertEqual(format_name("  malisha tandukar  "), "Malisha Tandukar")

    def test_email_splitting(self):
        # Checks if username and domain are separated
        user, domain = split_email_data("TEST@Gmail.com")
        self.assertEqual(user, "test")
        self.assertEqual(domain, "gmail.com")

    def test_phone_cleaning(self):
        # 1. Test if it removes special characters and spaces
        self.assertEqual(clean_mobile("984-123 4567"), "9841234567")

        # 2. Test if it raises an error for too many digits (11 digits)
        # with self.assertRaises(ValueError):
        #     clean_mobile("98412345678")

        # 3. Test if it raises an error for letters
        with self.assertRaises(ValueError):
            clean_mobile("984123abcd")

if __name__ == "__main__":
    unittest.main()