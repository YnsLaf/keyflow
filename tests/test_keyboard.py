import unittest

from keyflow import keyboard, ui


class KeyboardTest(unittest.TestCase):
    def test_letters_and_shift_use_opposite_hand(self):
        keys, hint = keyboard.keys_for("A", "de")
        self.assertEqual(keys, {"a", "shift_r"})
        self.assertIn("linker kleiner Finger", hint)
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

    def test_layout_rows_have_equal_width(self):
        for lang in ("de", "en"):
            widths = [sum(w + 1 for _, _, w in row) for row in keyboard.layout(lang)[:4]]
            self.assertEqual(len(set(widths)), 1, (lang, widths))


class ColorTest(unittest.TestCase):
    def test_dark_grays_stay_gray(self):
        self.assertGreaterEqual(ui.rgb_to_256((38, 42, 50)), 232)
        self.assertEqual(ui.rgb_to_256((255, 0, 0)), 196)


if __name__ == "__main__":
    unittest.main()
