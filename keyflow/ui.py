"""Farben, Layout-Helfer und wiederverwendbare Bausteine wie das Menü."""

import colorsys
import math
import re
import time

from colorama import Back, Fore, Style

from . import terminal as T

RESET = Style.RESET_ALL
BRIGHT = Style.BRIGHT
TEXT = Fore.WHITE
DIM = Fore.LIGHTBLACK_EX
ACCENT = Fore.CYAN
GOOD = Fore.GREEN
BAD = Fore.RED
WARN = Fore.YELLOW
GOLD = Style.BRIGHT + Fore.YELLOW
UNDERLINE = "\x1b[4m"
REVERSE = "\x1b[7m"

_ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")

# Aktueller Farbmodus und ob sich Farben bewegen (wird aus den Einstellungen gesetzt).
STYLE = {"color": "256", "animate": True}

# Hintergründe, die KeyFlow beim Start ins Terminal setzt: (Name, RGB, Deckkraft).
# Deckkraft None = die Deckkraft des Terminal-Profils bleibt, wie sie ist.
# "glas": Farbton 0°, Sättigung 0 %, Helligkeit 10 %, Deckkraft 30 %.
BACKGROUNDS = {
    "glas": ("Glas (yns.laf)", (26, 26, 26), 0.30),   # im Mac-Terminal: Profil bleibt
    "mitternacht": ("Mitternacht", (13, 17, 23), None),
    "graphit": ("Graphit", (24, 24, 27), None),
    "ozean": ("Ozean", (8, 24, 38), None),
    "wald": ("Wald", (12, 28, 20), None),
    "aubergine": ("Aubergine", (28, 14, 34), None),
    "schwarz": ("Schwarz", (0, 0, 0), None),
    "aus": ("wie im Terminal", None, None),
}


def configure(settings):
    STYLE["color"] = settings.get("color_mode", "256")
    STYLE["animate"] = settings.get("animations", True)


def tick():
    """Wie lange auf eine Taste gewartet wird, bevor neu gezeichnet wird."""
    return 0.08 if STYLE["animate"] else 0.5


def clock():
    """Zeit für Animationen; ohne Animationen bleibt sie stehen."""
    return time.monotonic() if STYLE["animate"] else 0.0


_CUBE = (0, 95, 135, 175, 215, 255)


def _cube_index(v):
    return min(range(6), key=lambda i: abs(_CUBE[i] - v))


def rgb_to_256(rgb):
    """Nächstliegende Farbe der 256er-Palette (Farbwürfel oder Graustufe)."""
    r, g, b = rgb
    ci = (_cube_index(r), _cube_index(g), _cube_index(b))
    cube = tuple(_CUBE[i] for i in ci)
    level = min(23, max(0, int(round((sum(rgb) / 3 - 8) / 10))))
    gray = 8 + level * 10

    def dist(c):
        return sum((x - y) ** 2 for x, y in zip(rgb, c))

    if dist((gray, gray, gray)) < dist(cube):
        return 232 + level
    return 16 + 36 * ci[0] + 6 * ci[1] + ci[2]


def _basic(rgb, background):
    h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
    if s < 0.25:
        names = ("BLACK", "LIGHTBLACK_EX", "WHITE", "LIGHTWHITE_EX")
        name = names[min(3, int(v * 4))]
    else:
        names = ("RED", "YELLOW", "GREEN", "CYAN", "BLUE", "MAGENTA")
        name = names[int(((h + 1 / 12) % 1) * 6)]
        if v > 0.7 and not background:
            name = "LIGHT" + name + "_EX"
    return getattr(Back if background else Fore, name)


def fg(rgb):
    mode = STYLE["color"]
    if mode == "truecolor":
        return "\x1b[38;2;%d;%d;%dm" % tuple(rgb)
    if mode == "256":
        return "\x1b[38;5;%dm" % rgb_to_256(rgb)
    return _basic(rgb, False)


def bg(rgb):
    mode = STYLE["color"]
    if mode == "truecolor":
        return "\x1b[48;2;%d;%d;%dm" % tuple(rgb)
    if mode == "256":
        return "\x1b[48;5;%dm" % rgb_to_256(rgb)
    return _basic(rgb, True)


def hsv(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


def mix(a, b, f):
    return tuple(int(x + (y - x) * f) for x, y in zip(a, b))


def pulse(speed=3.0):
    """Wert zwischen 0 und 1, der langsam hin und her schwingt."""
    return (math.sin(clock() * speed) + 1) / 2


def gradient(text, speed=0.12, spread=0.035, base=0.5, s=0.55, v=1.0, bold=True):
    """Text mit fließendem Farbverlauf."""
    t = clock()
    out = [BRIGHT] if bold else []
    for i, ch in enumerate(text):
        if ch == " ":
            out.append(ch)
        else:
            out.append(fg(hsv(base + i * spread + t * speed, s, v)) + ch)
    return "".join(out) + RESET


def flow_line(width, fraction, speed=0.25):
    """Fortschrittslinie, deren gefüllter Teil in bewegten Farben fließt."""
    fraction = max(0.0, min(1.0, fraction))
    full = int(round(width * fraction))
    t = clock()
    parts = [fg(hsv(0.5 + i * 0.012 - t * speed, 0.6, 1.0)) + "━" for i in range(full)]
    return "".join(parts) + fg((60, 64, 72)) + "─" * (width - full) + RESET


SOFT = "\x1b[38;5;250m"   # ruhiges Grau für nicht ausgewählte Einträge


def strip_ansi(text):
    return _ANSI.sub("", text)


def vlen(text):
    """Sichtbare Länge (ohne Farbcodes)."""
    return len(strip_ansi(text))


def pad(text, width):
    return text + " " * max(0, width - vlen(text))


def clip(text, width):
    """Kürzt auf width sichtbare Zeichen, Farbcodes bleiben erhalten."""
    out, visible, i = [], 0, 0
    while i < len(text):
        m = _ANSI.match(text, i)
        if m:
            out.append(m.group())
            i = m.end()
            continue
        if visible < width:
            out.append(text[i])
            visible += 1
        i += 1
    return "".join(out)


def fmt_num(value, digits=0):
    """Zahl im deutschen Format: 12.345,6"""
    text = "{:,.{}f}".format(value, digits)
    return text.replace(",", "\0").replace(".", ",").replace("\0", ".")


def fmt_minutes(seconds):
    minutes = seconds / 60
    return fmt_num(minutes, 1 if 0 < minutes < 10 else 0)


def fmt_duration(seconds):
    seconds = int(round(seconds))
    if seconds < 60:
        return "%d s" % seconds
    minutes = seconds // 60
    if minutes < 60:
        return "%d min" % minutes
    return "%d h %02d min" % (minutes // 60, minutes % 60)


def fmt_clock(seconds):
    seconds = int(seconds)
    return "%d:%02d" % (seconds // 60, seconds % 60)


def fmt_date(d):
    return d.strftime("%d.%m.%Y")


def acc_color(acc):
    return GOOD if acc >= 97 else WARN if acc >= 90 else BAD


def progress_bar(fraction, width, color=GOOD):
    fraction = max(0.0, min(1.0, fraction))
    full = int(round(fraction * width))
    return color + "█" * full + DIM + "░" * (width - full) + RESET


_SPARK = "▁▂▃▄▅▆▇█"


def sparkline(values, width=None):
    values = list(values)
    if width and len(values) > width:
        # auf width Werte zusammenfassen
        step = len(values) / width
        values = [sum(values[int(i * step):int((i + 1) * step)] or [0])
                  / max(1, len(values[int(i * step):int((i + 1) * step)]))
                  for i in range(width)]
    if not values:
        return ""
    top = max(values) or 1
    return "".join(_SPARK[min(7, int(v / top * 7.999))] for v in values)


def bar_chart(values, height):
    """Senkrechte Balken, eine Spalte pro Wert. Die y-Achse beginnt knapp
    unter dem kleinsten Wert, damit Unterschiede sichtbar werden."""
    if not values:
        return []
    top = max(values)
    low = int(min(values) * 0.8) // 10 * 10
    span = (top - low) or 1
    lines = []
    for row in range(height, 0, -1):
        cells = []
        for v in values:
            level = (v - low) / span * height - (row - 1)
            if level >= 1:
                cells.append("█")
            elif level > 0:
                cells.append(_SPARK[min(7, int(level * 8))])
            else:
                cells.append(" ")
        if row == height:
            axis = "%4d ┤" % round(top)
        elif row == 1:
            axis = "%4d ┤" % low
        else:
            axis = "     │"
        lines.append(DIM + axis + RESET + ACCENT + "".join(cells) + RESET)
    return lines


# --- Kalender-Farben (GitHub-Grün) -------------------------------------------

_HEAT_TRUE = ((52, 58, 66), (14, 68, 41), (0, 109, 50), (38, 166, 65), (57, 211, 83))
_HEAT_256 = (237, 22, 28, 34, 46)
_HEAT_BASIC = (
    (Fore.LIGHTBLACK_EX, "■"), (Fore.GREEN, "▪"), (Fore.GREEN, "■"),
    (Fore.LIGHTGREEN_EX, "■"), (Style.BRIGHT + Fore.LIGHTGREEN_EX, "█"),
)


def heat_cell(level, mode="256"):
    if mode == "truecolor":
        r, g, b = _HEAT_TRUE[level]
        return "\x1b[38;2;%d;%d;%dm■%s" % (r, g, b, RESET)
    if mode == "256":
        return "\x1b[38;5;%dm■%s" % (_HEAT_256[level], RESET)
    color, glyph = _HEAT_BASIC[level]
    return color + glyph + RESET


def heat_level(seconds, goal_seconds):
    if seconds <= 0:
        return 0
    if seconds < goal_seconds * 0.5:
        return 1
    if seconds < goal_seconds:
        return 2
    if seconds < goal_seconds * 2:
        return 3
    return 4


# --- Große Ziffern für das Ergebnis ----------------------------------------

_BIG = {
    "0": ("█▀█", "█ █", "▀▀▀"),
    "1": ("▀█ ", " █ ", "▀▀▀"),
    "2": ("▀▀█", "█▀▀", "▀▀▀"),
    "3": ("▀▀█", " ▀█", "▀▀▀"),
    "4": ("█ █", "▀▀█", "  ▀"),
    "5": ("█▀▀", "▀▀█", "▀▀▀"),
    "6": ("█▀▀", "█▀█", "▀▀▀"),
    "7": ("▀▀█", "  █", "  ▀"),
    "8": ("█▀█", "█▀█", "▀▀▀"),
    "9": ("█▀█", "▀▀█", "▀▀▀"),
}


def big_number(value):
    digits = str(int(round(value)))
    return [" ".join(_BIG[d][row] for d in digits) for row in range(3)]


# --- Bildschirm --------------------------------------------------------------

def draw(term, lines):
    """Zeichnet den ganzen Bildschirm neu, ohne zu flackern."""
    cols, rows = term.size()
    buf = [T.HOME]
    for line in lines[:rows - 1]:
        buf.append(clip(line, cols - 1) + RESET + T.CLEAR_EOL + "\n")
    buf.append(T.CLEAR_EOS)
    term.write("".join(buf))


def frame(term, lines, footer="", width=72):
    """Zentriert einen Block waagerecht und setzt die Fußzeile nach unten."""
    cols, rows = term.size()
    w = min(width, cols - 2)
    margin = " " * max(1, (cols - w) // 2)
    top = [""] * max(0, (rows - 2 - len(lines)) // 3)
    body = top + [margin + line for line in lines]
    if footer:
        body = body[:rows - 2]
        while len(body) < rows - 2:
            body.append("")
        body.append(margin + DIM + footer + RESET)
    return body


def content_width(term, width=72):
    cols, _ = term.size()
    return min(width, cols - 2)


def title_block(title, subtitle="", width=72):
    head = gradient(title)
    if subtitle:
        head += "  " + DIM + subtitle + RESET
    return [head, DIM + "─" * width + RESET]


def message(term, title, lines, footer="Weiter mit beliebiger Taste"):
    width = content_width(term)
    draw(term, frame(term, title_block(title, width=width) + [""] + list(lines), footer))
    term.flush_input()
    while term.read_key(0.5) is None:
        draw(term, frame(term, title_block(title, width=width) + [""] + list(lines), footer))


def confirm(term, title, question):
    width = content_width(term)
    lines = title_block(title, width=width) + ["", question, "",
                                               DIM + "[j] Ja    [n] Nein" + RESET]
    while True:
        draw(term, frame(term, lines))
        key = term.read_key(0.5)
        if key in ("j", "J", "y", "Y"):
            return True
        if key in ("n", "N", T.ESC, T.CTRL_C):
            return False


class Item:
    """Ein Menüeintrag. Mit options wird daraus ein Auswahlfeld (◀ ▶)."""

    def __init__(self, label="", action=None, options=None, value=None, fmt=None,
                 on_change=None, hint="", right="", separator=False):
        self.label = label
        self.action = action
        self.options = options
        self.value = value
        self.fmt = fmt
        self.on_change = on_change
        self.hint = hint
        self.right = right
        self.separator = separator

    @classmethod
    def sep(cls):
        return cls(separator=True)

    def display_value(self):
        if self.fmt is None:
            return str(self.value)
        if isinstance(self.fmt, dict):
            return self.fmt.get(self.value, str(self.value))
        return self.fmt(self.value)

    def cycle(self, step):
        i = self.options.index(self.value) if self.value in self.options else 0
        self.value = self.options[(i + step) % len(self.options)]
        if self.on_change:
            self.on_change(self.value)


def run_menu(term, header, items, index=0, footer="", extra_keys=(), width=72,
             numbered=False, side=None, side_col=34):
    """Zeigt ein Menü. Gibt (aktion, index, taste) zurück; aktion None = zurück.

    numbered: Einträge mit 1–9 direkt wählbar.
    side:     Funktion, die Zeilen liefert, die rechts neben dem Menü stehen."""
    selectable = [i for i, it in enumerate(items) if not it.separator]
    if index not in selectable:
        index = selectable[0]
    label_w = max(vlen(items[i].label) for i in selectable) + 3
    while True:
        cols, rows = term.size()
        lines = list(header() if callable(header) else header)
        menu_lines = []
        for i, it in enumerate(items):
            if it.separator:
                menu_lines.append("")
                continue
            active = i == index
            glow = fg(hsv(0.5 + clock() * 0.12, 0.55, 1.0))
            marker = glow + BRIGHT + "❯ " if active else "  "
            if numbered:
                n = selectable.index(i) + 1
                marker += (DIM + "%d  " % n + RESET) if n <= 9 else "   "
            label = (BRIGHT + TEXT if active else SOFT) + pad(it.label, label_w) + RESET
            extra = ""
            if it.options is not None:
                value = it.display_value()
                extra = (glow + "‹ " + RESET + BRIGHT + value + RESET + glow + " ›") if active \
                    else (DIM + "  " + value)
            elif it.right:
                extra = DIM + "  " + it.right
            menu_lines.append(marker + RESET + label + extra + RESET)
        hint = items[index].hint
        # Wenn das Menü nicht auf den Bildschirm passt, nur einen Ausschnitt zeigen.
        room = rows - len(lines) - (4 if hint else 2)
        if len(menu_lines) > room > 3:
            first = min(max(0, index - room // 2), len(menu_lines) - room)
            menu_lines = menu_lines[first:first + room]
        if side and content_width(term, width) >= side_col + 24:
            panel = side()
            merged = []
            for i in range(max(len(menu_lines), len(panel))):
                left = menu_lines[i] if i < len(menu_lines) else ""
                right = panel[i] if i < len(panel) else ""
                merged.append(pad(left, side_col) + right)
            menu_lines = merged
        lines += menu_lines
        if hint:
            lines += ["", DIM + hint + RESET]
        draw(term, frame(term, lines, footer, width))

        key = term.read_key(0.08 if STYLE["animate"] else 0.5)
        if key is None:
            continue
        item = items[index]
        pos = selectable.index(index)
        if key in (T.UP, "k"):
            index = selectable[(pos - 1) % len(selectable)]
        elif key in (T.DOWN, "j", T.TAB):
            index = selectable[(pos + 1) % len(selectable)]
        elif key in (T.LEFT, "h") and item.options is not None:
            item.cycle(-1)
        elif key in (T.RIGHT, "l") and item.options is not None:
            item.cycle(1)
        elif key in (T.ENTER, " "):
            if item.action is not None:
                return item.action, index, key
            if item.options is not None:
                item.cycle(1)
        elif key in (T.ESC, "q", T.CTRL_C):
            return None, index, key
        elif key in extra_keys:
            return item.action, index, key
        elif numbered and len(key) == 1 and key.isdigit() and 1 <= int(key) <= min(9, len(selectable)):
            index = selectable[int(key) - 1]
            if items[index].action is not None:
                return items[index].action, index, T.ENTER
