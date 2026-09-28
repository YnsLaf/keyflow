"""Checks PyPI for a newer KeyFlow version and knows how to update this installation."""

import json
import os
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

from . import __version__

PACKAGE = "keyflow-typing"
PYPI_URL = "https://pypi.org/pypi/%s/json" % PACKAGE
PROJECT_URL = "https://pypi.org/project/%s/" % PACKAGE
GITHUB_USER_URL = "https://github.com/YnsLaf"
GITHUB_REPO_URL = "https://github.com/YnsLaf/keyflow"


def parse_version(text):
    """"1.10.2" -> (1, 10, 2); ignores anything that is not a number."""
    parts = []
    for piece in str(text).split("."):
        digits = "".join(ch for ch in piece if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def is_newer(latest, current=__version__):
    return parse_version(latest) > parse_version(current)


def install_method():
    """How KeyFlow was installed: "source" (git checkout), "pipx" or "pip"."""
    root = Path(__file__).resolve().parent.parent
    if (root / ".git").exists() or (root / "start.py").exists():
        return "source"
    if "pipx" in Path(sys.prefix).parts:
        return "pipx"
    return "pip"


def update_command():
    method = install_method()
    if method == "pipx":
        return ["pipx", "upgrade", PACKAGE]
    if method == "pip":
        return [sys.executable, "-m", "pip", "install", "--upgrade", PACKAGE]
    return ["git", "-C", str(Path(__file__).resolve().parent.parent), "pull"]


def update_command_text():
    method = install_method()
    if method == "pipx":
        return "pipx upgrade %s" % PACKAGE
    if method == "pip":
        return "pip3 install --upgrade %s" % PACKAGE if sys.platform == "darwin" \
            else "pip install --upgrade %s" % PACKAGE
    return "git pull"


def run_update():
    """Runs the update in the normal terminal and returns True on success."""
    try:
        return subprocess.call(update_command()) == 0
    except OSError:
        return False


class UpdateChecker:
    """Asks PyPI in the background, so the menu never waits for the network.

    status: "checking", "current", "available", "unpublished", "offline" or "off"."""

    def __init__(self, enabled=True, timeout=4.0):
        self.status = "checking" if enabled else "off"
        self.latest = None
        self.timeout = timeout
        if enabled:
            self.start()

    def start(self):
        self.status = "checking"
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        if os.environ.get("KEYFLOW_NO_UPDATE_CHECK"):
            self.status = "off"
            return
        try:
            with urllib.request.urlopen(PYPI_URL, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
            self.latest = data["info"]["version"]
            self.status = "available" if is_newer(self.latest) else "current"
        except urllib.error.HTTPError as exc:
            self.status = "unpublished" if exc.code == 404 else "offline"
        except (OSError, ValueError, KeyError):
            self.status = "offline"

    @property
    def available(self):
        return self.status == "available"
