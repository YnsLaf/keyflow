"""Evaluations: records, streaks, daily totals, weak keys and achievements."""

from datetime import date, timedelta

from .i18n import pick

MODE_ORDER = ("zeit", "woerter", "frei", "unendlich", "geschichte", "saetze", "zahlen",
              "zeichen", "gemischt", "zitat", "schwaechen", "eigener")


def entry_date(entry):
    return date.fromisoformat(entry["ts"][:10])


def daily_seconds(history):
    days = {}
    for e in history:
        d = entry_date(e)
        days[d] = days.get(d, 0.0) + e.get("duration", 0)
    return days


def daily_tests(history):
    days = {}
    for e in history:
        d = entry_date(e)
        days[d] = days.get(d, 0) + 1
    return days


def streaks(days, today):
    """(current streak, longest streak) in days. The current streak stays alive
    as long as you practiced yesterday – there is still time today."""
    active = set(days)
    if not active:
        return 0, 0
    ordered = sorted(active)
    longest = run = 1
    for a, b in zip(ordered, ordered[1:]):
        run = run + 1 if (b - a).days == 1 else 1
        longest = max(longest, run)
    day = today if today in active else today - timedelta(days=1)
    current = 0
    while day in active:
        current += 1
        day -= timedelta(days=1)
    return current, longest


def record_value(entry):
    """What records are compared by: words reached in endless mode,
    otherwise speed."""
    return entry.get("score", entry["wpm"])


def record_eligible(entry):
    # a few seconds in free mode should not count as a record
    return not (entry["mode"].startswith("frei") and entry.get("duration", 0) < 30)


def records(history):
    best = {}
    for e in history:
        if not record_eligible(e):
            continue
        cur = best.get(e["mode"])
        if cur is None or record_value(e) > record_value(cur):
            best[e["mode"]] = e
    return best


def best_entry(history):
    eligible = [e for e in history if record_eligible(e) and "score" not in e]
    return max(eligible, key=lambda e: e["wpm"]) if eligible else None


def mode_sort_key(mode):
    parts = mode.split("-")
    base = parts[0]
    order = MODE_ORDER.index(base) if base in MODE_ORDER else len(MODE_ORDER)
    rest = tuple((0, int(p), "") if p.isdigit() else (1, 0, p) for p in parts[1:])
    return (order, rest)


def merged_key_stats(key_stats):
    """Merges upper and lower case (A and a = key A)."""
    merged = {}
    for ch, (attempts, errors) in key_stats.items():
        key = ch.lower() if ch.isalpha() else ch
        slot = merged.setdefault(key, [0, 0])
        slot[0] += attempts
        slot[1] += errors
    return merged


def weak_keys(key_stats, count=6, min_attempts=15, include_space=False):
    rows = []
    for ch, (attempts, errors) in merged_key_stats(key_stats).items():
        if attempts >= min_attempts and errors > 0 and (include_space or ch != " "):
            rows.append((ch, attempts, errors, errors / attempts))
    rows.sort(key=lambda r: (-r[3], -r[2]))
    return rows[:count]


def average(values):
    values = list(values)
    return sum(values) / len(values) if values else 0.0


# --- Achievements-------------------------------------------------------------

ACHIEVEMENTS = (
    ("start", ("Erste Schritte", "First Steps"),
     ("Schließe deinen ersten Test ab.", "Finish your first test.")),
    ("wpm30", ("Warmgelaufen", "Warmed Up"),
     ("Erreiche 30 WPM (mit mind. 90 % Genauigkeit).", "Reach 30 WPM (with at least 90 % accuracy).")),
    ("wpm50", ("Flinke Finger", "Quick Fingers"),
     ("Erreiche 50 WPM (mit mind. 90 % Genauigkeit).", "Reach 50 WPM (with at least 90 % accuracy).")),
    ("wpm70", ("Schnellschreiber", "Speed Typist"),
     ("Erreiche 70 WPM (mit mind. 90 % Genauigkeit).", "Reach 70 WPM (with at least 90 % accuracy).")),
    ("wpm90", ("Tastenblitz", "Lightning Keys"),
     ("Erreiche 90 WPM (mit mind. 90 % Genauigkeit).", "Reach 90 WPM (with at least 90 % accuracy).")),
    ("wpm110", ("Überschall", "Supersonic"),
     ("Erreiche 110 WPM (mit mind. 90 % Genauigkeit).", "Reach 110 WPM (with at least 90 % accuracy).")),
    ("perfekt", ("Fehlerfrei", "Flawless"),
     ("100 % Genauigkeit bei mindestens 100 Zeichen.", "100 % accuracy over at least 100 characters.")),
    ("praezise", ("Präzisionsarbeit", "Precision Work"),
     ("5 Tests hintereinander mit mind. 98 % Genauigkeit.", "5 tests in a row with at least 98 % accuracy.")),
    ("serie3", ("Dranbleiben", "Keep Going"),
     ("Übe an 3 Tagen in Folge.", "Practice 3 days in a row.")),
    ("serie7", ("Eine Woche stark", "Strong Week"),
     ("Übe an 7 Tagen in Folge.", "Practice 7 days in a row.")),
    ("serie30", ("Gewohnheit", "Habit"),
     ("Übe an 30 Tagen in Folge.", "Practice 30 days in a row.")),
    ("ziel", ("Tagesziel erreicht", "Daily Goal"),
     ("Erreiche dein Tagesziel an einem Tag.", "Reach your daily goal on one day.")),
    ("zeit1h", ("Eine Stunde", "One Hour"),
     ("Übe insgesamt eine Stunde.", "Practice for one hour in total.")),
    ("zeit10h", ("Zehn Stunden", "Ten Hours"),
     ("Übe insgesamt zehn Stunden.", "Practice for ten hours in total.")),
    ("tests50", ("Fleißig", "Diligent"),
     ("Schließe 50 Tests ab.", "Finish 50 tests.")),
    ("tests250", ("Unermüdlich", "Tireless"),
     ("Schließe 250 Tests ab.", "Finish 250 tests.")),
    ("marathon", ("Marathon", "Marathon"),
     ("Tippe im freien Modus 10 Minuten am Stück.", "Type for 10 minutes straight in free mode.")),
    ("zahlen", ("Zahlenprofi", "Number Pro"),
     ("Zahlen-Modus mit mind. 35 WPM und 95 % Genauigkeit.",
      "Numbers mode with at least 35 WPM and 95 % accuracy.")),
    ("zeichen", ("Symbolmeister", "Symbol Master"),
     ("Sonderzeichen mit mind. 25 WPM und 95 % Genauigkeit.",
      "Symbols mode with at least 25 WPM and 95 % accuracy.")),
    ("zitate", ("Belesen", "Well Read"),
     ("Tippe 10 Zitate.", "Type 10 quotes.")),
    ("eigener", ("Eigene Worte", "Own Words"),
     ("Tippe einen eigenen Text.", "Type one of your own texts.")),
    ("unendlich50", ("Durchhalter", "Stayer"),
     ("Schaffe 50 Wörter im Unendlich-Modus.", "Get 50 words in endless mode.")),
    ("unendlich150", ("Unaufhaltsam", "Unstoppable"),
     ("Schaffe 150 Wörter im Unendlich-Modus.", "Get 150 words in endless mode.")),
    ("geschichten10", ("Geschichtenerzähler", "Storyteller"),
     ("Tippe 10 verschiedene Geschichten.", "Type 10 different stories.")),
    ("geschichten40", ("Bücherwurm", "Bookworm"),
     ("Tippe alle 40 Geschichten.", "Type all 40 stories.")),
    ("extrem", ("Extremist", "Extremist"),
     ("Tippe eine extreme Geschichte mit mind. 95 % Genauigkeit.",
      "Type an extreme story with at least 95 % accuracy.")),
    ("zweisprachig", ("Zweisprachig", "Bilingual"),
     ("Übe auf Deutsch und auf Englisch.", "Practice in German and in English.")),
    ("eule", ("Nachteule", "Night Owl"),
     ("Übe zwischen 0 und 4 Uhr nachts.", "Practice between midnight and 4 a.m.")),
    ("frueh", ("Früher Vogel", "Early Bird"),
     ("Übe zwischen 4 und 7 Uhr morgens.", "Practice between 4 and 7 a.m.")),
)


def achievement_text(key):
    """(name, description) in the current language."""
    for k, name, desc in ACHIEVEMENTS:
        if k == key:
            return pick(name), pick(desc)
    return key, ""


def achieved(history, goal_minutes, today):
    """Set of all achievements whose condition the history meets."""
    got = set()
    if not history:
        return got
    got.add("start")
    best = max((e["wpm"] for e in history if e["acc"] >= 90), default=0)
    for n in (30, 50, 70, 90, 110):
        if best >= n:
            got.add("wpm%d" % n)
    if any(e["acc"] >= 100 and e.get("chars", 0) >= 100 for e in history):
        got.add("perfekt")
    run = 0
    for e in history:
        run = run + 1 if e["acc"] >= 98 else 0
        if run >= 5:
            got.add("praezise")
            break
    days = daily_seconds(history)
    _, longest = streaks(days, today)
    for n in (3, 7, 30):
        if longest >= n:
            got.add("serie%d" % n)
    if any(v >= goal_minutes * 60 for v in days.values()):
        got.add("ziel")
    total = sum(days.values())
    if total >= 3600:
        got.add("zeit1h")
    if total >= 36000:
        got.add("zeit10h")
    if len(history) >= 50:
        got.add("tests50")
    if len(history) >= 250:
        got.add("tests250")
    for e in history:
        mode = e["mode"]
        if mode.startswith("frei") and e.get("duration", 0) >= 600:
            got.add("marathon")
        if mode.startswith("zahlen") and e["wpm"] >= 35 and e["acc"] >= 95:
            got.add("zahlen")
        if mode.startswith("zeichen") and e["wpm"] >= 25 and e["acc"] >= 95:
            got.add("zeichen")
        if mode.startswith("eigener"):
            got.add("eigener")
        hour = int(e["ts"][11:13])
        if hour < 4:
            got.add("eule")
        elif hour < 7:
            got.add("frueh")
    best_endless = max((e.get("score", 0) for e in history if e["mode"].startswith("unendlich")),
                       default=0)
    if best_endless >= 50:
        got.add("unendlich50")
    if best_endless >= 150:
        got.add("unendlich150")
    stories = {e["story"] for e in history if e.get("story")}
    if len(stories) >= 10:
        got.add("geschichten10")
    if len(stories) >= 40:
        got.add("geschichten40")
    if any(e.get("story", "").startswith("extreme") and e["acc"] >= 95 for e in history):
        got.add("extrem")
    if sum(1 for e in history if e["mode"].startswith("zitat")) >= 10:
        got.add("zitate")
    if {"de", "en"} <= {e.get("lang") for e in history}:
        got.add("zweisprachig")
    return got
