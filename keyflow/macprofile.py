"""Transparent background in the macOS Terminal (Terminal.app).

Terminal.app cannot set the opacity via AppleScript – only a profile can.
So KeyFlow creates a "KeyFlow" profile once (color, opacity and font) and
switches its own tab to it on start. On quit the previous profile comes back."""

import os
import plistlib
import subprocess
import sys
import tempfile
import time

PROFILE = "KeyFlow"          # profile name prefix; the opacity is appended ("KeyFlow 70")
LEGACY_PROFILE = "KeyFlow"   # old profile with 30 % from version 1.4.0
TITLE = "KeyFlow"


def profile_name(opacity):
    return "%s %d" % (PROFILE, round(opacity * 100))


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
    """AppleScript for exactly the tab KeyFlow runs in (variable t)."""
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
    """A color packed the way Terminal profiles store it (NSKeyedArchiver)."""
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
        "name": profile_name(opacity),
        "type": "Window Settings",
        "ProfileCurrentVersion": 2.07,
        "BackgroundColor": ns_color(r, g, b, opacity),
        "BackgroundBlur": 0.85,   # strong blur so text stays readable in front of bright windows
        "TextColor": ns_color(0.92, 0.92, 0.92),
        "TextBoldColor": ns_color(1, 1, 1),
        "CursorColor": ns_color(0.85, 0.85, 0.85),
        "SelectionColor": ns_color(0.35, 0.35, 0.35),
        "columnCount": columns,
        "rowCount": rows,
        "UseBrightBold": True,
        # title bar: only "KeyFlow" – no folder, process or window size
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


def _profile_exists(name):
    return run_script('tell application "Terminal" to return exists settings set "%s"' % name) == "true"


def _import_profile(name, rgb, opacity, columns, rows):
    """Opens a .terminal file: Terminal imports it as a profile and opens a
    window for it, which is closed again right away."""
    folder = tempfile.mkdtemp(prefix="keyflow-")
    path = os.path.join(folder, name + ".terminal")
    with open(path, "wb") as fh:
        plistlib.dump(profile_data(rgb, opacity, columns, rows), fh)
    try:
        subprocess.run(["open", path], timeout=5)
    except (OSError, subprocess.SubprocessError):
        return False
    for _ in range(40):
        if _profile_exists(name):
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
        'end tell' % name)
    return True


def _set_title_options(name):
    """Also for an existing profile: title shows only "KeyFlow"."""
    options = [
        'set custom title of s to "%s"' % TITLE,
        "set title displays custom title of s to true",
        "set title displays device name of s to false",
        "set title displays shell path of s to false",
        "set title displays window size of s to false",
        "set title displays settings name of s to false",
    ]
    run_script('tell application "Terminal"\n'
               '  set s to settings set "%s"\n' % name
               + "".join("  try\n    %s\n  end try\n" % o for o in options)
               + "end tell")


def _remove_legacy_profile():
    """Removes the old "KeyFlow" profile (30 %) if it still exists."""
    if _profile_exists(LEGACY_PROFILE):
        run_script('tell application "Terminal"\n'
                   '  try\n    delete settings set "%s"\n  end try\n'
                   'end tell' % LEGACY_PROFILE)


def _is_keyflow_profile(name):
    return name == LEGACY_PROFILE or name.startswith(PROFILE + " ")


class GlassProfile:
    """Switches our own tab to a KeyFlow profile and back again."""

    def __init__(self):
        self.previous = None

    def apply(self, rgb, opacity, columns, rows):
        name = profile_name(opacity)
        current = tab_script("return name of current settings of t")
        if current is None:
            return False
        if current == name:
            return True
        font = tab_script('return (font name of current settings of t) & "|" & '
                          '(font size of current settings of t)')
        if not _profile_exists(name) and not _import_profile(name, rgb, opacity, columns, rows):
            return False
        # keep the font of the previous profile
        if font and "|" in font:
            font_name, size = font.split("|", 1)
            run_script('tell application "Terminal"\n'
                       '  set font name of settings set "%s" to "%s"\n'
                       '  set font size of settings set "%s" to %s\n'
                       'end tell' % (name, font_name, name, size.replace(",", ".")))
        _set_title_options(name)
        if tab_script('set current settings of t to settings set "%s"' % name) is None:
            return False
        tab_script('set custom title of t to "%s"' % TITLE)
        # when switching between two KeyFlow levels, keep the original profile
        if self.previous is None and not _is_keyflow_profile(current):
            self.previous = current
        _remove_legacy_profile()
        return True

    def restore(self):
        if self.previous:
            tab_script('set current settings of t to settings set "%s"' % self.previous)
            tab_script('set custom title of t to ""')
            self.previous = None
