import unittest

from tipptrainer import stories, textgen


class StoriesTest(unittest.TestCase):
    def test_ten_stories_per_level(self):
        for level in stories.LEVELS:
            self.assertEqual(len(stories.STORIES[level]), 10, level)

    def test_stories_are_typeable(self):
        for level in stories.LEVELS:
            for title, text in stories.STORIES[level]:
                self.assertEqual(textgen.normalize_text(text), text, title)
                self.assertTrue(text.isprintable(), title)

    def test_difficulty_grows(self):
        def avg_len(level):
            return sum(len(t) for _, t in stories.STORIES[level]) / 10

        lengths = [avg_len(level) for level in stories.LEVELS]
        self.assertEqual(lengths, sorted(lengths))

        def special(level):
            return sum(sum(1 for c in t if not (c.isalpha() or c in " .,"))
                       for _, t in stories.STORIES[level])

        self.assertEqual(special("easy"), 0)
        self.assertLess(special("medium"), special("hard"))
        self.assertLess(special("hard"), special("extreme"))


class EndlessSourceTest(unittest.TestCase):
    def test_level_changes_text(self):
        src = textgen.EndlessSource("de")
        easy = " ".join(src.chunk() for _ in range(20))
        self.assertTrue(all(len(w) <= 5 for w in easy.split()))
        src.level = 8
        self.assertTrue(src.chunk())


if __name__ == "__main__":
    unittest.main()
