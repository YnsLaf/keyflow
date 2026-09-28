"""Programmablauf: Hauptmenü, Tests starten, Ergebnisse speichern."""

import argparse
import random
import sys
import time
import webbrowser
from datetime import date, datetime
from pathlib import Path

from . import i18n, screens, stats, stories, textgen, ui, updates
from . import terminal as T
from .engine import TypingTest
from .i18n import tr
from .storage import Store
from . import __version__


ENDLESS_START = 10.0         # Startzeit im Unendlich-Modus (Sekunden)
ENDLESS_MAX = 20.0           # mehr Zeitvorrat als das gibt es nicht
ENDLESS_PENALTY = 1.0        # Sekunden Abzug pro Tippfehler
ENDLESS_WORDS_PER_LEVEL = 20


def endless_target_wpm(level):
    """Tempo, mit dem man im jeweiligen Level genau gleich viel Zeit gewinnt, wie
    man verbraucht. Wer schneller tippt, baut Vorrat auf."""
    return 25 + 5 * level


class Mode:
    """Beschreibt einen Test.

    kind:  "time" (Zeitlimit), "text" (fester Text), "free" (endlos) oder
           "endless" (Unendlich-Modus: Zeit läuft ab, richtige Wörter bringen Zeit).
    source: liefert bei "time"/"free" immer neue Textstücke.
    make_text: liefert bei "text" (text, hinweis)."""

    def __init__(self, key, label, kind, limit=0, source=None, make_text=None,
                 on_complete=None, repeatable=True, count_words=False, extra=None):
        self.key = key
        self.label = label
        self.kind = kind
        self.limit = limit
        self.source = source
        self.make_text = make_text
        self.on_complete = on_complete
        self.repeatable = repeatable and kind == "text"
        self.count_words = count_words
        self.extra = extra          # () -> zusätzliche Felder für den Verlauf
        self.state = None           # Laufzeitwerte des Unendlich-Modus


class App:
    def __init__(self, term, store, rng=None):
        self.term = term
        self.store = store
        self.rng = rng or random.Random()
        i18n.set_language(store.settings["ui_language"])

    # --- Hauptschleife ---------------------------------------------------
    def apply_look(self):
        """Farbmodus, Animationen und Terminal-Hintergrund aus den Einstellungen."""
        ui.configure(self.settings)
        _, rgb, opacity = ui.BACKGROUNDS[self.settings["background"]]
        if opacity is not None:
            opacity = self.settings["glass_opacity"] / 100.0
        self.term.set_background(rgb, opacity)

    def set_ui_language(self, lang):
        """Oberfläche und Übungstexte auf eine Sprache umstellen."""
        i18n.set_language(lang)
        self.settings["ui_language"] = lang
        self.settings["language"] = lang
        self.store.save()

    def run(self):
        self.apply_look()
        if self.store.needs_language:
            lang = screens.language_picker(self.term)
            self.settings["kb_layout"] = lang
            self.set_ui_language(lang)
            self.store.needs_language = False
        if self.store.load_error:
            path, error, backup = self.store.load_error
            ui.message(self.term, tr("Hinweis", "Note"), [
                tr("Die Datei %s war beschädigt (%s) und wurde nach %s verschoben.",
                   "The file %s was damaged (%s) and was moved to %s.") % (path, error, backup)])
        self.update_achievements()
        self.updater = updates.UpdateChecker(enabled=self.settings["check_updates"])
        index = 0
        while True:
            action, index = screens.main_menu(self.term, self.store, index, self.updater)
            if action in (None, "quit"):
                return
            if action == "quick":
                self.open(self.settings["menu"]["last"])
            elif action == "settings":
                screens.settings_screen(self.term, self.store, on_look_change=self.apply_look,
                                        on_language_change=self.set_ui_language)
            elif action == "info":
                self.info()
            else:
                self.category(action)

    def info(self):
        index = 0
        while True:
            action, index = screens.info_screen(self.term, self.store, self.updater, index)
            if action in (None, "back"):
                return
            if action == "github":
                webbrowser.open(updates.GITHUB_USER_URL)
            elif action == "repo":
                webbrowser.open(updates.GITHUB_REPO_URL)
            elif action == "pypi":
                webbrowser.open(updates.PROJECT_URL)
            elif action == "check":
                self.updater.start()
            elif action == "update":
                self.update_now()

    def update_now(self):
        with self.term.cooked():
            print(tr("KeyFlow wird aktualisiert: ", "Updating KeyFlow: ") + updates.update_command_text() + "\n")
            ok = updates.run_update()
            print()
            if ok:
                print(tr("Fertig! Starte KeyFlow neu, um die neue Version zu nutzen.",
                         "Done! Restart KeyFlow to use the new version."))
            else:
                print(tr("Das Update hat nicht geklappt. Du kannst es selbst ausführen mit:",
                         "The update did not work. You can run it yourself with:"))
                print("  " + updates.update_command_text())
            try:
                input(tr("\nWeiter mit Enter …", "\nPress Enter to continue …"))
            except (EOFError, KeyboardInterrupt):
                pass

    def category(self, category):
        index = 0
        while True:
            action, index = screens.category_menu(self.term, self.store, category, index)
            if action in (None, "back"):
                return
            self.open(action)

    def open(self, action):
        """Startet einen Modus oder öffnet einen Bildschirm."""
        if action == "stats":
            screens.stats_screen(self.term, self.store)
        elif action == "activity":
            screens.activity_screen(self.term, self.store)
        elif action == "achievements":
            screens.achievements_screen(self.term, self.store)
        elif action == "custom":
            self.custom_texts()
        else:
            if self.settings["menu"]["last"] != action:
                self.settings["menu"]["last"] = action
                self.store.save()
            if action == "stories":
                self.stories_menu()
            else:
                self.run_mode(self.build_mode(action))

    # --- Modi ------------------------------------------------------------
    @property
    def settings(self):
        return self.store.settings

    def _lang(self):
        return self.settings["language"]

    def _word_variant(self):
        s = self.settings
        key = s["language"] + ("-p" if s["punctuation"] else "") + ("-n" if s["numbers"] else "")
        label = s["language"].upper()
        if s["punctuation"]:
            label += tr(" · Satzzeichen", " · punctuation")
        if s["numbers"]:
            label += tr(" · Zahlen", " · numbers")
        return key, label

    def _word_source(self):
        s = self.settings
        return textgen.WordSource(s["language"], s["difficulty"], s["punctuation"],
                                  s["numbers"], s["lowercase"], rng=self.rng)

    def _free_source(self, kind):
        lang = self._lang()
        if kind == "sentences":
            return textgen.SentenceSource(lang, rng=self.rng)
        if kind == "numbers":
            return textgen.NumberSource(lang, rng=self.rng)
        if kind == "symbols":
            return textgen.SymbolSource(lang, rng=self.rng)
        if kind == "mixed":
            return textgen.MixedSource(lang, self.settings["difficulty"], rng=self.rng)
        return self._word_source()

    def _fixed(self, make_source, count):
        return lambda: (make_source().text(count), "")

    def build_mode(self, action):
        value = self.settings["menu"][action]
        lang = self._lang()
        up = lang.upper()
        if action == "time":
            variant, label = self._word_variant()
            return Mode("zeit-%d-%s" % (value, variant), tr("Zeit %d s · %s", "Time %d s · %s") % (value, label),
                        "time", limit=value, source=self._word_source())
        if action == "words":
            variant, label = self._word_variant()
            return Mode("woerter-%d-%s" % (value, variant), "%s · %s" % (screens.words_label(value), label),
                        "text", make_text=self._fixed(self._word_source, value), count_words=True)
        if action == "free":
            if value == "words":
                variant, label = self._word_variant()
            else:
                variant, label = lang, up
            return Mode("frei-%s-%s" % (value, variant),
                        tr("Freier Modus · %s · %s", "Free mode · %s · %s") % (screens.free_label(value), label),
                        "free", source=self._free_source(value))
        if action == "endless":
            source = textgen.EndlessSource(lang, rng=self.rng)
            mode = Mode("unendlich-%d-%s" % (value, lang),
                        tr("Unendlich ab Level %d · %s", "Endless from level %d · %s") % (value, up),
                        "endless", limit=value, source=source)
            mode.extra = lambda: {"score": mode.state["words"], "level": mode.state["level"]}
            return mode
        if action == "sentences":
            return Mode("saetze-%d-%s" % (value, lang), "%s · %s" % (
                tr("1 Satz", "1 sentence") if value == 1 else tr("%d Sätze", "%d sentences") % value, up),
                "text",
                make_text=self._fixed(lambda: textgen.SentenceSource(lang, rng=self.rng), value))
        if action == "numbers":
            return Mode("zahlen-%d-%s" % (value, lang), tr("Zahlen %d · %s", "Numbers %d · %s") % (value, up),
                        "text",
                        make_text=self._fixed(lambda: textgen.NumberSource(lang, rng=self.rng), value))
        if action == "symbols":
            return Mode("zeichen-%d-%s" % (value, lang), tr("Sonderzeichen %d · %s", "Symbols %d · %s")
                        % (value, up), "text",
                        make_text=self._fixed(lambda: textgen.SymbolSource(lang, rng=self.rng), value))
        if action == "mixed":
            return Mode("gemischt-%d-%s" % (value, lang), tr("Gemischt %d · %s", "Mixed %d · %s") % (value, up),
                        "text",
                        make_text=self._fixed(lambda: textgen.MixedSource(
                            lang, self.settings["difficulty"], rng=self.rng), value))
        if action == "quotes":
            def make_quote():
                text, source = textgen.pick_quote(lang, value, self.rng)
                return text, "— " + source
            return Mode("zitat-%s-%s" % (value, lang), tr("Zitat (%s) · %s", "Quote (%s) · %s") % (
                screens.quote_label(value), up), "text", make_text=make_quote)
        if action == "weak":
            def make_weak():
                weak = [row[0] for row in stats.weak_keys(self.store.key_stats)]
                source = textgen.WeakSource(lang, weak, rng=self.rng)
                if weak:
                    note = tr("Fokus auf: ", "Focus on: ") + "  ".join(weak)
                else:
                    note = tr("Noch zu wenig Daten – übe erst ein paar andere Tests.",
                              "Not enough data yet – do a few other tests first.")
                return source.text(value), note
            return Mode("schwaechen-%d-%s" % (value, lang),
                        tr("Schwächen-Training %d · %s", "Weak keys %d · %s") % (value, up),
                        "text", make_text=make_weak, count_words=True)
        raise ValueError(action)

    # --- Ablauf eines Tests ----------------------------------------------
    def run_mode(self, mode):
        text = note = None
        while True:
            if mode.kind == "text" and text is None:
                text, note = mode.make_text()
                text = textgen.finalize(text, self.settings)
            outcome, test = self.run_test(mode, text, note)
            if outcome == "abort":
                return
            if outcome == "restart":
                text = None
                continue
            result = test.result()
            info = self.save_result(mode, result)
            if info["saved"] and mode.on_complete and test.complete():
                mode.on_complete(result)
            choice = screens.result_screen(self.term, mode, result, info, self.store)
            if choice == "menu":
                return
            if choice == "next":
                text = None

    def run_test(self, mode, text, note):
        settings = self.settings
        endless = mode.kind == "endless"
        if endless:
            mode.state = {"budget": ENDLESS_START, "level": mode.limit, "words": 0, "credited": set()}
            mode.source.level = mode.limit
        if mode.kind == "text":
            target = text
        else:
            target = self._next_chunk(mode)
            while len(target) < (150 if endless else 400):
                target += " " + self._next_chunk(mode)
        test = TypingTest(target, strict=settings["strict"])
        wrong = None  # (falsch gedrückte Taste, Zeitpunkt) für das rote Aufblinken
        self.term.flush_input()
        while True:
            now = time.monotonic()
            if test.started:
                test.sample(now)
                if mode.kind == "time" and test.elapsed(now) >= mode.limit:
                    test.finish(test.start_time + mode.limit)
                    return "done", test
                if endless and test.elapsed(now) >= mode.state["budget"]:
                    test.finish(test.start_time + max(0.0, mode.state["budget"]))
                    return "done", test
            if mode.kind != "text" and len(test.target) - test.pos < (120 if endless else 250):
                test.extend(" " + self._next_chunk(mode))
            flash = wrong[0] if wrong and now - wrong[1] < 0.35 else None
            screens.draw_test(self.term, test, now, mode, settings, note, flash)

            key = self.term.read_key(0.08 if test.started or settings["animations"] else 0.5)
            if key is None:
                continue
            if key in (T.ESC, T.CTRL_C):
                if mode.kind in ("free", "endless") and test.pos > 0:
                    test.finish(time.monotonic())
                    return "done", test
                return "abort", test
            if key == T.TAB:
                return "restart", test
            if key == T.BACKSPACE:
                test.backspace()
            elif key == T.CTRL_BACKSPACE:
                test.backspace_word()
            elif T.is_char(key):
                ok = test.type_char(key, time.monotonic())
                if ok is False:
                    wrong = (key, time.monotonic())
                    if settings["bell"]:
                        self.term.bell()
                if endless and ok is not None:
                    self._endless_step(mode, test, ok)
                if mode.kind == "text" and test.complete():
                    test.finish(time.monotonic())
                    return "done", test

    def _endless_step(self, mode, test, ok):
        """Unendlich-Modus: Fehler kosten Zeit, fertige Wörter bringen Zeit."""
        state = mode.state
        now_elapsed = test.elapsed(time.monotonic())
        if not ok:
            state["budget"] -= ENDLESS_PENALTY
            return
        end = test.pos - 1
        if test.target[end] != " " or end in state["credited"]:
            return
        start = test.target.rfind(" ", 0, end) + 1
        if not all(test.marks[start:end + 1]):
            return
        state["credited"].add(end)
        state["words"] += 1
        seconds_per_char = 60.0 / (5 * endless_target_wpm(state["level"]))
        state["budget"] = min(state["budget"] + (end + 1 - start) * seconds_per_char,
                              now_elapsed + ENDLESS_MAX)
        state["level"] = mode.limit + state["words"] // ENDLESS_WORDS_PER_LEVEL
        mode.source.level = state["level"]

    def _next_chunk(self, mode):
        return textgen.finalize(mode.source.chunk(), self.settings)

    def save_result(self, mode, result):
        if result["keystrokes"] < 5 or result["duration"] < 1:
            return {"saved": False}
        entry = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "mode": mode.key,
            "label": mode.label,
            "lang": self._lang(),
            "wpm": result["wpm"],
            "raw": result["raw"],
            "acc": result["acc"],
            "duration": result["duration"],
            "chars": result["chars"],
            "errors": result["errors"],
            "consistency": result["consistency"],
        }
        if mode.extra:
            entry.update(mode.extra())
        previous = stats.records(self.store.history).get(mode.key)
        record = stats.record_eligible(entry) and (
            previous is None or stats.record_value(entry) > stats.record_value(previous))
        self.store.add_result(entry, result["key_attempts"], result["key_errors"])
        new = self.update_achievements()
        return {"saved": True, "record": record, "previous": previous, "achievements": new,
                "entry": entry}

    def update_achievements(self):
        got = stats.achieved(self.store.history, self.settings["daily_goal"], date.today())
        new = [key for key, _, _ in stats.ACHIEVEMENTS
               if key in got and key not in self.store.achievements]
        if new:
            stamp = datetime.now().isoformat(timespec="seconds")
            for key in new:
                self.store.achievements[key] = stamp
            self.store.save()
        return new

    # --- Geschichten ------------------------------------------------------
    def stories_menu(self):
        level = self.settings["menu"]["stories"]
        index = 0
        while True:
            action, index, _ = screens.stories_menu(self.term, self.store, level, index)
            if action is None or action == "back":
                return
            self.run_mode(self._story_mode(level, action))

    def _story_mode(self, level, first):
        lang = self._lang()
        items = stories.stories_for(lang, level)
        label = stories.level_label(level)
        story = tr("Geschichte", "Story")
        state = {"i": first, "shown": first}

        def make_text():
            state["shown"] = state["i"]
            title, text = items[state["i"]]
            return text, "\"%s\" · %s %d/%d (%s)" % (title, story, state["i"] + 1, len(items), label)

        def on_complete(result):
            state["i"] = (state["shown"] + 1) % len(items)

        key = "geschichte-%s" % level + ("-en" if lang == "en" else "")
        mode = Mode(key, "%s (%s)" % (story, label), "text", make_text=make_text, on_complete=on_complete)
        mode.extra = lambda: {"story": stories.story_id(level, state["shown"]), "lang": lang,
                              "label": "%s (%s) · %s" % (story, label, items[state["shown"]][0])}
        return mode

    # --- Eigene Texte ----------------------------------------------------
    def custom_texts(self):
        index = 0
        while True:
            action, index, key = screens.custom_menu(self.term, self.store, index)
            if action in (None, "back"):
                return
            if action == "new":
                self._add_pasted_text()
            elif action == "file":
                self._add_file_text()
            elif isinstance(action, int):
                entry = self.store.custom_texts[action]
                if key in (T.DELETE, "d", "D"):
                    title = entry.get("title") or entry["text"][:30]
                    if ui.confirm(self.term, tr("Text löschen", "Delete text"),
                                  tr("„%s“ wirklich löschen?", "Really delete \"%s\"?") % title):
                        del self.store.custom_texts[action]
                        self.store.save()
                        index = max(0, index - 1)
                else:
                    self.run_mode(self._custom_mode(entry))

    def _custom_mode(self, entry):
        title = entry.get("title") or entry["text"][:30]
        state = {}

        def make_text():
            start, end = textgen.custom_chunk(entry["text"], entry.get("pos", 0))
            state["end"] = end
            note = ""
            if end - start < len(entry["text"]):
                note = tr("Abschnitt: %d %% – %d %% des Textes", "Part: %d %% – %d %% of the text") % (
                    100 * start // len(entry["text"]), 100 * end // len(entry["text"]))
            return entry["text"][start:end].strip(), note

        def on_complete(result):
            end = state.get("end", 0)
            entry["pos"] = 0 if end >= len(entry["text"]) else end
            self.store.save()

        return Mode("eigener", tr("Eigener Text · %s", "Own text · %s") % title[:40], "text",
                    make_text=make_text, on_complete=on_complete)

    def _save_custom(self, title, text):
        text = textgen.normalize_text(text)
        if not text:
            ui.message(self.term, tr("Eigener Text", "Your own text"),
                       [tr("Der Text ist leer – nichts gespeichert.", "The text is empty – nothing saved.")])
            return
        title = textgen.normalize_text(title) or text[:30]
        self.store.custom_texts.append({
            "title": title[:60], "text": text, "pos": 0,
            "added": datetime.now().isoformat(timespec="seconds"),
        })
        self.store.save()

    def _add_pasted_text(self):
        lines, title = [], ""
        with self.term.cooked():
            print(tr("EIGENEN TEXT EINFÜGEN\n", "PASTE YOUR OWN TEXT\n"))
            print(tr("Füge deinen Text ein (z. B. mit Cmd+V, Strg+Umschalt+V oder Rechtsklick).",
                     "Paste your text (e.g. with Cmd+V, Ctrl+Shift+V or right-click)."))
            print(tr("Zum Abschließen zweimal Enter drücken – oder eine Zeile mit nur einem Punkt.\n",
                     "Press Enter twice to finish – or type a line with just a period.\n"))
            empty = 0
            try:
                while True:
                    line = input()
                    if line.strip() == ".":
                        break
                    if not line.strip():
                        empty += 1
                        if empty >= 2 or not lines:
                            break
                        continue
                    empty = 0
                    lines.append(line)
                if lines:
                    title = input(tr("\nTitel (optional, Enter = automatisch): ",
                                     "\nTitle (optional, Enter = automatic): "))
            except (EOFError, KeyboardInterrupt):
                lines = []
        if lines:
            self._save_custom(title, " ".join(lines))

    def _add_file_text(self):
        with self.term.cooked():
            print(tr("TEXT AUS DATEI LADEN\n", "LOAD TEXT FROM FILE\n"))
            try:
                raw = input(tr("Pfad zur Datei (leer = abbrechen): ",
                               "Path to the file (empty = cancel): ")).strip().strip("\"'")
            except (EOFError, KeyboardInterrupt):
                raw = ""
        if not raw:
            return
        path = Path(raw).expanduser()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            ui.message(self.term, tr("Datei laden", "Load file"),
                       [tr("Die Datei konnte nicht gelesen werden:", "The file could not be read:"), str(exc)])
            return
        self._save_custom(path.stem, text)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="keyflow",
                                     description="KeyFlow – a typing trainer for the terminal. "
                                                 "Made by YnsLaf")
    parser.add_argument("--data", "--daten", dest="data", metavar="FILE",
                        help="use a different data file (default: ~/.keyflow/daten.json)")
    parser.add_argument("--version", action="version", version="KeyFlow %s" % __version__)
    args = parser.parse_args(argv)

    store = Store(args.data)
    try:
        with T.Terminal() as term:
            try:
                App(term, store).run()
            except (KeyboardInterrupt, EOFError):
                pass
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1
    days = stats.daily_seconds(store.history)
    today_minutes = days.get(date.today(), 0) / 60
    print(tr("Bis bald! Heute geübt: %s min.", "See you soon! Practiced today: %s min.")
          % ui.fmt_minutes(today_minutes * 60))
    return 0
