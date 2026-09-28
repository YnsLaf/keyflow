"""Tastatur-Eingabe und Bildschirmsteuerung für Windows, Linux und macOS."""

import os
import re
import shutil
import subprocess
import sys
import time
from contextlib import contextmanager

import colorama

from . import macprofile

WINDOWS = os.name == "nt"

if WINDOWS:  # pragma: no cover - nur unter Windows
    import msvcrt
else:
    import select
    import termios
    import tty

# Namen für Sondertasten. Normale Zeichen kommen als einzelnes Zeichen zurück.
UP = "<oben>"
DOWN = "<unten>"
LEFT = "<links>"
RIGHT = "<rechts>"
ENTER = "<enter>"
TAB = "<tab>"
ESC = "<esc>"
BACKSPACE = "<rücktaste>"
CTRL_BACKSPACE = "<strg-rücktaste>"
DELETE = "<entf>"
CTRL_C = "<strg-c>"

HOME = "\x1b[H"
CLEAR = "\x1b[2J"
CLEAR_EOL = "\x1b[K"
CLEAR_EOS = "\x1b[J"
HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"
ALT_SCREEN_ON = "\x1b[?1049h"
ALT_SCREEN_OFF = "\x1b[?1049l"
# Bildschirm und Scrollback leeren, Cursor nach oben links
WIPE = "\x1b[2J\x1b[3J\x1b[H"
# Fenstertitel: alten Titel merken, "KeyFlow" setzen – und beim Beenden zurück
TITLE_ON = "\x1b[22;0t\x1b]0;KeyFlow\x07"
TITLE_OFF = "\x1b]0;\x07\x1b[23;0t"

_CSI_KEYS = {
    b"A": UP, b"B": DOWN, b"C": RIGHT, b"D": LEFT, b"3~": DELETE,
}

_WIN_KEYS = {
    "\r": ENTER, "\n": ENTER, "\t": TAB, "\x08": BACKSPACE,
    "\x7f": CTRL_BACKSPACE, "\x17": CTRL_BACKSPACE, "\x1b": ESC, "\x03": CTRL_C,
}
_WIN_SPECIAL = {"H": UP, "P": DOWN, "K": LEFT, "M": RIGHT, "S": DELETE}


def is_char(key):
    return key is not None and len(key) == 1 and key.isprintable()


class Terminal:
    """Schaltet das Terminal in den Tasten-Modus und zurück (mit `with`)."""

    def __init__(self):
        self.out = sys.stdout
        self.fd = None
        self._saved = None
        self._erase = b"\x7f"
        self._apple_original = None   # ursprüngliche Hintergrundfarbe (Terminal.app)
        self._osc_background = False
        self._glass = macprofile.GlassProfile()

    def __enter__(self):
        fix = getattr(colorama, "just_fix_windows_console", None)
        if fix:
            fix()
        else:  # ältere colorama-Versionen
            colorama.init()
        if not WINDOWS:
            if not sys.stdin.isatty():
                raise RuntimeError("KeyFlow needs to be run in a terminal.")
            self.fd = sys.stdin.fileno()
            self._saved = termios.tcgetattr(self.fd)
            erase = self._saved[6][termios.VERASE]
            if isinstance(erase, int):
                erase = bytes([erase])
            if erase:
                self._erase = erase
            tty.setcbreak(self.fd)
        self.write(TITLE_ON + WIPE + ALT_SCREEN_ON + HIDE_CURSOR + CLEAR + HOME)
        return self

    def __exit__(self, *exc):
        self.restore_background()
        self.write(colorama.Style.RESET_ALL + SHOW_CURSOR + ALT_SCREEN_OFF + WIPE + TITLE_OFF)
        if self._saved is not None:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self._saved)
        return False

    # --- Ausgabe ---------------------------------------------------------
    def write(self, text):
        self.out.write(text)
        self.out.flush()

    def size(self):
        size = shutil.get_terminal_size((80, 24))
        return max(20, size.columns), max(8, size.lines)

    # --- Hintergrundfarbe des Terminals ---------------------------------
    def _apple_terminal(self):
        return sys.platform == "darwin" and os.environ.get("TERM_PROGRAM") == "Apple_Terminal"

    def _apple_script(self, action):
        """Führt AppleScript für genau diesen Terminal-Tab aus (erkannt am tty)."""
        try:
            tty_name = os.ttyname(sys.stdin.fileno())
        except OSError:
            return None
        script = (
            'tell application "Terminal"\n'
            '  repeat with w in windows\n'
            '    repeat with t in tabs of w\n'
            '      if tty of t is "%s" then %s\n'
            '    end repeat\n'
            '  end repeat\n'
            'end tell' % (tty_name, action))
        try:
            done = subprocess.run(["osascript", "-e", script], capture_output=True,
                                  text=True, timeout=4)
        except (OSError, subprocess.SubprocessError):
            return None
        return done.stdout if done.returncode == 0 else None

    def set_background(self, rgb, opacity=None):
        """Setzt die Hintergrundfarbe (und im Mac-Terminal die Deckkraft 0–1);
        rgb None stellt die ursprüngliche Farbe wieder her."""
        if rgb is None:
            self.restore_background()
            return
        if self._apple_terminal():
            if opacity is not None:
                # Deckkraft geht in Terminal.app nur über ein Profil (siehe macprofile).
                if self._apple_original:
                    self.restore_background()
                cols, rows = self.size()
                self._glass.apply(rgb, opacity, cols, rows)
                return
            self._glass.restore()
            if self._apple_original is None:
                out = self._apple_script("return background color of t") or ""
                self._apple_original = [int(n) for n in re.findall(r"-?\d+", out)]
            if len(self._apple_original) < 3:
                return  # Farbe ließ sich nicht auslesen – dann lieber nichts ändern
            color = [c * 257 for c in rgb]
            self._apple_script("set background color of t to {%s}" % ", ".join(map(str, color)))
        else:
            self.write("\x1b]11;#%02x%02x%02x\x1b\\" % tuple(rgb))
            self._osc_background = True

    def restore_background(self):
        self._glass.restore()
        if self._apple_original:
            self._apple_script("set background color of t to {%s}"
                               % ", ".join(map(str, self._apple_original)))
            self._apple_original = None
        if self._osc_background:
            self.write("\x1b]111\x1b\\")
            self._osc_background = False

    def bell(self):
        self.write("\a")

    @contextmanager
    def cooked(self):
        """Normaler Zeilen-Modus, z. B. für input()."""
        self.write(colorama.Style.RESET_ALL + CLEAR + HOME + SHOW_CURSOR)
        if self._saved is not None:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self._saved)
        try:
            yield
        finally:
            if self._saved is not None:
                tty.setcbreak(self.fd)
            self.write(HIDE_CURSOR + CLEAR + HOME)

    # --- Eingabe ---------------------------------------------------------
    def read_key(self, timeout=None):
        """Wartet auf eine Taste; gibt None zurück, wenn timeout abläuft."""
        if WINDOWS:
            return self._read_key_windows(timeout)
        return self._read_key_posix(timeout)

    def flush_input(self):
        """Verwirft Tasten, die noch im Puffer liegen."""
        if WINDOWS:
            while msvcrt.kbhit():
                msvcrt.getwch()
        elif self.fd is not None:
            termios.tcflush(self.fd, termios.TCIFLUSH)

    def _byte(self, timeout):
        ready, _, _ = select.select([self.fd], [], [], timeout)
        if not ready:
            return None
        data = os.read(self.fd, 1)
        if not data:
            raise EOFError
        return data

    def _read_key_posix(self, timeout):
        b = self._byte(timeout)
        if b is None:
            return None
        if b == b"\x1b":
            return self._escape_sequence()
        if b in (b"\r", b"\n"):
            return ENTER
        if b == b"\t":
            return TAB
        if b == self._erase or b == b"\x7f":
            return BACKSPACE
        if b in (b"\x08", b"\x17"):  # Strg+Rücktaste bzw. Strg+W
            return CTRL_BACKSPACE
        if b == b"\x03":
            return CTRL_C
        first = b[0]
        if first < 0x20:
            return None
        if first >= 0xC0:  # mehrbytiges UTF-8-Zeichen (ä, ö, ü, ß, € …)
            need = 1 if first < 0xE0 else 2 if first < 0xF0 else 3
            for _ in range(need):
                nxt = self._byte(0.05)
                if nxt is None:
                    break
                b += nxt
        ch = b.decode("utf-8", errors="replace")
        return ch if len(ch) == 1 and ch.isprintable() else None

    def _escape_sequence(self):
        nxt = self._byte(0.03)
        if nxt is None:
            return ESC
        if nxt in (b"[", b"O"):
            seq = b""
            while len(seq) < 8:
                c = self._byte(0.03)
                if c is None:
                    break
                seq += c
                if 0x40 <= c[0] <= 0x7E:
                    break
            return _CSI_KEYS.get(seq)
        if nxt in (b"\x7f", b"\x08"):  # Alt+Rücktaste (macOS: Option+Rücktaste)
            return CTRL_BACKSPACE
        if nxt == b"\x1b":
            return ESC
        return None

    def _read_key_windows(self, timeout):  # pragma: no cover - nur unter Windows
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            while msvcrt.kbhit():
                ch = msvcrt.getwch()
                if ch in ("\x00", "\xe0"):
                    if ch == "\xe0" and not msvcrt.kbhit():
                        return ch  # das Zeichen "à"
                    key = _WIN_SPECIAL.get(msvcrt.getwch())
                    if key:
                        return key
                    continue
                if ch in _WIN_KEYS:
                    return _WIN_KEYS[ch]
                if ch.isprintable():
                    return ch
            if deadline is not None and time.monotonic() >= deadline:
                return None
            time.sleep(0.01)
