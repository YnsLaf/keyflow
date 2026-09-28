# Keyflow

*made by yns.laf*

Keyflow ist ein Tipptrainer fürs Terminal, geschrieben in Python mit
[colorama](https://pypi.org/project/colorama/). Er läuft unter Windows, Linux
und macOS.

```
K E Y F L O W  made by yns.laf                  Serie 4 Tage  ·  Bestwert 85 WPM
Heute 6,5/15 min ████░░░░░░░░          14 Tage ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■
────────────────────────────────────────────────────────────────────────
▶ Zeit-Test               ◀ 30 s ▶
  Wörter-Test               25 Wörter
  Freier Modus              Wörter
  Unendlich-Modus           ab Level 1
  Geschichten               einfach (10)
  Sätze                     3 Sätze
  Zahlen                    25 Zahlen
  Sonderzeichen             25 Gruppen
  Gemischt (Profi)          50 Teile
  Zitate & Sprichwörter     zufällig
  Schwächen-Training        25 Wörter
  Eigener Text              2 gespeichert
  Statistik & Rekorde
  Aktivität
  Erfolge                   8/29
  Einstellungen
  Beenden
```

## Starten

Du brauchst Python 3.8 oder neuer.

### macOS und Linux

```bash
git clone https://github.com/YnsLaf/keyflow
cd tipptrainer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python start.py
```

Beim nächsten Mal reicht:

```bash
cd tipptrainer
source .venv/bin/activate
python start.py
```

Auf dem Mac heißen die Befehle ohne Umgebung `python3` und `pip3`. Wenn beim
ersten `python3` ein Fenster die „Befehlszeilenentwickler-Tools“ installieren
will, bestätige das und starte die Befehle danach noch einmal.

### Mit einem Befehl starten (macOS/Linux)

Damit sich der Trainer öffnet, sobald du `trainer` eingibst, egal in welchem
Ordner:

```bash
echo 'alias trainer="$HOME/tipptrainer/.venv/bin/python $HOME/tipptrainer/start.py"' >> ~/.zshrc && source ~/.zshrc
```

Das setzt voraus, dass der Ordner unter `~/tipptrainer` liegt und `.venv`
angelegt ist. Mit bash statt zsh nimm `~/.bashrc` statt `~/.zshrc`.

### Windows

```bat
git clone https://github.com/YnsLaf/keyflow
cd tipptrainer
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python start.py
```

Am besten funktioniert das *Windows Terminal*.

### Als Befehl installieren

Bei aktiver Umgebung installiert `pip install .` den Befehl `keyflow`.
Er funktioniert, solange die Umgebung aktiv ist.

Das Terminalfenster sollte mindestens 80 × 24 Zeichen groß sein. Beim Starten und
Beenden wird das Terminal komplett geleert.

## Modi

| Modus | Was passiert |
|---|---|
| **Zeit-Test** | Du tippst so viele Wörter wie möglich in 15, 30, 60 oder 120 Sekunden. |
| **Wörter-Test** | Du tippst 10, 25, 50 oder 100 Wörter so schnell wie möglich. |
| **Freier Modus** | Kein Limit, der Text geht immer weiter. Esc beendet den Test und speichert ihn. Als Text gibt es Wörter, Sätze, Zahlen, Sonderzeichen oder alles gemischt. |
| **Unendlich-Modus** | Überlebensmodus: Du startest mit 10 Sekunden. Jedes richtig getippte Wort bringt Zeit, jeder Fehler kostet 1 Sekunde. Alle 20 Wörter steigt das Level: Die Wörter werden länger, dann kommen Satzzeichen, Zahlen und Sonderzeichen dazu, und pro Wort gibt es weniger Zeit. Du kannst ab Level 1, 3 oder 5 starten. Rekord ist die Zahl der geschafften Wörter. |
| **Geschichten** | 40 Geschichten auf Deutsch: 10 einfache, 10 mittlere, 10 schwere und 10 extreme. Einfach heißt kurze Sätze und bekannte Wörter. Extrem heißt lange Texte voller Zahlen, Einheiten, Klammern, Paragrafen und Fachwörter. Die Liste zeigt, welche du schon geschafft hast und mit welchem Tempo. Nach einer Geschichte geht es mit Enter direkt zur nächsten. |
| **Sätze** | Automatisch erzeugte, grammatisch richtige Sätze auf Deutsch oder Englisch. |
| **Zahlen** | Preise, Uhrzeiten, Datumsangaben, Rechnungen, Einheiten und Telefonnummern. |
| **Sonderzeichen** | Klammern, Operatoren, Pfade, E-Mail-Adressen und Code-Schnipsel. |
| **Gemischt (Profi)** | Wörter, Großbuchstaben, Satzzeichen, Zahlen und Sonderzeichen durcheinander. |
| **Zitate & Sprichwörter** | Sprichwörter und berühmte Textstellen, z. B. von Goethe, Schiller, Kafka oder den Brüdern Grimm. |
| **Schwächen-Training** | Erzeugt Text mit genau den Tasten, bei denen du die meisten Fehler machst. |
| **Eigener Text** | Du fügst einen Text ein oder lädst eine `.txt`-Datei. Lange Texte werden in Abschnitten geübt, und der Trainer merkt sich, wo du stehst. |

Im Hauptmenü wählst du Länge oder Variante direkt mit **← →** aus.

## Aussehen

- **Hintergrund:** Beim Start färbt Keyflow den Terminal-Hintergrund ein.
  - Standard ist „Glas (yns.laf)“: Farbton 0°, Sättigung 0 %, Helligkeit 10 %,
    Deckkraft 30 %.
  - Außerdem gibt es Mitternacht, Graphit, Ozean, Wald, Aubergine, Schwarz und
    „wie im Terminal“.
  - Beim Beenden kommt dein eigener Hintergrund zurück.
  - Im Mac-Terminal passiert das über AppleScript. Beim ersten Start fragt macOS
    eventuell, ob das Terminal gesteuert werden darf.
  - Die Deckkraft deines Profils bleibt erhalten.
  - In anderen Terminals (iTerm2, Windows Terminal, die meisten Linux-Terminals)
    funktioniert es über eine Steuersequenz.
- **Bewegte Farben:**
  - Der Titel und die Fortschrittslinie über dem Text laufen als Farbverlauf.
  - Die nächste Taste pulsiert.
  - In den Einstellungen lässt sich das abschalten.
- **Tastatur beim Tippen:** Unter dem Text ist eine Tastatur zu sehen.
  - Die nächste Taste leuchtet, bei Großbuchstaben und Sonderzeichen auch die
    passende Umschalt-, AltGr- bzw. ⌥-Taste.
  - Darunter steht, mit welchem Finger du die Taste drückst.
  - Eine falsch gedrückte Taste blinkt kurz rot.
  - Das Wort, an dem du gerade tippst, ist hervorgehoben.
  - Mac-Tastaturen (⌥) werden automatisch erkannt.

## Tasten beim Tippen

| Taste | Wirkung |
|---|---|
| Rücktaste | letztes Zeichen löschen |
| Strg + Rücktaste (macOS: Option + Rücktaste) | ganzes Wort löschen |
| Tab | Test mit neuem Text neu starten |
| Esc | zurück ins Menü (im freien und im Unendlich-Modus: beenden und speichern) |

## Statistik, Rekorde und Aktivität

- **Ergebnis nach jedem Test**
  - WPM in großen Ziffern und Genauigkeit
  - Roh-WPM, Konstanz, Anzahl der Fehler und ein WPM-Verlauf über die Zeit
  - welche Tasten dir Probleme gemacht haben
  - eine Meldung bei neuem Rekord
- **Rekorde** werden je Modus, Länge und Sprache geführt. Mit Satzzeichen oder
  Zahlen gibt es eigene Rekorde.
- **Verlauf**
  - Balkendiagramm deiner letzten Tests
  - Trend im Vergleich zu den zehn Tests davor
- **Tastatur-Ansicht**
  - Die QWERTZ- bzw. QWERTY-Tastatur ist nach deiner Fehlerquote eingefärbt,
    von grün bis rot.
  - Darunter stehen deine schwächsten Tasten.
- **Aktivitätskalender** wie auf GitHub:
  - Er zeigt das letzte Jahr, und jeder Tag ist ein Kästchen. Je länger du
    geübt hast, desto kräftiger ist das Grün.
  - Die Farbe richtet sich nach deinem Tagesziel.
  - Dazu kommen aktuelle und längste Serie, aktive Tage und die Übungszeit.
  - Mit ← → blätterst du in ältere Zeiträume.
- **Tagesziel und Serie** stehen immer oben im Hauptmenü.
- **29 Erfolge** gibt es, z. B. für 50/70/90/110 WPM, fehlerfreie Tests,
  7 Tage am Stück, 150 Wörter im Unendlich-Modus oder alle 40 Geschichten.

```
     Nov     Dez       Jan     Feb     Mär       Apr     Mai     Jun       Jul
 Mo  ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■
     ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■
 Mi  ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■
     ...
     Weniger ■ ■ ■ ■ ■ Mehr

 183 aktive Tage  ·  16 h 19 min Übung  ·  835 Tests
 Aktuelle Serie 4  ·  Längste Serie 11  ·  Tagesziel 15 min
```

## Einstellungen

- Sprache der Texte: Deutsch oder Englisch
- Wortlänge: kurz, gemischt oder lang
- Satzzeichen und Zahlen in Zeit-, Wörter- und freien Tests
- nur Kleinbuchstaben
- Umlaute & ß tippen oder durch ae/oe/ue/ss ersetzen (praktisch ohne
  deutsche Tastatur)
- Fehlermodus: weitertippen erlaubt oder Fehler müssen korrigiert werden
- Live-WPM, Cursorform, sichtbare Zeilen, Textbreite und Ton bei Fehlern
- Hintergrund, Farbmodus (256 Farben, True Color, 16 Farben) und bewegte Farben
- Tastatur beim Tippen an oder aus
- Tagesziel von 5 bis 60 Minuten
- Statistiken zurücksetzen

## Wo werden die Daten gespeichert?

Alles liegt in einer einzigen Datei: `~/.keyflow/daten.json`. Unter Windows
ist das `C:\Users\<Name>\.keyflow\daten.json`. Mit `--daten PFAD` oder der
Umgebungsvariable `KEYFLOW_HOME` kannst du einen anderen Ort wählen. Daten aus
älteren Versionen (`~/.tipptrainer`) werden beim ersten Start automatisch übernommen.

## Wie wird gerechnet?

- **WPM** (Wörter pro Minute) = richtig getippte Zeichen ÷ 5 ÷ Minuten.
  5 Zeichen gelten als ein Wort, so wie bei den meisten Tipptrainern.
- **Roh-WPM** zählt alle Anschläge, auch die falschen.
- **Genauigkeit** = richtige Anschläge ÷ alle Anschläge. Ein Fehler zählt also
  auch dann, wenn du ihn danach korrigierst.
- **Konstanz** zeigt, wie gleichmäßig du tippst: 100 % heißt, dein Tempo war
  jede Sekunde gleich.

## Tests

```bash
python -m unittest discover -s tests
```

## Aufbau

```
keyflow/
  app.py       Programmablauf, Modi, Speichern der Ergebnisse
  engine.py    Tipp-Logik und Berechnungen (ohne Ein-/Ausgabe)
  textgen.py   Textgenerator: Wörter, Sätze, Zahlen, Sonderzeichen, Zitate
  words.py     Wortlisten, Satzbausteine, Zitate
  stories.py   die 40 Geschichten
  stats.py     Rekorde, Serien, schwache Tasten, Erfolge
  storage.py   Einstellungen und Verlauf als JSON
  screens.py   alle Bildschirme
  ui.py        Farben, Farbverläufe, Menüs, Diagramme
  keyboard.py  Bildschirm-Tastatur und Fingerzuordnung
  terminal.py  Tastatur-Eingabe für Windows, Linux und macOS
```
