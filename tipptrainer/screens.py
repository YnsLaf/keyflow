"""Alle Bildschirme: Hauptmenü, Test, Ergebnis, Statistik, Kalender, Erfolge …"""

import time
from datetime import date, timedelta

from colorama import Back, Fore

from . import stats, storage, stories
from . import terminal as T
from .ui import (ACCENT, BAD, BRIGHT, DIM, GOLD, GOOD, RESET, REVERSE, TEXT,
                 UNDERLINE, WARN, Item, acc_color, confirm, bar_chart, big_number,
                 content_width, draw, fmt_clock, fmt_minutes, fmt_date, fmt_duration, fmt_num,
                 frame, heat_cell, heat_level, pad, progress_bar, run_menu,
                 sparkline, title_block, vlen)

MONTHS = ("Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez")
WEEKDAYS = ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")
ON_OFF = {True: "an", False: "aus"}

FREE_LABELS = {
    "words": "Wörter", "sentences": "Sätze", "numbers": "Zahlen",
    "symbols": "Sonderzeichen", "mixed": "Gemischt",
}
QUOTE_LABELS = {"random": "zufällig", "short": "kurz", "medium": "mittel", "long": "lang"}


# --- Hauptmenü ---------------------------------------------------------------

MAIN_ITEMS = (
    ("time", "Zeit-Test", lambda v: "%d s" % v,
     "So viele Wörter wie möglich, bis die Zeit abläuft."),
    ("words", "Wörter-Test", lambda v: "%d Wörter" % v,
     "Eine feste Anzahl Wörter – so schnell und genau wie möglich."),
    ("free", "Freier Modus", FREE_LABELS,
     "Ohne Limit und ohne Druck: tippe endlos weiter. Esc beendet und speichert."),
    ("endless", "Unendlich-Modus", lambda v: "ab Level %d" % v,
     "Die Zeit läuft ab – jedes richtige Wort bringt Sekunden. Wie weit kommst du?"),
    ("stories", "Geschichten", lambda v: "%s (10)" % stories.LEVEL_LABELS[v],
     "40 Geschichten: einfach, mittel, schwer, extrem. Enter öffnet die Liste."),
    ("sentences", "Sätze", lambda v: "1 Satz" if v == 1 else "%d Sätze" % v,
     "Automatisch erzeugte Sätze mit Groß-/Kleinschreibung und Satzzeichen."),
    ("numbers", "Zahlen", lambda v: "%d Zahlen" % v,
     "Preise, Uhrzeiten, Datumsangaben, Rechnungen, Telefonnummern …"),
    ("symbols", "Sonderzeichen", lambda v: "%d Gruppen" % v,
     "Klammern, Operatoren, Pfade und E-Mails – ideal fürs Programmieren."),
    ("mixed", "Gemischt (Profi)", lambda v: "%d Teile" % v,
     "Wörter, Großbuchstaben, Zahlen und Sonderzeichen durcheinander."),
    ("quotes", "Zitate & Sprichwörter", QUOTE_LABELS,
     "Sprichwörter und berühmte Textstellen aus der Literatur."),
    ("weak", "Schwächen-Training", lambda v: "%d Wörter" % v,
     "Übt gezielt die Tasten, bei denen du die meisten Fehler machst."),
)


def main_header(store, width):
    today = date.today()
    days = stats.daily_seconds(store.history)
    current, _ = stats.streaks(days, today)
    goal = store.settings["daily_goal"]
    done = days.get(today, 0)
    best = stats.best_entry(store.history)
    mode = store.settings["color_mode"]

    title = BRIGHT + ACCENT + "T I P P T R A I N E R" + RESET + DIM + "  made by yns.laf" + RESET
    info = "Serie %s%d %s%s" % (GOLD if current else DIM, current,
                                 "Tag" if current == 1 else "Tage", RESET)
    if best:
        info += DIM + "  ·  " + RESET + "Bestwert " + BRIGHT + "%d WPM" % round(best["wpm"]) + RESET
    first = title + " " * max(2, width - vlen(title) - vlen(info)) + info

    cells = " ".join(heat_cell(heat_level(days.get(today - timedelta(days=i), 0), goal * 60), mode)
                     for i in range(13, -1, -1))
    goal_done = done >= goal * 60
    today_text = "Heute %s/%d min " % (fmt_minutes(done), goal)
    bar = progress_bar(done / (goal * 60), 12, GOOD if goal_done else ACCENT)
    tick = GOOD + " ✓" + RESET if goal_done else ""
    second_left = today_text + bar + tick
    second_right = DIM + "14 Tage " + RESET + cells
    second = second_left + " " * max(2, width - vlen(second_left) - vlen(second_right)) + second_right
    return [first, second, DIM + "─" * width + RESET]


def main_menu(term, store, index=0):
    menu = store.settings["menu"]

    def setter(key):
        def change(value):
            menu[key] = value
            store.save()
        return change

    items = []
    for key, label, fmt, hint in MAIN_ITEMS:
        items.append(Item(label, action=key, options=storage.MENU_OPTIONS[key],
                          value=menu[key], fmt=fmt, on_change=setter(key), hint=hint))
    unlocked = len(store.achievements)
    items += [
        Item("Eigener Text", action="custom", right="%d gespeichert" % len(store.custom_texts),
             hint="Eigene Texte einfügen oder aus einer Datei laden."),
        Item("Statistik & Rekorde", action="stats",
             hint="Bestwerte, Verlauf, Durchschnitt und deine schwächsten Tasten."),
        Item("Aktivität", action="activity",
             hint="Kalender deiner Übungstage – wie auf GitHub."),
        Item("Erfolge", action="achievements",
             right="%d/%d" % (unlocked, len(stats.ACHIEVEMENTS)),
             hint="Abzeichen für Tempo, Genauigkeit und Ausdauer."),
        Item("Einstellungen", action="settings",
             hint="Sprache, Satzzeichen, Zahlen, Fehlermodus, Tagesziel …"),
        Item("Beenden", action="quit"),
    ]
    width = content_width(term)
    action, index, _ = run_menu(
        term, lambda: main_header(store, content_width(term)), items, index,
        footer="↑↓ auswählen · ←→ ändern · Enter starten · Esc beenden", width=width)
    return action, index


# --- Test-Ansicht -------------------------------------------------------------

def _char_style(test, i, cursor):
    if i < test.pos:
        if test.marks[i]:
            return GOOD
        return Back.RED + Fore.WHITE if test.target[i] == " " else BAD + UNDERLINE
    if i == test.pos:
        return cursor
    return DIM


def draw_test(term, test, now, mode, settings, note=""):
    cols, rows = term.size()
    width = max(20, min(settings["text_width"], cols - 6))
    margin = " " * max(1, (cols - width) // 2)
    cursor = REVERSE if settings["cursor"] == "block" else UNDERLINE + TEXT + BRIGHT

    starts = test.line_starts(width)
    n_lines = len(starts)
    visible = settings["visible_lines"]
    current = test.cursor_line(width)
    first = current - 1 if visible >= 3 and current > 0 else current
    first = max(0, min(first, n_lines - visible))

    text_lines = []
    for ln in range(first, min(first + visible, n_lines)):
        a = starts[ln]
        b = starts[ln + 1] if ln + 1 < n_lines else len(test.target)
        parts, prev = [], None
        for i in range(a, b):
            style = _char_style(test, i, cursor)
            if style != prev:
                parts.append(RESET + style)
                prev = style
            parts.append(test.target[i])
        text_lines.append(margin + "".join(parts) + RESET)
    while len(text_lines) < visible:
        text_lines.append("")

    # Kopfzeile mit Zeit und Werten
    elapsed = test.elapsed(now)
    state = getattr(mode, "state", None)
    if mode.kind == "endless":
        remaining = max(0.0, state["budget"] - elapsed)
        color = GOOD if remaining > 6 else WARN if remaining > 3 else BAD
        clock = (color + BRIGHT + "%s s " % fmt_num(remaining, 1) + RESET
                 + progress_bar(remaining / 20.0, 16, color))
    elif mode.kind == "time":
        remaining = max(0, mode.limit - elapsed)
        clock = "%d" % (remaining + 0.999) if test.started else "%d" % mode.limit
    else:
        clock = fmt_clock(elapsed)
    parts = [BRIGHT + ACCENT + clock + RESET]
    if test.started and elapsed >= 1:
        if settings["live_wpm"]:
            parts.append(BRIGHT + "%d" % round(test.wpm(now)) + RESET + DIM + " WPM" + RESET)
        acc = test.accuracy()
        parts.append(acc_color(acc) + "%d %%" % round(acc) + RESET)
    if mode.kind == "text":
        if getattr(mode, "count_words", False):
            parts.append(DIM + "%d/%d Wörter" % (test.words_done(), test.words_total()) + RESET)
        else:
            parts.append(DIM + "Fortschritt %d %%" % (100 * test.pos // max(1, len(test.target))) + RESET)
    elif mode.kind == "free":
        parts.append(DIM + "%d Wörter" % test.words_done() + RESET)
    elif mode.kind == "endless":
        parts.append(ACCENT + BRIGHT + "Level %d" % state["level"] + RESET)
        parts.append(BRIGHT + "%d" % state["words"] + RESET + DIM + " Wörter" + RESET)
    stat_line = (DIM + "  ·  " + RESET).join(parts)
    if not test.started:
        stat_line += DIM + "   Tipp einfach los." + RESET

    label_line = DIM + mode.label + RESET
    if settings["strict"]:
        label_line += DIM + " · Fehler korrigieren" + RESET

    if mode.kind == "free":
        footer = "Esc beenden & speichern · Tab neuer Text"
    elif mode.kind == "endless":
        footer = "Richtige Wörter bringen Zeit, Fehler kosten 1 s · Esc aufgeben · Tab neu"
    else:
        footer = "Tab neu starten · Esc Menü"

    lines = [margin + label_line, margin + stat_line, ""] + text_lines
    if note:
        lines += ["", margin + DIM + note + RESET]
    top = max(0, (rows - len(lines) - 2) // 3)
    screen = [""] * top + lines
    screen = screen[:rows - 2]
    while len(screen) < rows - 2:
        screen.append("")
    screen.append(margin + DIM + footer + RESET)
    draw(term, screen)


# --- Ergebnis -----------------------------------------------------------------

def record_text(entry):
    if "score" in entry:
        return "%d Wörter" % entry["score"]
    return "%d WPM" % round(entry["wpm"])


def result_lines(mode, result, info, store, width):
    wpm_rows = big_number(result["wpm"])
    acc_rows = big_number(result["acc"])
    acc_col = acc_color(result["acc"])
    big = []
    wpm_w = max(len(r) for r in wpm_rows)
    for i in range(3):
        left = ACCENT + BRIGHT + wpm_rows[i].ljust(wpm_w) + RESET
        left += (DIM + " WPM" + RESET) if i == 2 else "    "
        right = acc_col + BRIGHT + acc_rows[i] + RESET + ((DIM + " %" + RESET) if i == 2 else "")
        big.append("  " + left + "      " + right)

    lines = [DIM + mode.label + RESET, ""] + big + [""]
    details = [
        "Roh " + BRIGHT + fmt_num(result["raw"]) + RESET + DIM + " WPM" + RESET,
        "Konstanz " + BRIGHT + "%d %%" % result["consistency"] + RESET,
        "Zeichen " + GOOD + "%d" % result["chars"] + RESET + DIM + " / " + RESET
        + BAD + "%d" % result["errors"] + RESET,
        "Zeit " + BRIGHT + fmt_num(result["duration"], 1) + " s" + RESET,
    ]
    lines.append((DIM + "  ·  " + RESET).join(details))
    entry = info.get("entry") or {}
    if mode.kind == "endless" and "score" in entry:
        lines.append("Geschafft " + GOLD + "%d Wörter" % entry["score"] + RESET + DIM + "  ·  " + RESET
                     + "erreicht " + ACCENT + BRIGHT + "Level %d" % entry["level"] + RESET
                     + DIM + "  ·  " + RESET + "überlebt " + BRIGHT + fmt_clock(result["duration"]) + RESET)

    series = result["wpm_series"]
    if len(series) >= 3:
        smooth = [sum(series[max(0, i - 2):i + 1]) / len(series[max(0, i - 2):i + 1])
                  for i in range(len(series))]
        lines.append("Verlauf " + ACCENT + sparkline(smooth, width - 20) + RESET
                     + DIM + "  %d–%d WPM" % (min(smooth), max(smooth)) + RESET)
    lines.append("")

    if not info.get("saved"):
        lines.append(WARN + "Zu kurz – dieser Test wurde nicht gespeichert." + RESET)
    else:
        prev = info.get("previous")
        if info.get("record") and prev:
            lines.append(GOLD + "★ NEUER REKORD! " + RESET + DIM + "(vorher %s)" % record_text(prev) + RESET)
        elif info.get("record"):
            lines.append(GOLD + "★ Erster Eintrag in diesem Modus – das ist dein Rekord." + RESET)
        elif prev:
            lines.append(DIM + "Rekord in diesem Modus: %s" % record_text(prev) + RESET)
        for key in info.get("achievements", []):
            lines.append(GOLD + "✓ Erfolg freigeschaltet: " + RESET + BRIGHT
                         + stats.ACHIEVEMENT_NAMES.get(key, key) + RESET)

    errors = sorted(result["key_errors"].items(), key=lambda kv: -kv[1])[:6]
    if errors:
        shown = "  ".join(BAD + ("␣" if ch == " " else ch) + RESET + DIM + " ×%d" % n + RESET
                          for ch, n in errors)
        lines.append("Fehler bei " + shown)

    goal = store.settings["daily_goal"] * 60
    done = stats.daily_seconds(store.history).get(date.today(), 0)
    reached = done >= goal
    lines.append("Tagesziel " + progress_bar(done / goal, 16, GOOD if reached else ACCENT)
                 + " %s/%d min" % (fmt_minutes(done), goal // 60)
                 + (GOOD + "  ✓ geschafft!" + RESET if reached else ""))
    return lines


def result_screen(term, mode, result, info, store):
    """Zeigt das Ergebnis. Gibt "next", "repeat" oder "menu" zurück."""
    footer = "Enter nächster Test"
    if mode.repeatable:
        footer += " · R gleichen Text wiederholen"
    footer += " · Esc Menü"
    term.flush_input()
    shown_at = time.monotonic()
    while True:
        width = content_width(term)
        lines = title_block("Ergebnis", width=width) + result_lines(mode, result, info, store, width)
        draw(term, frame(term, lines, footer))
        key = term.read_key(0.5)
        # Kurze Sperre, damit nachträgliche Tastendrücke nichts auslösen.
        if key is None or time.monotonic() - shown_at < 0.6:
            continue
        if key in (T.ENTER, T.TAB, "n"):
            return "next"
        if key in ("r", "R") and mode.repeatable:
            return "repeat"
        if key in (T.ESC, "q", "m", T.CTRL_C):
            return "menu"


# --- Statistik ----------------------------------------------------------------

def overview_lines(store, width):
    history = store.history
    if not history:
        return [DIM + "Noch keine Tests – leg los!" + RESET]
    today = date.today()
    days = stats.daily_seconds(history)
    tests_today = stats.daily_tests(history).get(today, 0)
    current, longest = stats.streaks(days, today)
    last10 = history[-10:]
    best = stats.best_entry(history)
    week_start = today - timedelta(days=today.weekday())
    week = sum(v for d, v in days.items() if d >= week_start)
    total_chars = sum(e.get("chars", 0) for e in history)

    rows = [
        ("Tests gesamt", fmt_num(len(history))),
        ("Übungszeit gesamt", fmt_duration(sum(days.values()))),
        ("Richtig getippte Zeichen", fmt_num(total_chars)),
        ("Ø Tempo (letzte 10)", "%s WPM" % fmt_num(stats.average(e["wpm"] for e in last10))),
        ("Ø Genauigkeit (letzte 10)", "%s %%" % fmt_num(stats.average(e["acc"] for e in last10), 1)),
        ("Ø Tempo (alle)", "%s WPM" % fmt_num(stats.average(e["wpm"] for e in history))),
    ]
    if best:
        rows.append(("Bestes Tempo", "%d WPM  %s(%s, %s)%s" % (
            round(best["wpm"]), DIM, best.get("label", best["mode"]),
            fmt_date(stats.entry_date(best)), RESET)))
    rows += [
        ("Aktive Tage", fmt_num(len(days))),
        ("Aktuelle Serie", "%d Tage" % current),
        ("Längste Serie", "%d Tage" % longest),
        ("Heute", "%s · %d Tests" % (fmt_duration(days.get(today, 0)), tests_today)),
        ("Diese Woche", fmt_duration(week)),
    ]
    return [DIM + pad(name, 28) + RESET + BRIGHT + value + RESET for name, value in rows]


def records_lines(store, width):
    best = stats.records(store.history)
    if not best:
        return [DIM + "Noch keine Rekorde." + RESET]
    label_w = min(40, max(vlen(e.get("label", k)) for k, e in best.items()) + 2)
    lines = [DIM + pad("Modus", label_w) + pad("Rekord", 12) + pad("Genauigkeit", 14) + "Datum" + RESET]
    for key in sorted(best, key=stats.mode_sort_key):
        e = best[key]
        lines.append(pad(e.get("label", key)[:label_w - 1], label_w)
                     + BRIGHT + ACCENT + pad(record_text(e), 12) + RESET
                     + acc_color(e["acc"]) + pad("%s %%" % fmt_num(e["acc"], 1), 14) + RESET
                     + DIM + fmt_date(stats.entry_date(e)) + RESET)
    return lines


def history_lines(store, width):
    history = store.history
    if not history:
        return [DIM + "Noch kein Verlauf." + RESET]
    count = max(5, width - 8)
    recent = history[-count:]
    wpms = [e["wpm"] for e in recent]
    lines = [DIM + "Tempo der letzten %d Tests (WPM)" % len(recent) + RESET, ""]
    lines += bar_chart(wpms, 8)
    lines.append("")
    accs = [e["acc"] for e in recent]
    lines.append(DIM + "Genauigkeit  " + RESET + GOOD + sparkline([max(0, a - 80) for a in accs]) + RESET
                 + DIM + "  (80–100 %)" + RESET)
    last10 = stats.average(e["wpm"] for e in history[-10:])
    lines.append("")
    summary = "Ø letzte 10: " + BRIGHT + fmt_num(last10) + RESET
    if len(history) >= 20:
        before = stats.average(e["wpm"] for e in history[-20:-10])
        diff = last10 - before
        arrow = (GOOD + "▲ +" if diff >= 0 else BAD + "▼ ") + fmt_num(diff, 1) + " WPM" + RESET
        summary += DIM + "  ·  Trend " + RESET + arrow
    if len(history) >= 50:
        summary += DIM + "  ·  Ø letzte 50: " + RESET + fmt_num(stats.average(e["wpm"] for e in history[-50:]))
    lines.append(summary)
    return lines


KEYBOARDS = {
    "de": (("^1234567890ß´", 0), ("qwertzuiopü+", 2), ("asdfghjklöä#", 3), ("<yxcvbnm,.-", 1)),
    "en": (("`1234567890-=", 0), ("qwertyuiop[]\\", 2), ("asdfghjkl;'", 3), ("zxcvbnm,./", 4)),
}
SHIFTED = {
    "de": dict(zip('°!"§$%&/()=?`*\'>;:_', "^1234567890ß´+#<,.-")),
    "en": dict(zip('~!@#$%^&*()_+{}|:"<>?', "`1234567890-=[]\\;',./")),
}
ALTGR_DE = {"@": "q", "€": "e", "{": "7", "[": "8", "]": "9", "}": "0", "\\": "ß", "~": "+", "|": "<"}


def _key_color(rate):
    if rate is None:
        return DIM
    if rate < 0.03:
        return Back.GREEN + Fore.BLACK
    if rate < 0.07:
        return Back.YELLOW + Fore.BLACK
    if rate < 0.12:
        return Back.LIGHTRED_EX + Fore.BLACK
    return Back.RED + Fore.WHITE


def keyboard_lines(store, width):
    lang = store.settings["language"]
    merged = stats.merged_key_stats(store.key_stats)
    shift = dict(SHIFTED[lang])
    if lang == "de":
        shift.update(ALTGR_DE)
    per_key = {}
    for ch, (attempts, errors) in merged.items():
        base = shift.get(ch, ch)
        slot = per_key.setdefault(base, [0, 0])
        slot[0] += attempts
        slot[1] += errors

    def rate(key):
        a, e = per_key.get(key, (0, 0))
        return e / a if a >= 5 else None

    lines = [DIM + "Fehlerquote je Taste (Umschalt- und AltGr-Zeichen zählen zur Grundtaste)" + RESET, ""]
    for row, indent in KEYBOARDS[lang]:
        cells = [_key_color(rate(k)) + " " + (k.upper() if len(k.upper()) == 1 else k) + " " + RESET
                 for k in row]
        lines.append(" " * indent + " ".join(cells))
    space_rate = rate(" ")
    lines.append(" " * 12 + _key_color(space_rate) + " " * 22 + RESET + DIM + "  Leertaste" + RESET)
    lines.append("")
    lines.append(_key_color(0.0) + " < 3 % " + RESET + " " + _key_color(0.05) + " < 7 % " + RESET + " "
                 + _key_color(0.1) + " < 12 % " + RESET + " " + _key_color(0.5) + " ≥ 12 % " + RESET
                 + " " + DIM + "grau = zu wenig Daten" + RESET)
    lines.append("")
    weak = stats.weak_keys(store.key_stats, count=8, min_attempts=10, include_space=True)
    if weak:
        lines.append(DIM + "Schwächste Tasten" + RESET)
        for ch, attempts, errors, r in weak:
            name = "Leertaste" if ch == " " else ch
            lines.append("  " + BAD + BRIGHT + pad(name, 10) + RESET
                         + progress_bar(min(1, r * 4), 12, BAD)
                         + " %s %%  %s(%d von %d)%s" % (fmt_num(r * 100, 1), DIM, errors, attempts, RESET))
    else:
        lines.append(DIM + "Noch zu wenig Daten für eine Auswertung." + RESET)
    return lines


def tab_screen(term, title, tabs, index=0):
    scroll = 0
    while True:
        cols, rows = term.size()
        width = content_width(term, 90)
        bar = []
        for i, (name, _) in enumerate(tabs):
            bar.append((REVERSE + BRIGHT if i == index else DIM) + " " + name + " " + RESET)
        body = tabs[index][1](width)
        room = max(3, rows - 8)
        scroll = max(0, min(scroll, len(body) - room))
        lines = title_block(title, width=width) + ["  ".join(bar), ""] + body[scroll:scroll + room]
        footer = "←→ Bereich wechseln"
        if len(body) > room:
            footer += " · ↑↓ scrollen"
        footer += " · Esc zurück"
        draw(term, frame(term, lines, footer, width))
        key = term.read_key(0.5)
        if key in (T.RIGHT, T.TAB, "l"):
            index, scroll = (index + 1) % len(tabs), 0
        elif key in (T.LEFT, "h"):
            index, scroll = (index - 1) % len(tabs), 0
        elif key in (T.DOWN, "j"):
            scroll += 1
        elif key in (T.UP, "k"):
            scroll = max(0, scroll - 1)
        elif key in (T.ESC, T.ENTER, "q", T.CTRL_C):
            return


def stats_screen(term, store):
    tabs = [
        ("Übersicht", lambda w: overview_lines(store, w)),
        ("Rekorde", lambda w: records_lines(store, w)),
        ("Verlauf", lambda w: history_lines(store, w)),
        ("Tastatur", lambda w: keyboard_lines(store, w)),
    ]
    tab_screen(term, "Statistik & Rekorde", tabs)


# --- Aktivitätskalender -------------------------------------------------------

def activity_lines(store, width, offset_weeks=0, today=None):
    today = today or date.today()
    mode = store.settings["color_mode"]
    goal = store.settings["daily_goal"] * 60
    days = stats.daily_seconds(store.history)
    tests = stats.daily_tests(store.history)

    weeks = max(4, min(53, (width - 4) // 2))
    end_monday = today - timedelta(days=today.weekday()) - timedelta(weeks=offset_weeks)
    start = end_monday - timedelta(weeks=weeks - 1)
    end = min(today, end_monday + timedelta(days=6))

    label_row = [" "] * (weeks * 2 + 1)
    free_from = 0
    prev_month = None
    for col in range(weeks):
        month = (start + timedelta(weeks=col)).month
        if month != prev_month:
            name = MONTHS[month - 1]
            pos = col * 2
            if pos >= free_from and pos + len(name) <= len(label_row):
                label_row[pos:pos + len(name)] = list(name)
                free_from = pos + len(name) + 1
            prev_month = month
    lines = [DIM + "    " + "".join(label_row).rstrip() + RESET]

    for row in range(7):
        name = WEEKDAYS[row] if row in (0, 2, 4, 6) else ""
        cells = []
        for col in range(weeks):
            d = start + timedelta(days=col * 7 + row)
            if d > today:
                cells.append("  ")
            else:
                cells.append(heat_cell(heat_level(days.get(d, 0), goal), mode) + " ")
        lines.append(DIM + pad(name, 4) + RESET + "".join(cells))

    legend = " ".join(heat_cell(level, mode) for level in range(5))
    lines.append("")
    lines.append(DIM + "    Weniger " + RESET + legend + DIM + " Mehr" + RESET)
    lines.append(DIM + "    Stufen: unter ½ Tagesziel · unter Tagesziel · Ziel erreicht · doppeltes Ziel"
                 + RESET)
    lines.append("")

    in_range = [d for d in days if start <= d <= end]
    current, longest = stats.streaks(days, today)
    lines.append("Zeitraum " + BRIGHT + "%s – %s" % (fmt_date(start), fmt_date(end)) + RESET)
    lines.append(BRIGHT + "%d" % len(in_range) + RESET + " aktive Tage  ·  "
                 + BRIGHT + fmt_duration(sum(days[d] for d in in_range)) + RESET + " Übung  ·  "
                 + BRIGHT + "%d" % sum(tests.get(d, 0) for d in in_range) + RESET + " Tests")
    lines.append("Aktuelle Serie " + GOLD + "%d" % current + RESET + "  ·  Längste Serie "
                 + BRIGHT + "%d" % longest + RESET + "  ·  Tagesziel %d min" % (goal // 60))

    week_start = today - timedelta(days=today.weekday())
    week = []
    for i in range(7):
        d = week_start + timedelta(days=i)
        if d > today:
            week.append(DIM + WEEKDAYS[i] + " –" + RESET)
        else:
            minutes = days.get(d, 0) / 60
            color = GOOD if days.get(d, 0) >= goal else TEXT if minutes else DIM
            week.append(DIM + WEEKDAYS[i] + " " + RESET + color + fmt_num(minutes) + RESET)
    lines.append("Diese Woche (min)  " + "  ".join(week))
    return lines


def activity_screen(term, store):
    offset = 0
    while True:
        width = content_width(term, 112)
        lines = title_block("Aktivität", "an welchen Tagen du geübt hast", width)
        lines += [""] + activity_lines(store, width, offset)
        footer = "←→ Zeitraum verschieben · Esc zurück"
        draw(term, frame(term, lines, footer, width))
        key = term.read_key(0.5)
        weeks = max(4, min(53, (width - 4) // 2))
        if key in (T.LEFT, "h"):
            offset += max(4, weeks // 2)
        elif key in (T.RIGHT, "l"):
            offset = max(0, offset - max(4, weeks // 2))
        elif key in (T.ESC, T.ENTER, "q", T.CTRL_C):
            return


# --- Erfolge ------------------------------------------------------------------

def achievements_screen(term, store):
    scroll = 0
    while True:
        cols, rows = term.size()
        width = content_width(term)
        total = len(stats.ACHIEVEMENTS)
        got = len(store.achievements)
        lines = title_block("Erfolge", "%d von %d freigeschaltet" % (got, total), width)
        lines.append(progress_bar(got / total, min(40, width), GOLD))
        lines.append("")
        body = []
        for key, name, desc in stats.ACHIEVEMENTS:
            if key in store.achievements:
                when = store.achievements[key][:10]
                try:
                    when = fmt_date(date.fromisoformat(when))
                except ValueError:
                    pass
                body.append(GOLD + "★ " + pad(name, 20) + RESET + desc + DIM + "  " + when + RESET)
            else:
                body.append(DIM + "☆ " + pad(name, 20) + desc + RESET)
        room = max(3, rows - len(lines) - 4)
        scroll = max(0, min(scroll, len(body) - room))
        lines += body[scroll:scroll + room]
        footer = ("↑↓ scrollen · " if len(body) > room else "") + "Esc zurück"
        draw(term, frame(term, lines, footer))
        key = term.read_key(0.5)
        if key in (T.DOWN, "j"):
            scroll += 1
        elif key in (T.UP, "k"):
            scroll = max(0, scroll - 1)
        elif key in (T.ESC, T.ENTER, "q", T.CTRL_C):
            return


# --- Einstellungen ------------------------------------------------------------

SETTINGS_UI = (
    ("language", "Sprache der Texte", {"de": "Deutsch", "en": "Englisch"},
     "Sprache für Wörter, Sätze und Zitate. Rekorde werden je Sprache geführt."),
    ("difficulty", "Wortlänge", {"easy": "kurze Wörter", "normal": "gemischt", "hard": "lange Wörter"},
     "Welche Wörter in Zeit-, Wörter- und freien Tests vorkommen."),
    ("punctuation", "Satzzeichen", ON_OFF,
     "Fügt in Zeit-, Wörter- und freien Tests Kommas, Punkte, Klammern … ein."),
    ("numbers", "Zahlen", ON_OFF, "Mischt in Zeit-, Wörter- und freien Tests Zahlen unter die Wörter."),
    ("lowercase", "Nur Kleinbuchstaben", ON_OFF, "Schreibt alle Wörter klein (Satzanfänge bleiben groß)."),
    ("umlauts", "Umlaute & ß", {True: "tippen", False: "ersetzen (ae, oe, ue, ss)"},
     "Praktisch, wenn deine Tastatur keine deutschen Umlaute hat."),
    ("strict", "Fehler", {False: "weitertippen erlaubt", True: "müssen korrigiert werden"},
     "Im strengen Modus geht es erst weiter, wenn das richtige Zeichen getippt ist."),
    None,
    ("live_wpm", "Live-WPM anzeigen", ON_OFF, "Zeigt das Tempo schon während des Tippens."),
    ("cursor", "Cursor", {"block": "Block", "underline": "Unterstrich"}, "Wie die aktuelle Stelle markiert wird."),
    ("visible_lines", "Sichtbare Zeilen", str, "Wie viele Textzeilen gleichzeitig zu sehen sind."),
    ("text_width", "Textbreite", lambda v: "%d Zeichen" % v, "Maximale Breite einer Textzeile."),
    ("bell", "Ton bei Fehlern", ON_OFF, "Lässt bei jedem Tippfehler die Terminal-Glocke klingen."),
    ("color_mode", "Kalenderfarben", {"256": "256 Farben", "truecolor": "True Color",
                                       "basic": "Basis (16 Farben)"},
     "Falls der Kalender komisch aussieht, probiere eine andere Stufe."),
    None,
    ("daily_goal", "Tagesziel", lambda v: "%d min" % v,
     "Wie lange du pro Tag üben möchtest. Bestimmt auch die Kalenderfarben."),
)


def settings_screen(term, store):
    settings = store.settings

    def setter(key):
        def change(value):
            settings[key] = value
            store.save()
        return change

    items = []
    for entry in SETTINGS_UI:
        if entry is None:
            items.append(Item.sep())
            continue
        key, label, fmt, hint = entry
        items.append(Item(label, options=storage.SETTING_OPTIONS[key], value=settings[key],
                          fmt=fmt, on_change=setter(key), hint=hint))
    items += [
        Item.sep(),
        Item("Statistiken zurücksetzen", action="reset",
             hint="Löscht Verlauf, Rekorde, Tastenstatistik und Erfolge. Eigene Texte bleiben."),
        Item("Zurück", action="back"),
    ]
    width = content_width(term)
    index = 0
    while True:
        action, index, _ = run_menu(
            term, title_block("Einstellungen", "Datei: %s" % store.path, width), items, index,
            footer="↑↓ auswählen · ←→/Enter ändern · Esc zurück", width=width)
        if action == "reset":
            if confirm(term, "Statistiken zurücksetzen",
                       "Wirklich den gesamten Verlauf, alle Rekorde und Erfolge löschen?"):
                store.reset_stats()
            continue
        return


# --- Geschichten ----------------------------------------------------------------

def stories_menu(term, store, level, index=0):
    best = {}
    for e in store.history:
        sid = e.get("story")
        if sid and e["wpm"] > best.get(sid, 0):
            best[sid] = e["wpm"]
    items = []
    for i, (title, text) in enumerate(stories.STORIES[level]):
        sid = stories.story_id(level, i)
        mark = (GOOD + "✓ " + RESET + DIM + "%d WPM · " % round(best[sid])) if sid in best else DIM + "neu · "
        items.append(Item("%2d. %s" % (i + 1, title), action=i,
                          right=mark + "%d Zeichen" % len(text) + RESET,
                          hint=text[:66] + " …"))
    items += [Item.sep(), Item("Zurück", action="back")]
    done = sum(1 for i in range(len(stories.STORIES[level])) if stories.story_id(level, i) in best)
    width = content_width(term)
    header = title_block("Geschichten – %s" % stories.LEVEL_LABELS[level],
                         "%d von %d geschafft · auf Deutsch" % (done, len(stories.STORIES[level])), width)
    return run_menu(term, header, items, index,
                    footer="↑↓ auswählen · Enter tippen · Esc zurück", width=width)


# --- Eigene Texte -------------------------------------------------------------

def custom_menu(term, store, index=0):
    items = []
    for i, entry in enumerate(store.custom_texts):
        text = entry["text"]
        right = "%s Zeichen" % fmt_num(len(text))
        if len(text) > 600:
            right += " · %d %%" % (100 * entry.get("pos", 0) // len(text))
        title = entry.get("title") or text[:30]
        items.append(Item(title[:34], action=i, right=right,
                          hint="Enter üben · Entf/D löschen"))
    if items:
        items.append(Item.sep())
    items += [
        Item("+ Text einfügen", action="new", hint="Text aus der Zwischenablage einfügen."),
        Item("+ Aus Datei laden", action="file", hint="Eine .txt-Datei laden (UTF-8)."),
        Item("Zurück", action="back"),
    ]
    width = content_width(term)
    header = title_block("Eigener Text", "lange Texte werden in Abschnitten geübt", width)
    return run_menu(term, header, items, index,
                    footer="↑↓ auswählen · Enter üben · Entf/D löschen · Esc zurück",
                    extra_keys=(T.DELETE, "d", "D"), width=width)
