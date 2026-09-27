import unittest

from tipptrainer.engine import TypingTest, wrap


class WrapTest(unittest.TestCase):
    def test_lines_cover_text_and_respect_width(self):
        text = "eins zwei drei vier fünf sechs sieben acht neun zehn " * 5
        starts = wrap(text, 20)
        self.assertEqual(starts[0], 0)
        bounds = starts + [len(text)]
        for a, b in zip(bounds, bounds[1:]):
            self.assertLessEqual(len(text[a:b].rstrip(" ")), 20)

    def test_long_word_is_split(self):
        self.assertEqual(wrap("a" * 25, 10), [0, 10, 20])


class TypingTestTest(unittest.TestCase):
    def test_correct_and_wrong_chars(self):
        t = TypingTest("abc")
        self.assertTrue(t.type_char("a", 0.0))
        self.assertFalse(t.type_char("x", 0.5))
        self.assertEqual(t.correct, 1)
        self.assertEqual(t.errors, 1)
        self.assertEqual(t.key_errors, {"b": 1})
        t.backspace()
        self.assertTrue(t.type_char("b", 1.0))
        self.assertTrue(t.type_char("c", 1.5))
        self.assertTrue(t.complete())
        self.assertEqual(t.correct, 3)
        self.assertAlmostEqual(t.accuracy(), 75.0)

    def test_strict_mode_does_not_advance_on_error(self):
        t = TypingTest("ab", strict=True)
        t.type_char("x", 0.0)
        self.assertEqual(t.pos, 0)
        t.type_char("a", 0.1)
        self.assertEqual(t.pos, 1)

    def test_backspace_word(self):
        t = TypingTest("hallo welt")
        for i, ch in enumerate("hallo we"):
            t.type_char(ch, i * 0.1)
        t.backspace_word()
        self.assertEqual(t.pos, 6)
        t.backspace_word()
        self.assertEqual(t.pos, 0)

    def test_wpm(self):
        t = TypingTest("x" * 50)
        for i in range(50):
            t.type_char("x", i * 0.1)
        t.finish(60.0)
        # 50 Zeichen = 10 Wörter in einer Minute
        self.assertAlmostEqual(t.wpm(60.0), 10.0)
        result = t.result()
        self.assertEqual(result["chars"], 50)
        self.assertEqual(len(result["wpm_series"]), 60)

    def test_cursor_line(self):
        t = TypingTest("aaa bbb ccc")
        self.assertEqual(t.cursor_line(4), 0)
        for ch in "aaa b":
            t.type_char(ch, 0)
        self.assertEqual(t.cursor_line(4), 1)


if __name__ == "__main__":
    unittest.main()
