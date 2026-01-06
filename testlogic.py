import unittest
from etl import format_name, split_email_data

class TestLogic(unittest.TestCase):
    def test_name_formatting(self):
        # Checks if 'malisha' becomes 'Malisha'
        self.assertEqual(format_name("  malisha tandukar  "), "Malisha Tandukar")

    def test_email_splitting(self):
        # Checks if username and domain are separated
        user, domain = split_email_data("TEST@Gmail.com")
        self.assertEqual(user, "test")
        self.assertEqual(domain, "gmail.com")

if __name__ == "__main__":
    unittest.main()