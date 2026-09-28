import unittest

from keyflow import i18n, keyboard, ui


class KeyboardTest(unittest.TestCase):
    def test_letters_and_shift_use_opposite_hand(self):
        i18n.set_language("de")
        keys, hint = keyboard.keys_for("A", "de")
        self.assertEqual(keys, {"a", "shift_r"})
        self.assertIn("linker kleiner Finger", hint)
        i18n.set_language("en")
        self.assertIn("left pinky", keyboard.keys_for("A", "de")[1])
        keys, _ = keyboard.keys_for("J", "de")
        self.assertEqual(keys, {"j", "shift_l"})

    def test_space_and_symbols(self):
        self.assertEqual(keyboard.keys_for(" ", "de")[0], {" "})
        self.assertEqual(keyboard.keys_for("?", "de")[0], {"ß", "shift_l"})
        self.assertEqual(keyboard.keys_for(":", "en")[0], {";", "shift_l"})
        self.assertEqual(keyboard.keys_for("é", "de")[0], set())

    def test_every_layout_key_has_a_finger(self):
        for lang in ("de", "en"):
            for row, fingers in zip(keyboard.ROWS[lang], keyboard.FINGERS[lang]):
                self.assertEqual(len(row), len(fingers), row)

    def test_layout_keys_do_not_overlap(self):
        for lang in ("de", "en"):
            for row in keyboard.layout(lang):
                end = 0
                for x, _, _, width in row:
                    self.assertGreaterEqual(x, end, (lang, row))
                    end = x + width
                self.assertLessEqual(end, 45)


class ColorTest(unittest.TestCase):
    def test_dark_grays_stay_gray(self):
        self.assertGreaterEqual(ui.rgb_to_256((38, 42, 50)), 232)
        self.assertEqual(ui.rgb_to_256((255, 0, 0)), 196)


if __name__ == "__main__":
    unittest.main()
