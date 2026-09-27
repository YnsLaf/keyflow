import random
import unittest

from tipptrainer import textgen


class TextgenTest(unittest.TestCase):
    def setUp(self):
        self.rng = random.Random(42)

    def test_word_source_count(self):
        src = textgen.WordSource("de", rng=self.rng)
        self.assertEqual(len(src.text(25).split()), 25)

    def test_punctuation_ends_with_sentence_mark(self):
        for seed in range(30):
            src = textgen.WordSource("en", punctuation=True, rng=random.Random(seed))
            text = src.text(15)
            self.assertTrue(text[0].isupper() or text[0] in "\"(")
            self.assertIn(text[-1], ".?!")

    def test_difficulty_filters_length(self):
        self.assertTrue(all(len(w) <= 5 for w in textgen.word_pool("de", "easy")))
        self.assertTrue(all(len(w) >= 6 for w in textgen.word_pool("en", "hard")))

    def test_sources_produce_printable_text(self):
        sources = [
            textgen.SentenceSource("de", rng=self.rng),
            textgen.SentenceSource("en", rng=self.rng),
            textgen.NumberSource("de", rng=self.rng),
            textgen.NumberSource("en", rng=self.rng),
            textgen.SymbolSource("de", rng=self.rng),
            textgen.MixedSource("de", rng=self.rng),
            textgen.WeakSource("de", ["ö", "q", "7", ";"], rng=self.rng),
            textgen.WeakSource("en", [], rng=self.rng),
        ]
        for src in sources:
            for _ in range(50):
                text = src.chunk()
                self.assertTrue(text)
                self.assertTrue(text.isprintable(), text)
                self.assertNotIn("  ", text)

    def test_weak_source_prefers_weak_letters(self):
        src = textgen.WeakSource("de", ["ü"], rng=self.rng)
        words = [src.token() for _ in range(50)]
        self.assertTrue(all("ü" in w.lower() for w in words))

    def test_normalize_and_umlauts(self):
        self.assertEqual(textgen.normalize_text("„Hallo“ –  Welt…\n\tneu"), '"Hallo" - Welt... neu')
        self.assertEqual(textgen.finalize("Größe", {"umlauts": False}), "Groesse")
        self.assertEqual(textgen.finalize("Größe", {"umlauts": True}), "Größe")

    def test_quotes_by_length(self):
        text, _ = textgen.pick_quote("de", "short", self.rng)
        self.assertLess(len(text), 80)
        text, _ = textgen.pick_quote("en", "long", self.rng)
        self.assertGreaterEqual(len(text), 200)

    def test_custom_chunks_cover_whole_text(self):
        text = " ".join("Das ist Satz Nummer %d." % i for i in range(200))
        pos, pieces = 0, []
        while True:
            start, end = textgen.custom_chunk(text, pos)
            pieces.append(text[start:end].strip())
            if end >= len(text):
                break
            self.assertGreater(end, start)
            pos = end
        self.assertEqual(" ".join(pieces), text)
        self.assertEqual(textgen.custom_chunk("kurz", 0), (0, 4))


if __name__ == "__main__":
    unittest.main()
