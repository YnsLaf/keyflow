"""Makes the `keyflow` command available after `pip install --user`.

pip puts the command into a user folder (on macOS e.g. ~/Library/Python/3.9/bin)
that is often not on the PATH. On first start KeyFlow fixes that itself:
  1. a link in a folder that is already on the PATH and writable (works at once), or
  2. an `export PATH=...` line in the shell's startup file (works in new windows)."""

import os
import shutil
import sys
import sysconfig
from pathlib import Path

COMMAND = "keyflow"
MARKER = "# Added by KeyFlow: makes the keyflow command available"
SYSTEM_DIRS = {"/bin", "/sbin", "/usr/bin", "/usr/sbin"}


def available():
    return shutil.which(COMMAND) is not None


def _script_dirs():
    dirs = []
    schemes = []
    get_preferred = getattr(sysconfig, "get_preferred_scheme", None)
    if get_preferred:
        schemes.append(get_preferred("user"))
    schemes += ["osx_framework_user", "posix_user", "nt_user"]
    for scheme in schemes:
        try:
            dirs.append(sysconfig.get_path("scripts", scheme))
        except KeyError:
            continue
    dirs.append(sysconfig.get_path("scripts"))
    dirs.append(os.path.join(sys.prefix, "bin"))
    seen, result = set(), []
    for d in dirs:
        if d and d not in seen:
            seen.add(d)
            result.append(Path(d))
    return result


def installed_script():
    """Path of the `keyflow` script pip created, or None."""
    for folder in _script_dirs():
        candidate = folder / COMMAND
        if candidate.is_file():
            return candidate
    return None


def _writable_path_dir():
    home = str(Path.home())
    for entry in os.environ.get("PATH", "").split(os.pathsep):
        if not entry or entry in SYSTEM_DIRS:
            continue
        path = Path(os.path.expanduser(entry))
        # nur Ordner im eigenen Home oder bekannte Homebrew-/local-Ordner
        if not (str(path).startswith(home) or str(path) in ("/opt/homebrew/bin", "/usr/local/bin")):
            continue
        if path.is_dir() and os.access(str(path), os.W_OK):
            return path
    return None


def _rc_file():
    shell = os.path.basename(os.environ.get("SHELL", ""))
    home = Path.home()
    if shell == "bash":
        return home / (".bash_profile" if sys.platform == "darwin" else ".bashrc")
    if shell == "fish":
        return home / ".config" / "fish" / "config.fish"
    return home / ".zshrc"


def setup():
    """Tries to make `keyflow` available. Returns (how, where) or None.

    how: "link" (works immediately) or "rc" (works in new terminal windows)."""
    if os.name == "nt" or available():
        return None
    script = installed_script()
    if script is None:
        return None
    target_dir = _writable_path_dir()
    if target_dir is not None:
        link = target_dir / COMMAND
        try:
            if link.is_symlink() or link.exists():
                link.unlink()
            link.symlink_to(script)
            return "link", str(target_dir)
        except OSError:
            pass
    rc = _rc_file()
    folder = str(script.parent)
    try:
        existing = rc.read_text(encoding="utf-8") if rc.exists() else ""
        if folder not in existing:
            rc.parent.mkdir(parents=True, exist_ok=True)
            if rc.name == "config.fish":
                line = 'fish_add_path "%s"' % folder
            else:
                line = 'export PATH="$PATH:%s"' % folder
            with rc.open("a", encoding="utf-8") as fh:
                fh.write("\n%s\n%s\n" % (MARKER, line))
        return "rc", str(rc).replace(str(Path.home()), "~", 1)
    except OSError:
        return None
