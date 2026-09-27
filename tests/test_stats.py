import tempfile
import unittest
from datetime import date
from pathlib import Path

from keyflow import stats
from keyflow.storage import Store


def entry(ts, mode="zeit-30-de", wpm=50.0, acc=95.0, duration=30.0, chars=250, lang="de"):
    return {"ts": ts, "mode": mode, "label": mode, "wpm": wpm, "acc": acc,
            "duration": duration, "chars": chars, "errors": 3, "lang": lang}


class StreakTest(unittest.TestCase):
    def test_streaks(self):
        days = {date(2026, 9, d): 60 for d in (1, 2, 3, 10, 11, 26, 27)}
        self.assertEqual(stats.streaks(days, date(2026, 9, 27)), (2, 3))
        # gestern geübt, heute noch nicht: Serie läuft weiter
        self.assertEqual(stats.streaks(days, date(2026, 9, 28)), (2, 3))
        self.assertEqual(stats.streaks(days, date(2026, 9, 29)), (0, 3))
        self.assertEqual(stats.streaks({}, date(2026, 9, 29)), (0, 0))


class RecordTest(unittest.TestCase):
    def test_records_and_free_mode_minimum(self):
        history = [
            entry("2026-09-01T10:00:00", wpm=40),
            entry("2026-09-02T10:00:00", wpm=60),
            entry("2026-09-03T10:00:00", mode="frei-words-de", wpm=120, duration=10),
            entry("2026-09-03T11:00:00", mode="frei-words-de", wpm=55, duration=300),
        ]
        best = stats.records(history)
        self.assertEqual(best["zeit-30-de"]["wpm"], 60)
        self.assertEqual(best["frei-words-de"]["wpm"], 55)

    def test_mode_sort_key_is_numeric(self):
        keys = ["zeit-120-de", "zeit-15-de", "woerter-10-de", "zeit-30-de"]
        self.assertEqual(sorted(keys, key=stats.mode_sort_key),
                         ["zeit-15-de", "zeit-30-de", "zeit-120-de", "woerter-10-de"])

    def test_weak_keys_merge_case(self):
        ks = {"a": [10, 1], "A": [10, 3], "b": [30, 0], "ö": [20, 5], " ": [100, 50]}
        weak = stats.weak_keys(ks)
        self.assertEqual([w[0] for w in weak], ["ö", "a"])


class AchievementTest(unittest.TestCase):
    def test_achievements(self):
        history = [
            entry("2026-09-25T03:10:00", wpm=55, acc=100, chars=120),
            entry("2026-09-26T10:00:00", mode="zahlen-25-de", wpm=36, acc=96),
            entry("2026-09-27T10:00:00", lang="en", duration=900),
        ]
        got = stats.achieved(history, 15, date(2026, 9, 27))
        for key in ("start", "wpm30", "wpm50", "perfekt", "serie3", "ziel",
                    "zahlen", "eule", "zweisprachig"):
            self.assertIn(key, got)
        self.assertNotIn("wpm70", got)
        self.assertEqual(stats.achieved([], 15, date(2026, 9, 27)), set())


class StoreTest(unittest.TestCase):
    def test_roundtrip_and_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "daten.json"
            store = Store(path)
            store.settings["language"] = "en"
            store.settings["menu"]["time"] = 60
            store.add_result(entry("2026-09-27T10:00:00"), {"a": 5}, {"a": 1})
            again = Store(path)
            self.assertEqual(again.settings["language"], "en")
            self.assertEqual(again.settings["menu"]["time"], 60)
            self.assertEqual(again.key_stats, {"a": [5, 1]})
            self.assertEqual(len(again.history), 1)

    def test_invalid_values_fall_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "daten.json"
            path.write_text('{"settings": {"language": "xx", "strict": 1, "daily_goal": 30}}',
                            encoding="utf-8")
            store = Store(path)
            self.assertEqual(store.settings["language"], "de")
            self.assertIs(store.settings["strict"], False)
            self.assertEqual(store.settings["daily_goal"], 30)

    def test_broken_file_is_moved_away(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "daten.json"
            path.write_text("{kaputt", encoding="utf-8")
            store = Store(path)
            self.assertIsNotNone(store.load_error)
            self.assertTrue((Path(tmp) / "daten.defekt.json").exists())
            self.assertEqual(store.history, [])


if __name__ == "__main__":
    unittest.main()
