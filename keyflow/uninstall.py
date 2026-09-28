"""Removes KeyFlow from this computer (Info → Delete KeyFlow).

Runs after the terminal has been restored, so the output lands in the normal
terminal. Removes the package, the keyflow command link and PATH line that
KeyFlow set up, the macOS Terminal profiles and – if wanted – the data."""

import os
import subprocess
import sys
from pathlib import Path

from . import command, macprofile, updates
from .i18n import tr


def uninstall_command():
    """Command that removes the package, or None for a git checkout."""
    method = updates.install_method()
    if method == "pipx":
        return ["pipx", "uninstall", updates.PACKAGE]
    if method == "pip":
        return [sys.executable, "-m", "pip", "uninstall", "-y", updates.PACKAGE]
    return None


def uninstall_command_text():
    method = updates.install_method()
    if method == "pipx":
        return "pipx uninstall %s" % updates.PACKAGE
    if method == "pip":
        pip = "pip3" if sys.platform == "darwin" else "pip"
        return "%s uninstall %s" % (pip, updates.PACKAGE)
    return None


def remove_command_link():
    """Removes the keyflow link KeyFlow placed in a PATH folder. Returns its path or None."""
    script_dirs = set(command._script_dirs())
    for entry in os.environ.get("PATH", "").split(os.pathsep):
        if not entry:
            continue
        link = Path(os.path.expanduser(entry)) / command.COMMAND
        if not link.is_symlink():
            continue
        try:
            target = Path(os.readlink(str(link)))
        except OSError:
            continue
        # only the link KeyFlow made: it points to the script pip installed
        if target.name == command.COMMAND and target.parent in script_dirs:
            try:
                link.unlink()
                return str(link)
            except OSError:
                return None
    return None


def remove_path_line():
    """Removes the PATH line KeyFlow added to the shell startup file. Returns the file or None."""
    rc = command._rc_file()
    try:
        lines = rc.read_text(encoding="utf-8").splitlines(True)
    except OSError:
        return None
    kept, skip_next, changed = [], False, False
    for line in lines:
        if skip_next:
            skip_next, changed = False, True
            continue
        if line.strip() == command.MARKER:
            skip_next, changed = True, True
            if kept and not kept[-1].strip():
                kept.pop()
            continue
        kept.append(line)
    if not changed:
        return None
    try:
        rc.write_text("".join(kept), encoding="utf-8")
    except OSError:
        return None
    return str(rc).replace(str(Path.home()), "~", 1)


def remove_terminal_profiles():
    """Deletes the "KeyFlow …" profiles in the macOS Terminal. Returns how many."""
    if not macprofile.available():
        return 0
    names = macprofile.run_script('tell application "Terminal"\n'
                                  '  set AppleScript\'s text item delimiters to "|"\n'
                                  '  return (name of settings sets) as text\n'
                                  'end tell')
    removed = 0
    for name in (names or "").split("|"):
        if name and macprofile._is_keyflow_profile(name):
            done = macprofile.run_script('tell application "Terminal" to delete settings set "%s"' % name)
            removed += done is not None
    return removed


def remove_data(path):
    """Deletes the data file (and its backups) and the folder if it is empty afterwards."""
    path = Path(path)
    removed = False
    for candidate in (path, path.with_name(path.stem + ".broken.json"),
                      path.with_name(path.name + ".tmp")):
        try:
            candidate.unlink()
            removed = True
        except OSError:
            pass
    try:
        path.parent.rmdir()
    except OSError:
        pass
    return removed


def run(data_path, delete_data):
    """Removes everything and prints what happened. Returns True on success."""
    print(tr("KeyFlow wird entfernt …", "Removing KeyFlow …") + "\n")
    ok = True
    cmd = uninstall_command()
    if cmd is None:
        print(tr("• KeyFlow läuft aus dem Quellcode – lösche den Ordner einfach selbst:",
                 "• KeyFlow runs from source code – simply delete the folder yourself:"))
        print("    " + str(Path(__file__).resolve().parent.parent).replace(str(Path.home()), "~", 1))
    else:
        print("• " + uninstall_command_text())
        try:
            ok = subprocess.call(cmd) == 0
        except OSError:
            ok = False
        if not ok:
            print(tr("  Das hat nicht geklappt. Führe den Befehl bitte selbst aus.",
                     "  That did not work. Please run the command yourself."))
    link = remove_command_link()
    if link:
        print(tr("• Verweis entfernt: ", "• Link removed: ") + link.replace(str(Path.home()), "~", 1))
    rc = remove_path_line()
    if rc:
        print(tr("• PATH-Eintrag entfernt aus ", "• PATH entry removed from ") + rc)
    profiles = remove_terminal_profiles()
    if profiles:
        print(tr("• Terminal-Profile entfernt: %d", "• Terminal profiles removed: %d") % profiles)
    if delete_data:
        if remove_data(data_path):
            print(tr("• Deine Daten wurden gelöscht.", "• Your data was deleted."))
    else:
        print(tr("• Deine Daten bleiben erhalten: ", "• Your data was kept: ")
              + str(data_path).replace(str(Path.home()), "~", 1))
    print()
    if ok:
        print(tr("KeyFlow wurde entfernt. Danke fürs Üben! – YnsLaf",
                 "KeyFlow has been removed. Thanks for practicing! – YnsLaf"))
    return ok
