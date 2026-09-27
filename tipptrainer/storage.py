"""Speichert Einstellungen, Verlauf, Tastenstatistik und eigene Texte als JSON."""

import copy
import json
import os
from pathlib import Path

SETTING_OPTIONS = {
    "language": ["de", "en"],
    "difficulty": ["easy", "normal", "hard"],
    "punctuation": [False, True],
    "numbers": [False, True],
    "lowercase": [False, True],
    "umlauts": [True, False],
    "strict": [False, True],
    "live_wpm": [True, False],
    "cursor": ["block", "underline"],
    "visible_lines": [2, 3, 4, 5],
    "text_width": [50, 60, 70, 80, 100],
    "bell": [False, True],
    "color_mode": ["256", "truecolor", "basic"],
    "daily_goal": [5, 10, 15, 20, 30, 45, 60],
}

DEFAULT_SETTINGS = {
    "language": "de",
    "difficulty": "normal",
    "punctuation": False,
    "numbers": False,
    "lowercase": False,
    "umlauts": True,
    "strict": False,
    "live_wpm": True,
    "cursor": "block",
    "visible_lines": 3,
    "text_width": 70,
    "bell": False,
    "color_mode": "256",
    "daily_goal": 15,
}

MENU_OPTIONS = {
    "time": [15, 30, 60, 120],
    "words": [10, 25, 50, 100],
    "free": ["words", "sentences", "numbers", "symbols", "mixed"],
    "endless": [1, 3, 5],
    "stories": ["easy", "medium", "hard", "extreme"],
    "sentences": [1, 3, 5, 10],
    "numbers": [10, 25, 50],
    "symbols": [10, 25, 50],
    "mixed": [25, 50, 100],
    "quotes": ["random", "short", "medium", "long"],
    "weak": [25, 50, 100],
}

MENU_DEFAULTS = {
    "time": 30,
    "words": 25,
    "free": "words",
    "endless": 1,
    "stories": "easy",
    "sentences": 3,
    "numbers": 25,
    "symbols": 25,
    "mixed": 50,
    "quotes": "random",
    "weak": 25,
}


def default_path():
    base = os.environ.get("TIPPTRAINER_HOME")
    folder = Path(base) if base else Path.home() / ".tipptrainer"
    return folder / "daten.json"


def _valid(value, options):
    # bool ist in Python eine Unterklasse von int – deshalb den Typ mitprüfen.
    return any(value == o and type(value) is type(o) for o in options)


class Store:
    def __init__(self, path=None):
        self.path = Path(path) if path else default_path()
        self.settings = copy.deepcopy(DEFAULT_SETTINGS)
        self.settings["menu"] = dict(MENU_DEFAULTS)
        self.history = []
        self.key_stats = {}
        self.custom_texts = []
        self.achievements = {}
        self.load_error = None
        self.load()

    def load(self):
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("kein JSON-Objekt")
        except (OSError, ValueError) as exc:
            backup = self.path.with_name(self.path.stem + ".defekt.json")
            try:
                os.replace(self.path, backup)
            except OSError:
                pass
            self.load_error = "Die Datei %s war beschädigt (%s) und wurde nach %s verschoben." % (
                self.path, exc, backup.name)
            return
        stored = data.get("settings", {})
        for key, options in SETTING_OPTIONS.items():
            if key in stored and _valid(stored[key], options):
                self.settings[key] = stored[key]
        menu = stored.get("menu", {})
        for key, options in MENU_OPTIONS.items():
            if key in menu and _valid(menu[key], options):
                self.settings["menu"][key] = menu[key]
        self.history = [e for e in data.get("history", []) if isinstance(e, dict) and "ts" in e]
        self.key_stats = {k: list(v) for k, v in data.get("key_stats", {}).items()
                          if isinstance(v, list) and len(v) == 2}
        self.custom_texts = [t for t in data.get("custom_texts", [])
                             if isinstance(t, dict) and t.get("text")]
        self.achievements = dict(data.get("achievements", {}))

    def save(self):
        data = {
            "version": 1,
            "settings": self.settings,
            "history": self.history,
            "key_stats": self.key_stats,
            "custom_texts": self.custom_texts,
            "achievements": self.achievements,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_name(self.path.name + ".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, self.path)

    def add_result(self, entry, key_attempts=None, key_errors=None):
        self.history.append(entry)
        for ch, n in (key_attempts or {}).items():
            self.key_stats.setdefault(ch, [0, 0])[0] += n
        for ch, n in (key_errors or {}).items():
            self.key_stats.setdefault(ch, [0, 0])[1] += n
        self.save()

    def reset_stats(self):
        self.history = []
        self.key_stats = {}
        self.achievements = {}
        self.save()
