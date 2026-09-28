"""The typing logic: compares input with the target text and computes the stats.

Deliberately free of input/output so it is easy to test."""

import bisect
import statistics


def wrap(text, width):
    """Wraps text at spaces into lines of at most width characters.

    Returns the start index of every line. The space at the end of a line
    stays part of that line, so every index belongs to exactly one line."""
    width = max(1, width)
    starts = [0]
    start = 0
    while len(text) - start > width:
        cut = text.rfind(" ", start, start + width + 1)
        nxt = cut + 1 if cut > start else start + width
        starts.append(nxt)
        start = nxt
    return starts


class TypingTest:
    def __init__(self, target, strict=False):
        self.target = target
        self.strict = strict
        self.typed = []
        self.marks = []           # True = character typed correctly
        self.correct = 0          # currently correct characters
        self.keystrokes = 0       # all character keystrokes (without backspace)
        self.correct_keystrokes = 0
        self.errors = 0
        self.key_attempts = {}
        self.key_errors = {}
        self.start_time = None
        self.end_time = None
        self.samples = []         # per second: (correct characters, keystrokes)
        self._wrap_cache = None

    # --- State -----------------------------------------------------------
    @property
    def pos(self):
        return len(self.typed)

    @property
    def started(self):
        return self.start_time is not None

    @property
    def finished(self):
        return self.end_time is not None

    def complete(self):
        return self.pos >= len(self.target)

    def extend(self, more):
        self.target += more

    # --- Input ----------------------------------------------------------
    def type_char(self, ch, now):
        """Handles one character. Returns True/False (correct/wrong),
        or None when nothing more can be typed."""
        if self.finished or self.complete():
            return None
        if self.start_time is None:
            self.start_time = now
        expected = self.target[self.pos]
        self.keystrokes += 1
        self.key_attempts[expected] = self.key_attempts.get(expected, 0) + 1
        ok = ch == expected
        if ok:
            self.correct_keystrokes += 1
        else:
            self.errors += 1
            self.key_errors[expected] = self.key_errors.get(expected, 0) + 1
            if self.strict:
                return False
        self.typed.append(ch)
        self.marks.append(ok)
        if ok:
            self.correct += 1
        return ok

    def backspace(self):
        if self.typed and not self.finished:
            self.typed.pop()
            if self.marks.pop():
                self.correct -= 1

    def backspace_word(self):
        while self.typed and self.target[self.pos - 1] == " ":
            self.backspace()
        while self.typed and self.target[self.pos - 1] != " ":
            self.backspace()

    # --- Time & stats --------------------------------------------------
    def elapsed(self, now):
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time is not None else now
        return max(0.0, end - self.start_time)

    def sample(self, now):
        if self.start_time is None or self.finished:
            return
        second = int(self.elapsed(now))
        while len(self.samples) < second:
            self.samples.append((self.correct, self.keystrokes))

    def finish(self, now):
        if self.finished:
            return
        if self.start_time is None:
            self.start_time = now
        self.sample(now)
        self.end_time = now

    def wpm(self, now):
        minutes = self.elapsed(now) / 60
        return self.correct / 5 / minutes if minutes > 0 else 0.0

    def raw_wpm(self, now):
        minutes = self.elapsed(now) / 60
        return self.keystrokes / 5 / minutes if minutes > 0 else 0.0

    def accuracy(self):
        if not self.keystrokes:
            return 100.0
        return 100.0 * self.correct_keystrokes / self.keystrokes

    def words_done(self):
        return self.target.count(" ", 0, self.pos)

    def words_total(self):
        return self.target.count(" ") + 1

    def per_second(self):
        """WPM and raw WPM for every full second."""
        wpm, raw = [], []
        prev_c, prev_k = 0, 0
        for c, k in self.samples:
            wpm.append(max(0, c - prev_c) * 12)
            raw.append(max(0, k - prev_k) * 12)
            prev_c, prev_k = c, k
        return wpm, raw

    def consistency(self):
        _, raw = self.per_second()
        if len(raw) < 2:
            return 100.0
        mean = statistics.mean(raw)
        if mean == 0:
            return 0.0
        cv = statistics.pstdev(raw) / mean
        return max(0.0, 100.0 * (1 - cv))

    def result(self):
        now = self.end_time if self.end_time is not None else 0
        wpm_series, _ = self.per_second()
        return {
            "wpm": round(self.wpm(now), 1),
            "raw": round(self.raw_wpm(now), 1),
            "acc": round(self.accuracy(), 1),
            "duration": round(self.elapsed(now), 1),
            "chars": self.correct,
            "errors": self.errors,
            "keystrokes": self.keystrokes,
            "consistency": round(self.consistency()),
            "wpm_series": wpm_series,
            "key_attempts": dict(self.key_attempts),
            "key_errors": dict(self.key_errors),
        }

    # --- Display -------------------------------------------------------
    def line_starts(self, width):
        key = (len(self.target), width)
        if self._wrap_cache is None or self._wrap_cache[0] != key:
            self._wrap_cache = (key, wrap(self.target, width))
        return self._wrap_cache[1]

    def cursor_line(self, width):
        starts = self.line_starts(width)
        return max(0, bisect.bisect_right(starts, min(self.pos, len(self.target) - 1)) - 1)
