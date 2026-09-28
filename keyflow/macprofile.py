"""Transparenter Hintergrund im Mac-Terminal (Terminal.app).

Terminal.app kann die Deckkraft nicht per AppleScript setzen – nur ein Profil
kann das. KeyFlow legt deshalb einmalig das Profil "KeyFlow" an (Farbe,
Deckkraft und Schrift) und schaltet den eigenen Tab beim Start darauf um.
Beim Beenden wird wieder das vorherige Profil eingestellt."""

import os
import plistlib
import subprocess
import sys
import tempfile
import time

PROFILE = "KeyFlow"
TITLE = "KeyFlow"


def available():
    return sys.platform == "darwin" and os.environ.get("TERM_PROGRAM") == "Apple_Terminal"


def _tty():
    try:
        return os.ttyname(sys.stdin.fileno())
    except OSError:
        return None


def run_script(script, timeout=5):
    try:
        done = subprocess.run(["osascript", "-e", script], capture_output=True, text=True,
                              timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def tab_script(action):
    """AppleScript für genau den Tab, in dem KeyFlow läuft (Variable t)."""
    tty = _tty()
    if not tty:
        return None
    return run_script(
        'tell application "Terminal"\n'
        '  repeat with w in windows\n'
        '    repeat with t in tabs of w\n'
        '      if tty of t is "%s" then %s\n'
        '    end repeat\n'
        '  end repeat\n'
        'end tell' % (tty, action))


def ns_color(r, g, b, a=1.0):
    """Eine Farbe so verpackt, wie Terminal-Profile sie speichern (NSKeyedArchiver)."""
    archive = {
        "$archiver": "NSKeyedArchiver",
        "$version": 100000,
        "$top": {"root": plistlib.UID(1)},
        "$objects": [
            "$null",
            {"$class": plistlib.UID(2), "NSColorSpace": 1,
             "NSRGB": ("%.4f %.4f %.4f %.4f" % (r, g, b, a)).encode() + b"\x00"},
            {"$classname": "NSColor", "$classes": ["NSColor", "NSObject"]},
        ],
    }
    return plistlib.dumps(archive, fmt=plistlib.FMT_BINARY)


def profile_data(rgb, opacity, columns, rows):
    r, g, b = (c / 255 for c in rgb)
    return {
        "name": PROFILE,
        "type": "Window Settings",
        "ProfileCurrentVersion": 2.07,
        "BackgroundColor": ns_color(r, g, b, opacity),
        "BackgroundBlur": 0.5,
        "TextColor": ns_color(0.92, 0.92, 0.92),
        "TextBoldColor": ns_color(1, 1, 1),
        "CursorColor": ns_color(0.85, 0.85, 0.85),
        "SelectionColor": ns_color(0.35, 0.35, 0.35),
        "columnCount": columns,
        "rowCount": rows,
        "UseBrightBold": True,
        # Titelleiste: nur "KeyFlow" – ohne Ordner, Prozess und Fenstergröße
        "WindowTitle": TITLE,
        "ShowActiveProcessInTitle": False,
        "ShowActiveProcessArgumentsInTitle": False,
        "ShowCommandKeyInTitle": False,
        "ShowDimensionsInTitle": False,
        "ShowRepresentedURLInTitle": False,
        "ShowRepresentedURLPathInTitle": False,
        "ShowShellCommandInTitle": False,
        "ShowTTYNameInTitle": False,
        "ShowWindowSettingsNameInTitle": False,
        "ShowComponentsWhenTabHasCustomTitle": False,
        "ShowActiveProcessInTabTitle": False,
        "ShowWorkingDirectoryInTabTitle": False,
    }


def _profile_exists():
    return run_script('tell application "Terminal" to return exists settings set "%s"' % PROFILE) == "true"


def _import_profile(rgb, opacity, columns, rows):
    """Öffnet eine .terminal-Datei: Terminal übernimmt sie als Profil und öffnet
    dafür ein Fenster, das gleich wieder geschlossen wird."""
    folder = tempfile.mkdtemp(prefix="keyflow-")
    path = os.path.join(folder, PROFILE + ".terminal")
    with open(path, "wb") as fh:
        plistlib.dump(profile_data(rgb, opacity, columns, rows), fh)
    try:
        subprocess.run(["open", path], timeout=5)
    except (OSError, subprocess.SubprocessError):
        return False
    for _ in range(40):
        if _profile_exists():
            break
        time.sleep(0.1)
    else:
        return False
    time.sleep(0.3)
    run_script(
        'tell application "Terminal"\n'
        '  set ids to {}\n'
        '  repeat with w in windows\n'
        '    try\n'
        '      if name of current settings of selected tab of w is "%s" then set end of ids to id of w\n'
        '    end try\n'
        '  end repeat\n'
        '  repeat with i in ids\n'
        '    close (window id i)\n'
        '  end repeat\n'
        'end tell' % PROFILE)
    return True


def _set_title_options():
    """Auch bei einem schon vorhandenen Profil: Titel nur "KeyFlow"."""
    options = [
        'set custom title of s to "%s"' % TITLE,
        "set title displays custom title of s to true",
        "set title displays device name of s to false",
        "set title displays shell path of s to false",
        "set title displays window size of s to false",
        "set title displays settings name of s to false",
    ]
    run_script('tell application "Terminal"\n'
               '  set s to settings set "%s"\n' % PROFILE
               + "".join("  try\n    %s\n  end try\n" % o for o in options)
               + "end tell")


class GlassProfile:
    """Schaltet den eigenen Tab auf das KeyFlow-Profil und wieder zurück."""

    def __init__(self):
        self.previous = None

    def apply(self, rgb, opacity, columns, rows):
        current = tab_script("return name of current settings of t")
        if current is None:
            return False
        if current == PROFILE:
            return True
        font = tab_script('return (font name of current settings of t) & "|" & '
                          '(font size of current settings of t)')
        if not _profile_exists() and not _import_profile(rgb, opacity, columns, rows):
            return False
        # Schrift aus dem bisherigen Profil übernehmen
        if font and "|" in font:
            name, size = font.split("|", 1)
            run_script('tell application "Terminal"\n'
                       '  set font name of settings set "%s" to "%s"\n'
                       '  set font size of settings set "%s" to %s\n'
                       'end tell' % (PROFILE, name, PROFILE, size.replace(",", ".")))
        _set_title_options()
        if tab_script('set current settings of t to settings set "%s"' % PROFILE) is None:
            return False
        tab_script('set custom title of t to "%s"' % TITLE)
        self.previous = current
        return True

    def restore(self):
        if self.previous:
            tab_script('set current settings of t to settings set "%s"' % self.previous)
            tab_script('set custom title of t to ""')
            self.previous = None
