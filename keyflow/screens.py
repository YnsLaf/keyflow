"""Alle Bildschirme: Hauptmenü, Test, Ergebnis, Statistik, Kalender, Erfolge …"""

import platform
import sys
import time
from datetime import date, timedelta

from colorama import Back, Fore

from . import __version__, keyboard, stats, storage, stories, ui, updates
from . import terminal as T
from .i18n import pick, tr
from .ui import (ACCENT, BAD, BRIGHT, DIM, GOLD, GOOD, RESET, REVERSE, TEXT,
                 UNDERLINE, WARN, Item, acc_color, confirm, bar_chart, big_number,
                 content_width, draw, fmt_clock, fmt_minutes, fmt_date, fmt_duration, fmt_num,
                 frame, heat_cell, heat_level, pad, progress_bar, run_menu,
                 sparkline, title_block, vlen)

def months():
    return tr(("Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"),
              ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"))


def weekdays():
    return tr(("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"), ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"))


def on_off(value):
    return tr("an", "on") if value else tr("aus", "off")


def free_label(value):
    return pick({"words": ("Wörter", "Words"), "sentences": ("Sätze", "Sentences"),
                 "numbers": ("Zahlen", "Numbers"), "symbols": ("Sonderzeichen", "Symbols"),
                 "mixed": ("Gemischt", "Mixed")}[value])


def quote_label(value):
    return pick({"random": ("zufällig", "random"), "short": ("kurz", "short"),
                 "medium": ("mittel", "medium"), "long": ("lang", "long")}[value])


def words_label(n):
    return tr("%d Wörter", "%d words") % n


# --- Hauptmenü ---------------------------------------------------------------

def main_items():
    """(Schlüssel, Name, Format für den Wert, Hinweis) aller Übungsmodi."""
    return (
        ("time", tr("Zeit-Test", "Time test"), lambda v: "%d s" % v,
         tr("So viele Wörter wie möglich, bis die Zeit abläuft.",
            "As many words as possible before the time runs out.")),
        ("words", tr("Wörter-Test", "Word test"), words_label,
         tr("Eine feste Anzahl Wörter – so schnell und genau wie möglich.",
            "A fixed number of words – as fast and accurate as you can.")),
        ("free", tr("Freier Modus", "Free mode"), free_label,
         tr("Ohne Limit und ohne Druck: tippe endlos weiter. Esc beendet und speichert.",
            "No limit, no pressure: keep typing forever. Esc ends and saves.")),
        ("endless", tr("Unendlich-Modus", "Endless mode"), lambda v: tr("ab Level %d", "from level %d") % v,
         tr("Die Zeit läuft ab – jedes richtige Wort bringt Sekunden. Wie weit kommst du?",
            "The clock runs down – every correct word adds seconds. How far can you get?")),
        ("stories", tr("Geschichten", "Stories"), lambda v: "%s (10)" % stories.level_label(v),
         tr("40 Geschichten: einfach, mittel, schwer, extrem. Enter öffnet die Liste.",
            "40 stories: easy, medium, hard, extreme. Enter opens the list.")),
        ("sentences", tr("Sätze", "Sentences"),
         lambda v: tr("1 Satz", "1 sentence") if v == 1 else tr("%d Sätze", "%d sentences") % v,
         tr("Automatisch erzeugte Sätze mit Groß-/Kleinschreibung und Satzzeichen.",
            "Generated sentences with capitals and punctuation.")),
        ("numbers", tr("Zahlen", "Numbers"), lambda v: tr("%d Zahlen", "%d numbers") % v,
         tr("Preise, Uhrzeiten, Datumsangaben, Rechnungen, Telefonnummern …",
            "Prices, times, dates, sums, phone numbers …")),
        ("symbols", tr("Sonderzeichen", "Symbols"), lambda v: tr("%d Gruppen", "%d groups") % v,
         tr("Klammern, Operatoren, Pfade und E-Mails – ideal fürs Programmieren.",
            "Brackets, operators, paths and e-mails – great for coding.")),
        ("mixed", tr("Gemischt (Profi)", "Mixed (pro)"), lambda v: tr("%d Teile", "%d parts") % v,
         tr("Wörter, Großbuchstaben, Zahlen und Sonderzeichen durcheinander.",
            "Words, capitals, numbers and symbols all mixed up.")),
        ("quotes", tr("Zitate & Sprichwörter", "Quotes & proverbs"), quote_label,
         tr("Sprichwörter und berühmte Textstellen aus der Literatur.",
            "Proverbs and famous lines from literature.")),
        ("weak", tr("Schwächen-Training", "Weak keys"), words_label,
         tr("Übt gezielt die Tasten, bei denen du die meisten Fehler machst.",
            "Trains exactly the keys you get wrong the most.")),
    )


def mode_info(key):
    for k, label, fmt, hint in main_items():
        if k == key:
            return label, fmt, hint
    raise KeyError(key)


TITLE = "K E Y F L O W"


def main_header(store, width):
    today = date.today()
    days = stats.daily_seconds(store.history)
    current, _ = stats.streaks(days, today)
    goal = store.settings["daily_goal"]
    done = days.get(today, 0)
    best = stats.best_entry(store.history)
    mode = store.settings["color_mode"]

    title = TITLE + DIM + "  made by YnsLaf" + RESET
    info = tr("Serie", "Streak") + " %s%d %s%s" % (
        GOLD if current else DIM, current,
        tr("Tag", "day") if current == 1 else tr("Tage", "days"), RESET)
    if best:
        info += DIM + "  ·  " + RESET + tr("Bestwert ", "Best ") + BRIGHT + "%d WPM" % round(best["wpm"]) + RESET
    first = title + " " * max(2, width - vlen(title) - vlen(info)) + info

    cells = " ".join(heat_cell(heat_level(days.get(today - timedelta(days=i), 0), goal * 60), mode)
                     for i in range(13, -1, -1))
    goal_done = done >= goal * 60
    today_text = tr("Heute", "Today") + " %s/%d min " % (fmt_minutes(done), goal)
    bar = progress_bar(done / (goal * 60), 12, GOOD if goal_done else ACCENT)
    tick = GOOD + " ✓" + RESET if goal_done else ""
    second_left = today_text + bar + tick
    second_right = DIM + tr("14 Tage ", "14 days ") + RESET + cells
    second = second_left + " " * max(2, width - vlen(second_left) - vlen(second_right)) + second_right
    return [first, second, DIM + "─" * width + RESET]


def categories():
    return (
        ("practice", tr("Tippen üben", "Practice"),
         tr("Zeit-Test, Wörter-Test, Freier Modus und Unendlich-Modus.",
            "Time test, word test, free mode and endless mode."),
         ("time", "words", "free", "endless")),
        ("texts", tr("Texte & Geschichten", "Texts & stories"),
         tr("Geschichten, Sätze, Zitate und eigene Texte.",
            "Stories, sentences, quotes and your own texts."),
         ("stories", "sentences", "quotes", "custom")),
        ("special", tr("Zahlen & Zeichen", "Numbers & symbols"),
         tr("Zahlen, Sonderzeichen, Gemischt und Schwächen-Training.",
            "Numbers, symbols, mixed and weak-key training."),
         ("numbers", "symbols", "mixed", "weak")),
        ("progress", tr("Fortschritt", "Progress"),
         tr("Statistik & Rekorde, Aktivitätskalender und Erfolge.",
            "Stats & records, activity calendar and achievements."),
         ("stats", "activity", "achievements")),
    )


def quick_label(store):
    last = store.settings["menu"]["last"]
    label, fmt, _ = mode_info(last)
    value = store.settings["menu"][last]
    text = fmt.get(value, str(value)) if isinstance(fmt, dict) else fmt(value)
    return "%s · %s" % (label, text)


# --- Maskottchen ----------------------------------------------------------------

def mascot_messages(store, updater=None):
    if updater is not None and updater.available:
        return [tr("Neue Version %s ist da! Schau unter Info.", "Version %s is out! Have a look at Info.")
                % updater.latest] + mascot_messages(store)
    today = date.today()
    days = stats.daily_seconds(store.history)
    current, _ = stats.streaks(days, today)
    goal = store.settings["daily_goal"] * 60
    done = days.get(today, 0)
    best = stats.best_entry(store.history)
    home_row = tr("Tipp: Die Zeigefinger ruhen auf F und J.",
                  "Tip: Your index fingers rest on F and J.")
    if not store.history:
        return [tr("Hi, ich bin Flow! Drück Enter und leg los.",
                   "Hi, I'm Flow! Press Enter and get going."), home_row]
    msgs = []
    if done >= goal:
        msgs.append(tr("Tagesziel geschafft – stark!", "Daily goal done – awesome!"))
    elif done > 0:
        msgs.append(tr("Noch %d min bis zum Tagesziel.", "%d more min to your daily goal.")
                    % max(1, round((goal - done) / 60)))
    else:
        msgs.append(tr("Heute noch nicht geübt. Eine Runde?", "No practice yet today. One round?"))
    if current >= 2:
        msgs.append(tr("%d Tage in Folge – weiter so!", "%d days in a row – keep it up!") % current)
    if best:
        msgs.append(tr("Dein Rekord: %d WPM. Knackst du ihn?", "Your record: %d WPM. Can you beat it?")
                    % round(best["wpm"]))
    msgs += [tr("Tipp: Schau auf den Text, nicht auf die Tasten.",
                "Tip: Look at the text, not at the keys."),
             tr("Tipp: Erst genau, dann schnell.", "Tip: Accuracy first, speed follows."),
             home_row]
    return msgs


def _wrap_words(text, width):
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    return lines + [line] if line else lines


def mascot(store, messages):
    """Flow, das KeyFlow-Maskottchen: blinzelt, wippt und gibt Tipps."""
    t = ui.clock()
    body = ui.fg(ui.hsv(0.5 + t * 0.08, 0.45, 0.95))
    eye_col = TEXT + BRIGHT
    blink = (t % 4.0) < 0.18
    eye = "–" if blink else "◕"
    done_today = stats.daily_seconds(store.history).get(date.today(), 0) > 0
    mouth = "◡" if done_today else "‿"
    msg = messages[int(t / 5) % len(messages)] if t else messages[0]

    width = 24
    text_lines = _wrap_words(msg, width)[:3]
    bubble = [DIM + "╭" + "─" * (width + 2) + "╮" + RESET]
    for line in text_lines:
        bubble.append(DIM + "│ " + RESET + TEXT + line.ljust(width) + RESET + DIM + " │" + RESET)
    bubble.append(DIM + "╰──┬" + "─" * (width - 1) + "╯" + RESET)
    bubble.append(DIM + "   ╵" + RESET)

    bob = int(t * 1.5) % 2 if t else 0
    figure = [
        body + "  ╭───────╮" + RESET,
        body + "  │ " + eye_col + eye + "   " + eye + body + " │" + RESET,
        body + "  │   " + eye_col + mouth + body + "   │" + RESET,
        body + "  ╰─┬───┬─╯" + RESET,
        body + "    ╵   ╵" + RESET,
    ]
    return bubble + ([""] if bob else []) + figure + ([] if bob else [""]) + \
        [DIM + "    Flow" + RESET]


# --- Hauptmenü --------------------------------------------------------------

def main_menu(term, store, index=0, updater=None):
    items = [Item(tr("Weiter: ", "Continue: ") + quick_label(store), action="quick",
                  hint=tr("Startet sofort deinen zuletzt gespielten Modus.",
                          "Starts the mode you played last right away."))]
    for key, label, hint, _ in categories():
        items.append(Item(label, action=key, hint=hint))
    items += [
        Item(tr("Einstellungen", "Settings"), action="settings",
             hint=tr("Sprache, Satzzeichen, Hintergrund, Tastatur, Tagesziel …",
                     "Language, punctuation, background, keyboard, daily goal …")),
        Item("Info", action="info",
             right=(GOLD + tr("Update!", "Update!") + RESET) if updater is not None and updater.available else "",
             hint=tr("Version, Updates und alles über KeyFlow und YnsLaf.",
                     "Version, updates and all about KeyFlow and YnsLaf.")),
        Item(tr("Beenden", "Quit"), action="quit", hint=tr("Bis bald!", "See you soon!")),
    ]
    width = content_width(term)
    cache = {}
    messages = mascot_messages(store, updater)

    def header():
        w = content_width(term)
        if cache.get("width") != w:
            cache["width"], cache["lines"] = w, main_header(store, w)
        lines = list(cache["lines"])
        lines[0] = lines[0].replace(TITLE, ui.gradient(TITLE), 1)
        return lines + [""]

    action, index, _ = run_menu(
        term, header, items, index, numbered=True, side=lambda: mascot(store, messages),
        side_col=40, footer=tr("↑↓ wählen · Enter öffnen · 1–8 direkt · Esc beenden",
                               "↑↓ choose · Enter open · 1–8 direct · Esc quit"), width=width)
    return action, index


def category_menu(term, store, category, index=0):
    menu = store.settings["menu"]

    def setter(key):
        def change(value):
            menu[key] = value
            store.save()
        return change

    items = []
    cats = {c[0]: c for c in categories()}
    for key in cats[category][3]:
        if key in storage.MENU_OPTIONS:
            label, fmt, hint = mode_info(key)
            items.append(Item(label, action=key, options=storage.MENU_OPTIONS[key],
                              value=menu[key], fmt=fmt, on_change=setter(key), hint=hint))
        elif key == "custom":
            items.append(Item(tr("Eigener Text", "Your own text"), action="custom",
                              right=tr("%d gespeichert", "%d saved") % len(store.custom_texts),
                              hint=tr("Eigene Texte einfügen oder aus einer Datei laden.",
                                      "Paste your own texts or load them from a file.")))
        elif key == "stats":
            items.append(Item(tr("Statistik & Rekorde", "Stats & records"), action="stats",
                              hint=tr("Bestwerte, Verlauf, Durchschnitt und deine schwächsten Tasten.",
                                      "Best scores, history, averages and your weakest keys.")))
        elif key == "activity":
            items.append(Item(tr("Aktivität", "Activity"), action="activity",
                              hint=tr("Kalender deiner Übungstage – wie auf GitHub.",
                                      "Calendar of your practice days – like on GitHub.")))
        elif key == "achievements":
            items.append(Item(tr("Erfolge", "Achievements"), action="achievements",
                              right="%d/%d" % (len(store.achievements), len(stats.ACHIEVEMENTS)),
                              hint=tr("Abzeichen für Tempo, Genauigkeit und Ausdauer.",
                                      "Badges for speed, accuracy and stamina.")))
    items += [Item.sep(), Item(tr("Zurück", "Back"), action="back")]
    width = content_width(term)
    has_options = any(it.options for it in items)
    footer = (tr("↑↓ wählen · ←→ Länge/Stufe ändern · Enter starten · Esc zurück",
                 "↑↓ choose · ←→ change length/level · Enter start · Esc back") if has_options
              else tr("↑↓ wählen · Enter öffnen · Esc zurück", "↑↓ choose · Enter open · Esc back"))
    action, index, _ = run_menu(
        term, lambda: title_block(cats[category][1], width=width) + [""], items, index,
        numbered=True, footer=footer, width=width)
    return action, index


# --- Test-Ansicht -------------------------------------------------------------

KEY_IDLE_FG = (110, 116, 128)
KEY_HOME_FG = (170, 176, 188)   # F und J (Grundstellung)
KEY_SPACE_FG = (70, 74, 84)
KEY_GLOW_A = (80, 220, 255)
KEY_GLOW_B = (170, 120, 255)
KEY_ERROR = (235, 70, 80)


def live_keyboard(lang, next_char, flash=None):
    """Tastatur mit leuchtender nächster Taste. flash = falsch gedrückte Taste."""
    glow_keys, hint = keyboard.keys_for(next_char, lang)
    error_key = keyboard.base_key(flash, lang) if flash else None
    glow = ui.mix(KEY_GLOW_A, KEY_GLOW_B, ui.pulse(4.0))
    lines = []
    for row in keyboard.layout(lang):
        out, col = [], 0
        for x, label, key_id, width in row:
            out.append(" " * max(0, x - col))
            cap = label.center(width)
            if error_key is not None and key_id == error_key:
                out.append(ui.fg(KEY_ERROR) + BRIGHT + cap + RESET)
            elif key_id == " ":
                color = ui.fg(glow) + BRIGHT if " " in glow_keys else ui.fg(KEY_SPACE_FG)
                out.append(color + ("━" if " " in glow_keys else "─") * width + RESET)
            elif key_id in glow_keys:
                out.append(ui.fg(glow) + BRIGHT + cap + RESET)
            elif key_id in ("f", "j"):
                pad_l = (width - len(label)) // 2
                out.append(ui.fg(KEY_HOME_FG) + " " * pad_l + UNDERLINE + label + "\x1b[24m"
                           + " " * (width - pad_l - len(label)) + RESET)
            else:
                out.append(ui.fg(KEY_IDLE_FG) + cap + RESET)
            col = x + width
        lines.append("".join(out))
    return lines, hint


def _char_style(test, i, cursor, word_end):
    if i < test.pos:
        if test.marks[i]:
            return GOOD
        return Back.RED + Fore.WHITE if test.target[i] == " " else BAD + UNDERLINE
    if i == test.pos:
        return cursor
    if i < word_end:
        return TEXT + BRIGHT   # das aktuelle Wort leuchtet
    return DIM


def draw_test(term, test, now, mode, settings, note="", flash=None):
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
    word_end = test.target.find(" ", test.pos)
    word_end = len(test.target) if word_end == -1 else word_end

    text_lines = []
    for ln in range(first, min(first + visible, n_lines)):
        a = starts[ln]
        b = starts[ln + 1] if ln + 1 < n_lines else len(test.target)
        parts, prev = [], None
        for i in range(a, b):
            style = _char_style(test, i, cursor, word_end)
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
    progress = None
    if mode.kind == "endless":
        remaining = max(0.0, state["budget"] - elapsed)
        color = GOOD if remaining > 6 else WARN if remaining > 3 else BAD
        clock = color + BRIGHT + "%s s" % fmt_num(remaining, 1) + RESET
        progress = remaining / 20.0
    elif mode.kind == "time":
        remaining = max(0, mode.limit - elapsed)
        clock = "%d" % (remaining + 0.999) if test.started else "%d" % mode.limit
        progress = elapsed / mode.limit
    else:
        clock = fmt_clock(elapsed)
        if mode.kind == "text":
            progress = test.pos / max(1, len(test.target))
    parts = [BRIGHT + ACCENT + clock + RESET]
    if test.started and elapsed >= 1:
        if settings["live_wpm"]:
            parts.append(BRIGHT + "%d" % round(test.wpm(now)) + RESET + DIM + " wpm" + RESET)
        acc = test.accuracy()
        parts.append(acc_color(acc) + "%d %%" % round(acc) + RESET)
    if mode.kind == "text" and getattr(mode, "count_words", False):
        parts.append(DIM + "%d/%d" % (test.words_done(), test.words_total()) + RESET)
    elif mode.kind == "free":
        parts.append(DIM + words_label(test.words_done()) + RESET)
    elif mode.kind == "endless":
        parts.append(ACCENT + BRIGHT + "Level %d" % state["level"] + RESET)
        parts.append(BRIGHT + "%d" % state["words"] + RESET + DIM + tr(" Wörter", " words") + RESET)
    stat_line = (DIM + "   " + RESET).join(parts)
    if not test.started:
        stat_line += DIM + tr("   Tipp einfach los.", "   Just start typing.") + RESET

    label_line = DIM + mode.label + RESET
    if settings["strict"]:
        label_line += DIM + tr(" · Fehler korrigieren", " · fix mistakes") + RESET

    if mode.kind == "free":
        footer = tr("Esc beenden & speichern · Tab neuer Text", "Esc finish & save · Tab new text")
    elif mode.kind == "endless":
        footer = tr("Richtige Wörter bringen Zeit, Fehler kosten 1 s · Esc aufgeben · Tab neu",
                    "Correct words add time, mistakes cost 1 s · Esc give up · Tab restart")
    else:
        footer = tr("Tab neu starten · Esc Menü", "Tab restart · Esc menu")

    if progress is None:  # freier Modus: Linie fließt einfach
        line = ui.flow_line(width, 1.0, speed=0.15)
    else:
        line = ui.flow_line(width, progress)

    lines = [margin + label_line, margin + stat_line, margin + line, ""] + text_lines
    if note:
        lines += ["", margin + DIM + note + RESET]

    if settings.get("keyboard", True) and rows >= 20:
        next_char = test.target[test.pos] if test.pos < len(test.target) else None
        kb, hint = live_keyboard(settings["kb_layout"], next_char, flash)
        # Mitte der Grundreihe (A … #) genau unter die Mitte des Textes setzen
        home = keyboard.layout(settings["kb_layout"])[2]
        home_center = (home[0][0] + home[-1][0] + home[-1][3]) / 2
        text_center = len(margin) + width / 2
        kb_margin = " " * max(0, int(round(text_center - home_center)))
        room = rows - 2 - len(lines)
        if room >= len(kb) + 3:
            lines += [""] * (3 if room >= len(kb) + 8 else 1)
            lines += [kb_margin + k for k in kb]
            lines += [""] if room >= len(kb) + 6 else []
            lines.append(" " * max(0, int(round(text_center - len(hint) / 2))) + DIM + hint + RESET)

    top = max(0, (rows - len(lines) - 2) // 2)
    screen = [""] * top + lines
    screen = screen[:rows - 2]
    while len(screen) < rows - 2:
        screen.append("")
    screen.append(margin + DIM + footer + RESET)
    draw(term, screen)


# --- Ergebnis -----------------------------------------------------------------

def record_text(entry):
    if "score" in entry:
        return words_label(entry["score"])
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
        tr("Roh ", "Raw ") + BRIGHT + fmt_num(result["raw"]) + RESET + DIM + " WPM" + RESET,
        tr("Konstanz ", "Consistency ") + BRIGHT + "%d %%" % result["consistency"] + RESET,
        tr("Zeichen ", "Characters ") + GOOD + "%d" % result["chars"] + RESET + DIM + " / " + RESET
        + BAD + "%d" % result["errors"] + RESET,
        tr("Zeit ", "Time ") + BRIGHT + fmt_num(result["duration"], 1) + " s" + RESET,
    ]
    lines.append((DIM + "  ·  " + RESET).join(details))
    entry = info.get("entry") or {}
    if mode.kind == "endless" and "score" in entry:
        lines.append(tr("Geschafft ", "Made it ") + GOLD + words_label(entry["score"]) + RESET
                     + DIM + "  ·  " + RESET + tr("erreicht ", "reached ") + ACCENT + BRIGHT
                     + "Level %d" % entry["level"] + RESET + DIM + "  ·  " + RESET
                     + tr("überlebt ", "survived ") + BRIGHT + fmt_clock(result["duration"]) + RESET)

    series = result["wpm_series"]
    if len(series) >= 3:
        smooth = [sum(series[max(0, i - 2):i + 1]) / len(series[max(0, i - 2):i + 1])
                  for i in range(len(series))]
        lines.append(tr("Verlauf ", "Speed ") + ACCENT + sparkline(smooth, width - 20) + RESET
                     + DIM + "  %d–%d WPM" % (min(smooth), max(smooth)) + RESET)
    lines.append("")

    if not info.get("saved"):
        lines.append(WARN + tr("Zu kurz – dieser Test wurde nicht gespeichert.",
                               "Too short – this test was not saved.") + RESET)
    else:
        prev = info.get("previous")
        if info.get("record") and prev:
            lines.append(GOLD + tr("★ NEUER REKORD! ", "★ NEW RECORD! ") + RESET + DIM
                         + tr("(vorher %s)", "(before: %s)") % record_text(prev) + RESET)
        elif info.get("record"):
            lines.append(GOLD + tr("★ Erster Eintrag in diesem Modus – das ist dein Rekord.",
                                   "★ First result in this mode – that's your record.") + RESET)
        elif prev:
            lines.append(DIM + tr("Rekord in diesem Modus: %s", "Record in this mode: %s")
                         % record_text(prev) + RESET)
        for key in info.get("achievements", []):
            lines.append(GOLD + tr("✓ Erfolg freigeschaltet: ", "✓ Achievement unlocked: ") + RESET
                         + BRIGHT + stats.achievement_text(key)[0] + RESET)

    errors = sorted(result["key_errors"].items(), key=lambda kv: -kv[1])[:6]
    if errors:
        shown = "  ".join(BAD + ("␣" if ch == " " else ch) + RESET + DIM + " ×%d" % n + RESET
                          for ch, n in errors)
        lines.append(tr("Fehler bei ", "Mistakes on ") + shown)

    goal = store.settings["daily_goal"] * 60
    done = stats.daily_seconds(store.history).get(date.today(), 0)
    reached = done >= goal
    lines.append(tr("Tagesziel ", "Daily goal ") + progress_bar(done / goal, 16, GOOD if reached else ACCENT)
                 + " %s/%d min" % (fmt_minutes(done), goal // 60)
                 + (GOOD + tr("  ✓ geschafft!", "  ✓ done!") + RESET if reached else ""))
    return lines


def result_screen(term, mode, result, info, store):
    """Zeigt das Ergebnis. Gibt "next", "repeat" oder "menu" zurück."""
    footer = tr("Enter nächster Test", "Enter next test")
    if mode.repeatable:
        footer += tr(" · R gleichen Text wiederholen", " · R repeat same text")
    footer += tr(" · Esc Menü", " · Esc menu")
    term.flush_input()
    shown_at = time.monotonic()
    while True:
        width = content_width(term)
        lines = title_block(tr("Ergebnis", "Result"), width=width) + result_lines(mode, result, info, store, width)
        draw(term, frame(term, lines, footer))
        key = term.read_key(ui.tick())
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
        return [DIM + tr("Noch keine Tests – leg los!", "No tests yet – get started!") + RESET]
    today = date.today()
    days = stats.daily_seconds(history)
    tests_today = stats.daily_tests(history).get(today, 0)
    current, longest = stats.streaks(days, today)
    last10 = history[-10:]
    best = stats.best_entry(history)
    week_start = today - timedelta(days=today.weekday())
    week = sum(v for d, v in days.items() if d >= week_start)
    total_chars = sum(e.get("chars", 0) for e in history)

    days_label = tr("%d Tage", "%d days")
    rows = [
        (tr("Tests gesamt", "Total tests"), fmt_num(len(history))),
        (tr("Übungszeit gesamt", "Total practice time"), fmt_duration(sum(days.values()))),
        (tr("Richtig getippte Zeichen", "Correct characters"), fmt_num(total_chars)),
        (tr("Ø Tempo (letzte 10)", "Avg speed (last 10)"),
         "%s WPM" % fmt_num(stats.average(e["wpm"] for e in last10))),
        (tr("Ø Genauigkeit (letzte 10)", "Avg accuracy (last 10)"),
         "%s %%" % fmt_num(stats.average(e["acc"] for e in last10), 1)),
        (tr("Ø Tempo (alle)", "Avg speed (all)"), "%s WPM" % fmt_num(stats.average(e["wpm"] for e in history))),
    ]
    if best:
        rows.append((tr("Bestes Tempo", "Best speed"), "%d WPM  %s(%s, %s)%s" % (
            round(best["wpm"]), DIM, best.get("label", best["mode"]),
            fmt_date(stats.entry_date(best)), RESET)))
    rows += [
        (tr("Aktive Tage", "Active days"), fmt_num(len(days))),
        (tr("Aktuelle Serie", "Current streak"), days_label % current),
        (tr("Längste Serie", "Longest streak"), days_label % longest),
        (tr("Heute", "Today"), "%s · %d Tests" % (fmt_duration(days.get(today, 0)), tests_today)),
        (tr("Diese Woche", "This week"), fmt_duration(week)),
    ]
    return [DIM + pad(name, 28) + RESET + BRIGHT + value + RESET for name, value in rows]


def records_lines(store, width):
    best = stats.records(store.history)
    if not best:
        return [DIM + tr("Noch keine Rekorde.", "No records yet.") + RESET]
    label_w = min(40, max(vlen(e.get("label", k)) for k, e in best.items()) + 2)
    lines = [DIM + pad(tr("Modus", "Mode"), label_w) + pad(tr("Rekord", "Record"), 12)
             + pad(tr("Genauigkeit", "Accuracy"), 14) + tr("Datum", "Date") + RESET]
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
        return [DIM + tr("Noch kein Verlauf.", "No history yet.") + RESET]
    count = max(5, width - 8)
    recent = history[-count:]
    wpms = [e["wpm"] for e in recent]
    lines = [DIM + tr("Tempo der letzten %d Tests (WPM)", "Speed of the last %d tests (WPM)")
             % len(recent) + RESET, ""]
    lines += bar_chart(wpms, 8)
    lines.append("")
    accs = [e["acc"] for e in recent]
    lines.append(DIM + tr("Genauigkeit  ", "Accuracy  ") + RESET + GOOD + sparkline([max(0, a - 80) for a in accs]) + RESET
                 + DIM + "  (80–100 %)" + RESET)
    last10 = stats.average(e["wpm"] for e in history[-10:])
    lines.append("")
    summary = tr("Ø letzte 10: ", "Avg last 10: ") + BRIGHT + fmt_num(last10) + RESET
    if len(history) >= 20:
        before = stats.average(e["wpm"] for e in history[-20:-10])
        diff = last10 - before
        arrow = (GOOD + "▲ +" if diff >= 0 else BAD + "▼ ") + fmt_num(diff, 1) + " WPM" + RESET
        summary += DIM + "  ·  Trend " + RESET + arrow
    if len(history) >= 50:
        summary += DIM + tr("  ·  Ø letzte 50: ", "  ·  Avg last 50: ") + RESET + fmt_num(stats.average(e["wpm"] for e in history[-50:]))
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
    lang = store.settings["kb_layout"]
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

    lines = [DIM + tr("Fehlerquote je Taste (Umschalt- und AltGr-Zeichen zählen zur Grundtaste)",
                      "Error rate per key (shifted and AltGr characters count for the base key)")
             + RESET, ""]
    for row, indent in KEYBOARDS[lang]:
        cells = [_key_color(rate(k)) + " " + (k.upper() if len(k.upper()) == 1 else k) + " " + RESET
                 for k in row]
        lines.append(" " * indent + " ".join(cells))
    space_rate = rate(" ")
    lines.append(" " * 12 + _key_color(space_rate) + " " * 22 + RESET + DIM
                 + tr("  Leertaste", "  space") + RESET)
    lines.append("")
    lines.append(_key_color(0.0) + " < 3 % " + RESET + " " + _key_color(0.05) + " < 7 % " + RESET + " "
                 + _key_color(0.1) + " < 12 % " + RESET + " " + _key_color(0.5) + " ≥ 12 % " + RESET
                 + " " + DIM + tr("grau = zu wenig Daten", "gray = not enough data") + RESET)
    lines.append("")
    weak = stats.weak_keys(store.key_stats, count=8, min_attempts=10, include_space=True)
    if weak:
        lines.append(DIM + tr("Schwächste Tasten", "Weakest keys") + RESET)
        for ch, attempts, errors, r in weak:
            name = tr("Leertaste", "space") if ch == " " else ch
            lines.append("  " + BAD + BRIGHT + pad(name, 10) + RESET
                         + progress_bar(min(1, r * 4), 12, BAD)
                         + " %s %%  %s(%d %s %d)%s" % (fmt_num(r * 100, 1), DIM, errors,
                                                       tr("von", "of"), attempts, RESET))
    else:
        lines.append(DIM + tr("Noch zu wenig Daten für eine Auswertung.", "Not enough data yet.") + RESET)
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
        footer = tr("←→ Bereich wechseln", "←→ switch tab")
        if len(body) > room:
            footer += tr(" · ↑↓ scrollen", " · ↑↓ scroll")
        footer += tr(" · Esc zurück", " · Esc back")
        draw(term, frame(term, lines, footer, width))
        key = term.read_key(ui.tick())
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
        (tr("Übersicht", "Overview"), lambda w: overview_lines(store, w)),
        (tr("Rekorde", "Records"), lambda w: records_lines(store, w)),
        (tr("Verlauf", "History"), lambda w: history_lines(store, w)),
        (tr("Tastatur", "Keyboard"), lambda w: keyboard_lines(store, w)),
    ]
    tab_screen(term, tr("Statistik & Rekorde", "Stats & records"), tabs)


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
            name = months()[month - 1]
            pos = col * 2
            if pos >= free_from and pos + len(name) <= len(label_row):
                label_row[pos:pos + len(name)] = list(name)
                free_from = pos + len(name) + 1
            prev_month = month
    lines = [DIM + "    " + "".join(label_row).rstrip() + RESET]

    for row in range(7):
        name = weekdays()[row] if row in (0, 2, 4, 6) else ""
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
    lines.append(DIM + tr("    Weniger ", "    Less ") + RESET + legend + DIM + tr(" Mehr", " More") + RESET)
    lines.append(DIM + tr("    Stufen: unter ½ Tagesziel · unter Tagesziel · Ziel erreicht · doppeltes Ziel",
                          "    Levels: under ½ daily goal · under goal · goal reached · double goal")
                 + RESET)
    lines.append("")

    in_range = [d for d in days if start <= d <= end]
    current, longest = stats.streaks(days, today)
    lines.append(tr("Zeitraum ", "Period ") + BRIGHT + "%s – %s" % (fmt_date(start), fmt_date(end)) + RESET)
    lines.append(BRIGHT + "%d" % len(in_range) + RESET + tr(" aktive Tage  ·  ", " active days  ·  ")
                 + BRIGHT + fmt_duration(sum(days[d] for d in in_range)) + RESET
                 + tr(" Übung  ·  ", " practice  ·  ")
                 + BRIGHT + "%d" % sum(tests.get(d, 0) for d in in_range) + RESET + " Tests")
    lines.append(tr("Aktuelle Serie ", "Current streak ") + GOLD + "%d" % current + RESET
                 + tr("  ·  Längste Serie ", "  ·  Longest streak ") + BRIGHT + "%d" % longest + RESET
                 + tr("  ·  Tagesziel %d min", "  ·  Daily goal %d min") % (goal // 60))

    week_start = today - timedelta(days=today.weekday())
    week = []
    for i in range(7):
        d = week_start + timedelta(days=i)
        if d > today:
            week.append(DIM + weekdays()[i] + " –" + RESET)
        else:
            minutes = days.get(d, 0) / 60
            color = GOOD if days.get(d, 0) >= goal else TEXT if minutes else DIM
            week.append(DIM + weekdays()[i] + " " + RESET + color + fmt_num(minutes) + RESET)
    lines.append(tr("Diese Woche (min)  ", "This week (min)  ") + "  ".join(week))
    return lines


def activity_screen(term, store):
    offset = 0
    while True:
        width = content_width(term, 112)
        lines = title_block(tr("Aktivität", "Activity"),
                            tr("an welchen Tagen du geübt hast", "the days you practiced"), width)
        lines += [""] + activity_lines(store, width, offset)
        footer = tr("←→ Zeitraum verschieben · Esc zurück", "←→ move period · Esc back")
        draw(term, frame(term, lines, footer, width))
        key = term.read_key(ui.tick())
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
        lines = title_block(tr("Erfolge", "Achievements"),
                            tr("%d von %d freigeschaltet", "%d of %d unlocked") % (got, total), width)
        lines.append(progress_bar(got / total, min(40, width), GOLD))
        lines.append("")
        body = []
        for key, _, _ in stats.ACHIEVEMENTS:
            name, desc = stats.achievement_text(key)
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
        footer = (tr("↑↓ scrollen · ", "↑↓ scroll · ") if len(body) > room else "") + tr("Esc zurück", "Esc back")
        draw(term, frame(term, lines, footer))
        key = term.read_key(ui.tick())
        if key in (T.DOWN, "j"):
            scroll += 1
        elif key in (T.UP, "k"):
            scroll = max(0, scroll - 1)
        elif key in (T.ESC, T.ENTER, "q", T.CTRL_C):
            return


# --- Einstellungen ------------------------------------------------------------

def settings_ui():
    """(Schlüssel, Name, Anzeige des Werts, Hinweis); None = Abstand."""
    return (
        ("ui_language", tr("Sprache", "Language"), {"en": "English", "de": "Deutsch"},
         tr("Sprache von KeyFlow und der Übungstexte.", "Language of KeyFlow and of the practice texts.")),
        ("language", tr("Sprache der Texte", "Text language"),
         {"de": tr("Deutsch", "German"), "en": tr("Englisch", "English")},
         tr("Sprache für Wörter, Sätze, Zitate und Geschichten. Rekorde werden je Sprache geführt.",
            "Language of words, sentences, quotes and stories. Records are kept per language.")),
        ("kb_layout", tr("Tastaturlayout", "Keyboard layout"),
         {"de": tr("QWERTZ (Deutsch)", "QWERTZ (German)"), "en": "QWERTY (US)"},
         tr("Welche Tastatur beim Tippen angezeigt wird.", "Which keyboard is shown while you type.")),
        ("difficulty", tr("Wortlänge", "Word length"),
         {"easy": tr("kurze Wörter", "short words"), "normal": tr("gemischt", "mixed"),
          "hard": tr("lange Wörter", "long words")},
         tr("Welche Wörter in Zeit-, Wörter- und freien Tests vorkommen.",
            "Which words appear in time, word and free tests.")),
        ("punctuation", tr("Satzzeichen", "Punctuation"), on_off,
         tr("Fügt in Zeit-, Wörter- und freien Tests Kommas, Punkte, Klammern … ein.",
            "Adds commas, periods, brackets … to time, word and free tests.")),
        ("numbers", tr("Zahlen", "Numbers"), on_off,
         tr("Mischt in Zeit-, Wörter- und freien Tests Zahlen unter die Wörter.",
            "Mixes numbers into time, word and free tests.")),
        ("lowercase", tr("Nur Kleinbuchstaben", "Lowercase only"), on_off,
         tr("Schreibt alle Wörter klein (Satzanfänge bleiben groß).",
            "Writes all words in lowercase (sentence starts stay capitalized).")),
        ("umlauts", tr("Umlaute & ß", "Umlauts & ß"),
         {True: tr("tippen", "type them"), False: tr("ersetzen (ae, oe, ue, ss)", "replace (ae, oe, ue, ss)")},
         tr("Praktisch, wenn deine Tastatur keine deutschen Umlaute hat.",
            "Handy if your keyboard has no German umlauts.")),
        ("strict", tr("Fehler", "Mistakes"),
         {False: tr("weitertippen erlaubt", "keep typing"), True: tr("müssen korrigiert werden", "must be fixed")},
         tr("Im strengen Modus geht es erst weiter, wenn das richtige Zeichen getippt ist.",
            "In strict mode you only move on once the correct character is typed.")),
        None,
        ("live_wpm", tr("Live-WPM anzeigen", "Show live WPM"), on_off,
         tr("Zeigt das Tempo schon während des Tippens.", "Shows your speed while you type.")),
        ("cursor", "Cursor", {"block": "Block", "underline": tr("Unterstrich", "Underline")},
         tr("Wie die aktuelle Stelle markiert wird.", "How the current position is marked.")),
        ("visible_lines", tr("Sichtbare Zeilen", "Visible lines"), str,
         tr("Wie viele Textzeilen gleichzeitig zu sehen sind.", "How many lines of text are visible.")),
        ("text_width", tr("Textbreite", "Text width"), lambda v: tr("%d Zeichen", "%d characters") % v,
         tr("Maximale Breite einer Textzeile.", "Maximum width of a line of text.")),
        ("bell", tr("Ton bei Fehlern", "Sound on mistakes"), on_off,
         tr("Lässt bei jedem Tippfehler die Terminal-Glocke klingen.", "Rings the terminal bell on every mistake.")),
        ("background", tr("Hintergrund", "Background"), lambda v: pick(ui.BACKGROUNDS[v][0]),
         tr("Färbt das Terminal beim Start ein – beim Beenden kommt dein Hintergrund zurück.",
            "Colors the terminal on start – your own background returns when you quit.")),
        ("glass_opacity", tr("Glas-Deckkraft", "Glass opacity"), lambda v: "%d %%" % v,
         tr("Wie undurchsichtig der Glas-Hintergrund ist. Mehr = besser lesbar vor hellen Fenstern.",
            "How opaque the glass background is. Higher = easier to read over bright windows.")),
        ("color_mode", tr("Farbmodus", "Color mode"),
         {"256": tr("256 Farben", "256 colors"), "truecolor": "True Color",
          "basic": tr("Basis (16 Farben)", "Basic (16 colors)")},
         tr("True Color ist am schönsten. Falls Farben komisch aussehen, nimm 256 Farben.",
            "True Color looks best. If colors look odd, use 256 colors.")),
        ("animations", tr("Bewegte Farben", "Moving colors"), on_off,
         tr("Fließende Farbverläufe und leuchtende Tasten.", "Flowing gradients and glowing keys.")),
        ("keyboard", tr("Tastatur beim Tippen", "Keyboard while typing"), on_off,
         tr("Zeigt unter dem Text eine Tastatur, auf der die nächste Taste leuchtet.",
            "Shows a keyboard under the text where the next key lights up.")),
        ("check_updates", tr("Nach Updates suchen", "Check for updates"), on_off,
         tr("Fragt beim Start bei PyPI nach, ob es eine neue Version gibt.",
            "Asks PyPI on start whether a new version is available.")),
        None,
        ("daily_goal", tr("Tagesziel", "Daily goal"), lambda v: "%d min" % v,
         tr("Wie lange du pro Tag üben möchtest. Bestimmt auch die Kalenderfarben.",
            "How long you want to practice per day. Also sets the calendar colors.")),
    )


LOOK_SETTINGS = ("background", "glass_opacity", "color_mode", "animations")


def settings_screen(term, store, on_look_change=None, on_language_change=None):
    settings = store.settings
    index = 0
    while True:
        def setter(key):
            def change(value):
                settings[key] = value
                store.save()
                if key == "ui_language" and on_language_change:
                    on_language_change(value)
                if key in LOOK_SETTINGS and on_look_change:
                    on_look_change()
            return change

        items = []
        for entry in settings_ui():
            if entry is None:
                items.append(Item.sep())
                continue
            key, label, fmt, hint = entry
            items.append(Item(label, options=storage.SETTING_OPTIONS[key], value=settings[key],
                              fmt=fmt, on_change=setter(key), hint=hint,
                              refresh=key == "ui_language"))
        items += [
            Item.sep(),
            Item(tr("Statistiken zurücksetzen", "Reset statistics"), action="reset",
                 hint=tr("Löscht Verlauf, Rekorde, Tastenstatistik und Erfolge. Eigene Texte bleiben.",
                         "Deletes history, records, key stats and achievements. Your own texts stay.")),
            Item(tr("Zurück", "Back"), action="back"),
        ]
        width = content_width(term)
        action, index, _ = run_menu(
            term, lambda: title_block(tr("Einstellungen", "Settings"),
                                      tr("Datei: %s", "File: %s") % store.path, width), items, index,
            footer=tr("↑↓ auswählen · ←→/Enter ändern · Esc zurück", "↑↓ choose · ←→/Enter change · Esc back"),
            width=width)
        if action == ui.REFRESH:
            continue
        if action == "reset":
            if confirm(term, tr("Statistiken zurücksetzen", "Reset statistics"),
                       tr("Wirklich den gesamten Verlauf, alle Rekorde und Erfolge löschen?",
                          "Really delete your whole history, all records and achievements?")):
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
    lang = store.settings["language"]
    items_list = stories.stories_for(lang, level)
    for i, (title, text) in enumerate(items_list):
        sid = stories.story_id(level, i)
        mark = (GOOD + "✓ " + RESET + DIM + "%d WPM · " % round(best[sid])) if sid in best \
            else DIM + tr("neu · ", "new · ")
        items.append(Item("%2d. %s" % (i + 1, title), action=i,
                          right=mark + tr("%d Zeichen", "%d chars") % len(text) + RESET,
                          hint=text[:66] + " …"))
    items += [Item.sep(), Item(tr("Zurück", "Back"), action="back")]
    done = sum(1 for i in range(len(items_list)) if stories.story_id(level, i) in best)
    width = content_width(term)

    def header():
        return title_block(tr("Geschichten – %s", "Stories – %s") % stories.level_label(level),
                           tr("%d von %d geschafft", "%d of %d done") % (done, len(items_list)), width)
    return run_menu(term, header, items, index,
                    footer=tr("↑↓ auswählen · Enter tippen · Esc zurück", "↑↓ choose · Enter type · Esc back"),
                    width=width)


# --- Eigene Texte -------------------------------------------------------------

def custom_menu(term, store, index=0):
    items = []
    for i, entry in enumerate(store.custom_texts):
        text = entry["text"]
        right = tr("%s Zeichen", "%s chars") % fmt_num(len(text))
        if len(text) > 600:
            right += " · %d %%" % (100 * entry.get("pos", 0) // len(text))
        title = entry.get("title") or text[:30]
        items.append(Item(title[:34], action=i, right=right,
                          hint=tr("Enter üben · Entf/D löschen", "Enter practice · Del/D delete")))
    if items:
        items.append(Item.sep())
    items += [
        Item(tr("+ Text einfügen", "+ Paste text"), action="new",
             hint=tr("Text aus der Zwischenablage einfügen.", "Paste a text from the clipboard.")),
        Item(tr("+ Aus Datei laden", "+ Load from file"), action="file",
             hint=tr("Eine .txt-Datei laden (UTF-8).", "Load a .txt file (UTF-8).")),
        Item(tr("Zurück", "Back"), action="back"),
    ]
    width = content_width(term)
    def header():
        return title_block(tr("Eigener Text", "Your own text"),
                           tr("lange Texte werden in Abschnitten geübt", "long texts are practiced in parts"), width)
    return run_menu(term, header, items, index,
                    footer=tr("↑↓ auswählen · Enter üben · Entf/D löschen · Esc zurück",
                              "↑↓ choose · Enter practice · Del/D delete · Esc back"),
                    extra_keys=(T.DELETE, "d", "D"), width=width)


# --- Sprache beim ersten Start -------------------------------------------------

def language_picker(term):
    """Fragt beim allerersten Start nach der Sprache. Gibt "en" oder "de" zurück."""
    items = [Item("English", action="en", hint="KeyFlow will be in English."),
             Item("Deutsch", action="de", hint="KeyFlow wird auf Deutsch sein.")]
    width = content_width(term)

    def header():
        return [ui.gradient(TITLE) + DIM + "  made by YnsLaf" + RESET,
                DIM + "─" * width + RESET, "",
                BRIGHT + "Choose your language" + RESET + DIM + "  ·  " + RESET
                + BRIGHT + "Wähle deine Sprache" + RESET, ""]

    while True:
        action, _, _ = run_menu(term, header, items, 0, numbered=True,
                                footer="↑↓ · Enter", width=width)
        if action in ("en", "de"):
            return action


# --- Info -----------------------------------------------------------------------

def update_status_line(updater):
    status = updater.status if updater is not None else "off"
    if status == "checking":
        spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"[int(time.monotonic() * 10) % 10]
        return DIM + spinner + tr(" Suche nach Updates …", " Checking for updates …") + RESET
    if status == "available":
        return GOLD + tr("⬆ Update verfügbar: %s → %s", "⬆ Update available: %s → %s") % (
            __version__, updater.latest) + RESET
    if status == "current":
        return GOOD + tr("✓ Du hast die neueste Version.", "✓ You have the latest version.") + RESET
    if status == "unpublished":
        return DIM + tr("Noch nicht auf PyPI veröffentlicht.", "Not published on PyPI yet.") + RESET
    if status == "offline":
        return WARN + tr("Update-Suche nicht möglich (offline?).", "Could not check for updates (offline?).") \
            + RESET
    return DIM + tr("Update-Suche ist ausgeschaltet.", "Update check is turned off.") + RESET


def info_header(store, updater, width):
    system = {"darwin": "macOS", "win32": "Windows"}.get(sys.platform, platform.system() or sys.platform)
    method = {"pipx": "pipx", "pip": "pip", "source": tr("Quellcode (git)", "source code (git)")}[
        updates.install_method()]
    label_w = 14
    rows = [
        (tr("Version", "Version"), BRIGHT + "KeyFlow " + __version__ + RESET),
        (tr("Updates", "Updates"), update_status_line(updater)),
        (tr("Installiert", "Installed"), method + DIM + "  ·  " + tr("Update-Befehl: ", "update command: ")
         + updates.update_command_text() + RESET),
        ("Python", "%d.%d.%d" % sys.version_info[:3] + DIM + "  ·  " + system + RESET),
        (tr("Daten", "Data"), DIM + str(store.path) + RESET),
    ]
    lines = title_block("Info", tr("alles über KeyFlow", "all about KeyFlow"), width)
    lines += [DIM + pad(name, label_w) + RESET + value for name, value in rows]
    lines += [
        "",
        BRIGHT + tr("Über mich", "About me") + RESET,
        tr("KeyFlow wird von ", "KeyFlow is made by ") + ui.gradient("YnsLaf")
        + tr(" gebaut – ein Tipptrainer, der", " – a typing trainer that is fun,"),
        tr("direkt im Terminal Spaß macht. Ideen, Fehler oder Wünsche?",
           "right in the terminal. Ideas, bugs or wishes?"),
        tr("Schreib mir auf GitHub.", "Reach me on GitHub."),
        "",
        DIM + "GitHub  " + RESET + ACCENT + ui.link(updates.GITHUB_USER_URL, "github.com/YnsLaf") + RESET
        + DIM + "   ·   " + RESET + ACCENT + ui.link(updates.GITHUB_REPO_URL, "github.com/YnsLaf/keyflow") + RESET,
        DIM + "PyPI    " + RESET + ACCENT + ui.link(updates.PROJECT_URL, "pypi.org/project/keyflow-typing") + RESET,
        "",
    ]
    return lines


def info_screen(term, store, updater, index=0):
    """Gibt die gewählte Aktion zurück: github, repo, pypi, update, check oder None."""
    width = content_width(term)
    available = updater is not None and updater.available
    items = [
        Item(tr("Mein GitHub öffnen", "Open my GitHub"), action="github",
             hint=tr("Öffnet github.com/YnsLaf im Browser.", "Opens github.com/YnsLaf in your browser.")),
        Item(tr("KeyFlow auf GitHub", "KeyFlow on GitHub"), action="repo",
             hint=tr("Quellcode, Anleitung und Neuigkeiten.", "Source code, docs and news.")),
        Item(tr("KeyFlow auf PyPI", "KeyFlow on PyPI"), action="pypi",
             hint=tr("Die Paketseite mit allen Versionen.", "The package page with all versions.")),
        Item(tr("Jetzt aktualisieren", "Update now") if available else tr("Nach Updates suchen", "Check for updates"),
             action="update" if available else "check",
             hint=(tr("Führt aus: ", "Runs: ") + updates.update_command_text()) if available
             else tr("Fragt PyPI nach der neuesten Version.", "Asks PyPI for the latest version.")),
        Item.sep(),
        Item(tr("Zurück", "Back"), action="back"),
    ]
    action, index, _ = run_menu(term, lambda: info_header(store, updater, width), items, index,
                                numbered=True, width=width,
                                footer=tr("↑↓ wählen · Enter öffnen · Esc zurück", "↑↓ choose · Enter open · Esc back"))
    return action, index
