import unittest

from keyflow import updates


class UpdatesTest(unittest.TestCase):
    def test_versions(self):
        self.assertEqual(updates.parse_version("1.10.2"), (1, 10, 2))
        self.assertTrue(updates.is_newer("1.10.0", "1.9.3"))
        self.assertFalse(updates.is_newer("1.4.0", "1.4.0"))
        self.assertFalse(updates.is_newer("1.3.9", "1.4.0"))

    def test_source_checkout_is_detected(self):
        # Die Tests laufen im Quellcode-Ordner (mit start.py)
        self.assertEqual(updates.install_method(), "source")
        self.assertEqual(updates.update_command_text(), "git pull")

    def test_checker_can_be_turned_off(self):
        checker = updates.UpdateChecker(enabled=False)
        self.assertEqual(checker.status, "off")
        self.assertFalse(checker.available)


if __name__ == "__main__":
    unittest.main()
