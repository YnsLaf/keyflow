"""Erzeugt Übungstexte: Wörter, Sätze, Zahlen, Sonderzeichen, Zitate …"""

import random

from . import words as W

_UMLAUTS = str.maketrans({
    "ä": "ae", "ö": "oe", "ü": "ue", "Ä": "Ae", "Ö": "Oe", "Ü": "Ue", "ß": "ss",
})

# Typografische Zeichen, die auf normalen Tastaturen schwer zu tippen sind.
_TYPO = {
    "„": '"', "“": '"', "”": '"', "‚": "'", "‘": "'", "’": "'", "«": '"',
    "»": '"', "‹": "'", "›": "'", "–": "-", "—": "-", "…": "...",
    "\u00a0": " ", "\t": " ",
}


def replace_umlauts(text):
    return text.translate(_UMLAUTS)


def normalize_text(text):
    """Macht einen eingefügten Text tippbar: ein Leerzeichen zwischen Wörtern,
    keine typografischen Anführungszeichen, keine Steuerzeichen."""
    for src, dst in _TYPO.items():
        text = text.replace(src, dst)
    text = "".join(ch if ch.isprintable() else " " for ch in text)
    return " ".join(text.split())


def finalize(text, settings):
    """Wendet Einstellungen an, die für jeden erzeugten Text gelten."""
    if not settings.get("umlauts", True):
        text = replace_umlauts(text)
    return text


def word_pool(lang, difficulty="normal"):
    words = W.GERMAN_WORDS if lang == "de" else W.ENGLISH_WORDS
    if difficulty == "easy":
        pool = [w for w in words if len(w) <= 5]
    elif difficulty == "hard":
        pool = [w for w in words if len(w) >= 6]
    else:
        pool = list(words)
    return pool or list(words)


def _lower_first(text):
    return text[:1].lower() + text[1:]


def _join(*parts):
    return " ".join(p for p in parts if p)


class Source:
    """Liefert Text-Bausteine ("Tokens"). Für feste Tests wird eine bestimmte
    Anzahl geholt, für Zeit- und freie Tests immer neue Stücke (chunk)."""

    chunk_size = 10

    def __init__(self, rng=None):
        self.rng = rng or random.Random()

    def token(self):
        raise NotImplementedError

    def text(self, count):
        return " ".join(self.token() for _ in range(count))

    def chunk(self):
        return " ".join(self.token() for _ in range(self.chunk_size))


class WordSource(Source):
    def __init__(self, lang="de", difficulty="normal", punctuation=False,
                 numbers=False, lowercase=False, rng=None):
        super().__init__(rng)
        self.pool = word_pool(lang, difficulty)
        self.punctuation = punctuation
        self.numbers = numbers
        self.lowercase = lowercase
        self._capitalize_next = punctuation
        self._last = None

    def _pick(self):
        word = self.rng.choice(self.pool)
        if word == self._last and len(self.pool) > 1:
            word = self.rng.choice(self.pool)
        self._last = word
        return word

    def token(self):
        rng = self.rng
        if self.numbers and rng.random() < 0.12:
            word = str(rng.choice((rng.randint(0, 99), rng.randint(100, 999),
                                   rng.randint(1900, 2030))))
        else:
            word = self._pick()
            if self.lowercase:
                word = word.lower()
        if not self.punctuation:
            return word
        if self._capitalize_next:
            word = word[:1].upper() + word[1:]
            self._capitalize_next = False
        r = rng.random()
        if r < 0.08:
            word += "."
            self._capitalize_next = True
        elif r < 0.10:
            word += "?"
            self._capitalize_next = True
        elif r < 0.115:
            word += "!"
            self._capitalize_next = True
        elif r < 0.20:
            word += ","
        elif r < 0.215:
            word += ":"
        elif r < 0.225:
            word += ";"
        elif r < 0.245:
            word = '"' + word + '"'
        elif r < 0.26:
            word = "(" + word + ")"
        elif r < 0.27:
            word += " -"
        return word

    def text(self, count):
        tokens = [self.token() for _ in range(count)]
        if self.punctuation and tokens:
            last = tokens[-1].rstrip(",:;- ")
            if not last.endswith((".", "?", "!")):
                last += "."
            tokens[-1] = last
        return " ".join(tokens)


def german_sentence(rng):
    subject = rng.choice(W.DE_SUBJECTS)
    verb, rest = rng.choice(W.DE_VERBS)
    place = rng.choice(W.DE_PLACES) if rng.random() < 0.6 else ""
    end = "!" if rng.random() < 0.1 else "."
    form = rng.random()
    if form < 0.35:
        return _join(subject, verb, place, rest) + end
    if form < 0.6:
        return _join(rng.choice(W.DE_TIMES), verb, _lower_first(subject), place, rest) + end
    if form < 0.8:
        subject2 = rng.choice(W.DE_SUBJECTS)
        verb2, rest2 = rng.choice(W.DE_VERBS)
        conj = rng.choice(("und", "aber", "denn"))
        return (_join(subject, verb, rest) + ", "
                + _join(conj, _lower_first(subject2), verb2, rest2) + end)
    if form < 0.9:
        return _join(rng.choice(W.DE_QUESTIONS), verb, _lower_first(subject), rest) + "?"
    return _join(verb.capitalize(), _lower_first(subject), place, rest) + "?"


def english_sentence(rng):
    subject = rng.choice(W.EN_SUBJECTS)
    verb, base, rest = rng.choice(W.EN_VERBS)
    place = rng.choice(W.EN_PLACES) if rng.random() < 0.6 else ""
    end = "!" if rng.random() < 0.1 else "."
    form = rng.random()
    if form < 0.35:
        return _join(subject, verb, rest, place) + end
    if form < 0.6:
        return rng.choice(W.EN_TIMES) + ", " + _join(_lower_first(subject), verb, rest, place) + end
    if form < 0.8:
        subject2 = rng.choice(W.EN_SUBJECTS)
        verb2, _, rest2 = rng.choice(W.EN_VERBS)
        conj = rng.choice(("and", "but", "so"))
        return (_join(subject, verb, rest) + ", "
                + _join(conj, _lower_first(subject2), verb2, rest2) + end)
    if form < 0.9:
        return _join(rng.choice(W.EN_QUESTIONS), _lower_first(subject), base, rest) + "?"
    return _join("Does", _lower_first(subject), base, rest, place) + "?"


class SentenceSource(Source):
    chunk_size = 1

    def __init__(self, lang="de", rng=None):
        super().__init__(rng)
        self.lang = lang

    def token(self):
        if self.lang == "de":
            return german_sentence(self.rng)
        return english_sentence(self.rng)


class NumberSource(Source):
    chunk_size = 8

    def __init__(self, lang="de", rng=None):
        super().__init__(rng)
        self.lang = lang

    def token(self):
        rng = self.rng
        de = self.lang == "de"
        dec = "," if de else "."
        kind = rng.randrange(13)
        if kind == 0:
            return str(rng.randint(0, 99))
        if kind == 1:
            return str(rng.randint(100, 99999))
        if kind == 2:
            return "%d%s%02d" % (rng.randint(0, 999), dec, rng.randint(0, 99))
        if kind == 3:
            cents = rng.choice(("99", "49", "95", "00", "%02d" % rng.randint(0, 99)))
            price = "%d%s%s" % (rng.randint(1, 999), dec, cents)
            return price + " €" if de else "$" + price
        if kind == 4:
            return "%d%%" % rng.randint(1, 100)
        if kind == 5:
            return "%02d:%02d" % (rng.randint(0, 23), rng.randint(0, 59))
        if kind == 6:
            d, m, y = rng.randint(1, 28), rng.randint(1, 12), rng.randint(1950, 2035)
            return "%02d.%02d.%d" % (d, m, y) if de else "%02d/%02d/%d" % (m, d, y)
        if kind == 7:
            return str(rng.randint(1800, 2030))
        if kind == 8:
            big = "{:,}".format(rng.randint(1000, 9999999))
            return big.replace(",", ".") if de else big
        if kind == 9:
            a, b = rng.randint(1, 99), rng.randint(1, 99)
            op = rng.choice("+-*")
            result = a + b if op == "+" else a - b if op == "-" else a * b
            return "%d %s %d = %d" % (a, op, b, result)
        if kind == 10:
            amount = str(rng.randint(1, 999)) if rng.random() < 0.6 else \
                "%d%s%d" % (rng.randint(0, 99), dec, rng.randint(1, 9))
            return amount + " " + rng.choice(W.UNITS[self.lang])
        if kind == 11:
            return "-%d" % rng.randint(1, 999)
        if de:
            return "0%d %d" % (rng.randint(151, 179), rng.randint(1000000, 9999999))
        return "(%d) %d-%d" % (rng.randint(200, 999), rng.randint(200, 999),
                               rng.randint(1000, 9999))


class SymbolSource(Source):
    chunk_size = 6

    def __init__(self, lang="de", rng=None):
        super().__init__(rng)
        self.lang = lang

    def token(self):
        rng = self.rng
        a, b = rng.sample(W.IDENTIFIERS, 2)
        n, m = rng.randint(0, 99), rng.randint(1, 9)
        tld = "de" if self.lang == "de" else "com"
        templates = (
            "(" + a + ")", "[" + a + "]", "{" + a + "}", "<" + a + ">",
            '"' + a + '"', "'" + a + "'", "`" + a + "`",
            "#" + a, "@" + a, "$" + a, "%" + a + "%", "&" + a, "*" + a + "*",
            "~" + a, a + "!", a + "?", a + ";", a + ":",
            a + "_" + b, a + "-" + b, a + "/" + b, a + "\\" + b, a + "." + b,
            a + "::" + b, a + "->" + b, a + "|" + b,
            "%s = %d;" % (a, n), "%s += %d;" % (a, m), "%s[%d]" % (a, m),
            "%s(%s)" % (a, b), "%s(%s, %d)" % (a, b, n),
            "if (%s > %d) {" % (a, n), "%s != %s" % (a, b), "%s == %s" % (a, b),
            "%s && %s" % (a, b), "%s || !%s" % (a, b), "%s <= %d" % (a, n),
            "%s >= %d" % (a, m), "%s => %s" % (a, b), "%s^%d" % (a, m),
            "%s %% %d" % (a, m), "%s@%s.%s" % (a, b, tld), "~/%s/%s.txt" % (a, b),
            "C:\\%s\\%s" % (a, b), "https://%s.org/%s?id=%d" % (a, b, n),
            "(%d + %d) * %d" % (n, m, m), "%d%% + %d%%" % (n, m),
            "[]", "{}", "()", "<>", "=>", "->", "!=", "&&", "||", "::",
        )
        return rng.choice(templates)


class MixedSource(Source):
    """Wörter mit Satzzeichen, Großbuchstaben, Zahlen und Sonderzeichen."""

    chunk_size = 10

    def __init__(self, lang="de", difficulty="normal", rng=None):
        super().__init__(rng)
        self.words = WordSource(lang, difficulty, punctuation=True, rng=self.rng)
        self.numbers = NumberSource(lang, rng=self.rng)
        self.symbols = SymbolSource(lang, rng=self.rng)

    def token(self):
        r = self.rng.random()
        if r < 0.15:
            return self.numbers.token()
        if r < 0.30:
            return self.symbols.token()
        word = self.words.token()
        if self.rng.random() < 0.2:
            word = word[:1].upper() + word[1:]
        return word


class EndlessSource(Source):
    """Text für den Unendlich-Modus: wird mit jedem Level schwieriger."""

    chunk_size = 4

    def __init__(self, lang="de", rng=None):
        super().__init__(rng)
        self.level = 1
        self.easy = WordSource(lang, "easy", rng=self.rng)
        self.normal = WordSource(lang, "normal", rng=self.rng)
        self.hard = WordSource(lang, "hard", punctuation=True, rng=self.rng)
        self.mixed = MixedSource(lang, "normal", rng=self.rng)

    def token(self):
        if self.level <= 2:
            return self.easy.token()
        if self.level <= 4:
            return self.normal.token()
        if self.level <= 6:
            return self.hard.token()
        return self.mixed.token()


class WeakSource(Source):
    """Bevorzugt Wörter, die deine schwächsten Tasten enthalten."""

    def __init__(self, lang="de", weak_chars=(), rng=None):
        super().__init__(rng)
        self.pool = word_pool(lang)
        letters = sorted({c.lower() for c in weak_chars if c.isalpha()})
        self.others = [c for c in weak_chars if not c.isalpha() and not c.isspace()]
        self.candidates, self.weights = [], []
        for word in self.pool:
            score = sum(word.lower().count(c) for c in letters)
            if score:
                self.candidates.append(word)
                self.weights.append(score)
        self.fallback = WordSource(lang, rng=self.rng)

    def token(self):
        rng = self.rng
        if self.others and rng.random() < 0.3:
            char = rng.choice(self.others)
            if char.isdigit():
                digits = [c for c in self.others if c.isdigit()]
                return "".join(rng.choice(digits) for _ in range(rng.randint(2, 4)))
            word = rng.choice(self.candidates or self.pool)
            return rng.choice((char + word, word + char, word + char + char))
        if self.candidates:
            return rng.choices(self.candidates, self.weights)[0]
        return self.fallback.token()


QUOTE_LENGTHS = ("random", "short", "medium", "long")


def pick_quote(lang, length="random", rng=None):
    rng = rng or random.Random()
    quotes = W.QUOTES["de" if lang == "de" else "en"]
    if length == "short":
        candidates = [q for q in quotes if len(q[0]) < 80]
    elif length == "medium":
        candidates = [q for q in quotes if 80 <= len(q[0]) < 200]
    elif length == "long":
        candidates = [q for q in quotes if len(q[0]) >= 200]
    else:
        candidates = list(quotes)
    return rng.choice(candidates or list(quotes))


CUSTOM_CHUNK = 400


def custom_chunk(text, pos, size=CUSTOM_CHUNK):
    """Teilt lange eigene Texte in Abschnitte. Gibt (start, ende) zurück;
    kurze Texte werden immer vollständig geübt."""
    if len(text) <= size * 1.5:
        return 0, len(text)
    if pos >= len(text) or pos < 0:
        pos = 0
    if pos + size >= len(text) - size * 0.3:
        return pos, len(text)
    lo, hi = pos + int(size * 0.6), min(len(text), pos + int(size * 1.3))
    best = max(text.rfind(mark, lo, hi) for mark in (". ", "! ", "? "))
    if best != -1:
        return pos, best + 1
    space = text.rfind(" ", pos + 1, pos + size + 1)
    return pos, space if space > pos else pos + size
