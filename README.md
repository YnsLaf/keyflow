# KeyFlow

*made by yns.laf*

KeyFlow is a typing trainer for the terminal, written in Python. It runs on
macOS, Linux and Windows and speaks **English and German**. On first start you
choose the language of the whole tool.

```
K E Y F L O W  made by yns.laf                             Streak 4 days
Today 6.5/15 min ████░░░░░░░░          14 days ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■
────────────────────────────────────────────────────────────────────────
❯ 1  Continue: Word test · 25 words     ╭──────────────────────────╮
  2  Practice                           │ 9 more min to your daily │
  3  Texts & stories                    │ goal.                    │
  4  Numbers & symbols                  ╰──┬───────────────────────╯
  5  Progress                              ╵
  6  Settings                             ╭───────╮
  7  Quit                                 │ ◕   ◕ │
                                          │   ‿   │
                                          ╰─┬───┬─╯
                                            ╵   ╵
                                            Flow
```

## Installation

You need Python 3.8 or newer. Everything else (the `colorama` library) is
installed automatically.

### macOS and Linux – one command

```bash
curl -fsSL https://raw.githubusercontent.com/YnsLaf/keyflow/main/install.sh | sh
```

The installer checks Python, installs [pipx](https://pipx.pypa.io) if needed
and then installs KeyFlow. Afterwards start it with:

```bash
keyflow
```

### With pip

```bash
pip install keyflow-typing
keyflow
```

On macOS, pipx is the cleanest way:

```bash
brew install pipx
pipx ensurepath
pipx install keyflow-typing
```

### Windows

```bat
py -m pip install keyflow-typing
keyflow
```

Windows Terminal works best.

### Updating

```bash
pipx upgrade keyflow-typing        # or: pip install -U keyflow-typing
```

> The package on PyPI is called **keyflow-typing** (the name "keyflow" was
> already taken). The command is simply `keyflow`.

## First start

Before KeyFlow starts for the first time, it asks:

```
Choose your language  ·  Wähle deine Sprache
❯ 1  English
  2  Deutsch
```

Menus, hints, statistics, achievements, Flow the mascot and the practice texts
then use that language. You can change it any time in the settings.

## Modes

| Mode | What happens |
|---|---|
| **Time test** | Type as many words as possible in 15, 30, 60 or 120 seconds. |
| **Word test** | Type 10, 25, 50 or 100 words as fast as you can. |
| **Free mode** | No limit – the text never ends. Esc finishes and saves. Words, sentences, numbers, symbols or mixed. |
| **Endless mode** | Survival: you start with 10 seconds, every correct word adds time, every mistake costs 1 second. Every 20 words the level rises and it gets harder. |
| **Stories** | 40 stories in English and German: 10 easy, 10 medium, 10 hard, 10 extreme. |
| **Sentences** | Generated, grammatically correct sentences. |
| **Numbers** | Prices, times, dates, sums, units and phone numbers. |
| **Symbols** | Brackets, operators, paths, e-mails and code snippets. |
| **Mixed (pro)** | Words, capitals, punctuation, numbers and symbols all mixed up. |
| **Quotes & proverbs** | Proverbs and famous lines from Shakespeare, Austen, Dickens, Goethe, Kafka … |
| **Weak keys** | Generates text with exactly the keys you get wrong the most. |
| **Your own text** | Paste a text or load a `.txt` file. Long texts are practiced in parts. |

## While typing

- A keyboard under the text shows which key comes next. With capitals and
  symbols the right ⇧ / ⌥ / AltGr key lights up too, and a hint tells you which
  finger to use. Mistakes flash red.
- The word you are typing is highlighted, and a flowing progress line runs
  above the text.

| Key | Action |
|---|---|
| Backspace | delete last character |
| Ctrl + Backspace (macOS: Option + Backspace) | delete whole word |
| Tab | restart with a new text |
| Esc | back to the menu (free and endless mode: finish and save) |

## Progress

- **Result after every test:** WPM and accuracy in big digits, raw WPM,
  consistency, a speed graph, the keys you missed and new records.
- **Records** per mode, length and language.
- **History:** chart of your recent tests and your trend.
- **Keyboard view:** every key colored by your error rate.
- **Activity calendar** like on GitHub, plus current and longest streak.
- **Daily goal and streak** at the top of the menu.
- **29 achievements**.

## Look

- **Background:** KeyFlow colors the terminal when it starts and restores it
  when you quit.
  - The default is "Glass": hue 0°, saturation 0 %, brightness 10 %, opacity 30 %.
  - In the macOS Terminal this uses a Terminal profile called "KeyFlow", which
    KeyFlow creates once (a window briefly opens and closes).
  - The window title then only shows "KeyFlow".
- **Moving colors:** flowing gradients, a shimmering menu and a pulsing next key.
- **Flow**, the mascot, blinks, bobs and gives you tips.

## Settings

Language, text language, keyboard layout (QWERTZ/QWERTY), word length,
punctuation, numbers, lowercase only, umlauts, strict mode, live WPM, cursor,
visible lines, text width, sound, background, color mode, moving colors,
keyboard while typing, daily goal, reset statistics.

## Data

Everything is stored in `~/.keyflow/daten.json`. Use `keyflow --data FILE` or the
environment variable `KEYFLOW_HOME` to choose another place.

## Development

```bash
git clone https://github.com/YnsLaf/keyflow
cd tipptrainer
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
keyflow
python -m unittest discover -s tests
```

A new release on GitHub publishes the package to PyPI automatically
(`.github/workflows/publish.yml`). Raise the version in `pyproject.toml` and
`keyflow/__init__.py` first.
