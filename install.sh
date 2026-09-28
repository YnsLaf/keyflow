#!/bin/sh
# KeyFlow installer for macOS and Linux – made by yns.laf
#
# Installs everything KeyFlow needs:
#   1. checks that Python 3.8+ is available
#   2. installs pipx if it is missing (keeps KeyFlow in its own environment)
#   3. installs KeyFlow from PyPI (package "keyflow-typing", command "keyflow")
set -e

PACKAGE="keyflow-typing"

say() { printf '\033[1;36m==>\033[0m %s\n' "$1"; }
fail() { printf '\033[1;31mError:\033[0m %s\n' "$1" >&2; exit 1; }

say "Installing KeyFlow"

# 1. Python
if ! command -v python3 >/dev/null 2>&1; then
    if [ "$(uname)" = "Darwin" ]; then
        fail "Python 3 was not found. Run 'xcode-select --install' (or 'brew install python') and start this installer again."
    fi
    fail "Python 3 was not found. Install it with your package manager (e.g. 'sudo apt install python3 python3-venv') and start this installer again."
fi
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)'; then
    fail "KeyFlow needs Python 3.8 or newer. You have $(python3 --version 2>&1)."
fi
say "Found $(python3 --version 2>&1)"

# 2. pipx
if ! command -v pipx >/dev/null 2>&1; then
    say "Installing pipx"
    if command -v brew >/dev/null 2>&1; then
        brew install pipx
    elif command -v apt-get >/dev/null 2>&1 && command -v sudo >/dev/null 2>&1; then
        sudo apt-get install -y pipx || python3 -m pip install --user pipx
    else
        python3 -m pip install --user pipx
    fi
    python3 -m pipx ensurepath >/dev/null 2>&1 || pipx ensurepath >/dev/null 2>&1 || true
fi

PIPX="pipx"
command -v pipx >/dev/null 2>&1 || PIPX="python3 -m pipx"

# 3. KeyFlow
say "Installing $PACKAGE"
$PIPX install --force "$PACKAGE"

say "Done! Start KeyFlow with:  keyflow"
echo "    (If the command is not found, open a new terminal window first.)"
