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


class GlassProfileTest(unittest.TestCase):
    def test_profile_name_contains_opacity(self):
        from keyflow import macprofile
        self.assertEqual(macprofile.profile_name(0.7), "KeyFlow 70")
        data = macprofile.profile_data((26, 26, 26), 0.7, 120, 30)
        self.assertEqual(data["name"], "KeyFlow 70")
        self.assertTrue(macprofile._is_keyflow_profile("KeyFlow"))
        self.assertTrue(macprofile._is_keyflow_profile("KeyFlow 85"))
        self.assertFalse(macprofile._is_keyflow_profile("Basic"))
