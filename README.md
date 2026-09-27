# Tipptrainer

Ein Tipptrainer fürs Terminal, geschrieben in Python mit
[colorama](https://pypi.org/project/colorama/). Er läuft unter Windows, Linux
und macOS.

```
T I P P T R A I N E R                          Serie 4 Tage  ·  Bestwert 85 WPM
Heute 6,5/15 min ████░░░░░░░░          14 Tage ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■
────────────────────────────────────────────────────────────────────────
▶ Zeit-Test               ◀ 30 s ▶
  Wörter-Test               25 Wörter
  Freier Modus              Wörter
  Sätze                     3 Sätze
  Zahlen                    25 Zahlen
  Sonderzeichen             25 Gruppen
  Gemischt (Profi)          50 Teile
  Zitate & Sprichwörter     zufällig
  Schwächen-Training        25 Wörter
  Eigener Text              2 gespeichert
  ············
  Statistik & Rekorde
  Aktivität
  Erfolge                   8/24
  Einstellungen
  Beenden
```

## Starten

Du brauchst Python 3.8 oder neuer.

```bash
pip install -r requirements.txt
python start.py
```

Du kannst ihn auch als Befehl installieren:

```bash
pip install .
tipptrainer
```

Das Terminalfenster sollte mindestens 80 × 24 Zeichen groß sein. Unter Windows
funktioniert am besten das *Windows Terminal*.

## Modi

| Modus | Was passiert |
|---|---|
| **Zeit-Test** | Du tippst so viele Wörter wie möglich in 15, 30, 60 oder 120 Sekunden. |
| **Wörter-Test** | Du tippst 10, 25, 50 oder 100 Wörter so schnell wie möglich. |
| **Freier Modus** | Kein Limit, der Text geht immer weiter. Esc beendet den Test und speichert ihn. Als Text gibt es Wörter, Sätze, Zahlen, Sonderzeichen oder alles gemischt. |
| **Sätze** | Automatisch erzeugte, grammatisch richtige Sätze auf Deutsch oder Englisch. |
| **Zahlen** | Preise, Uhrzeiten, Datumsangaben, Rechnungen, Einheiten und Telefonnummern. |
| **Sonderzeichen** | Klammern, Operatoren, Pfade, E-Mail-Adressen und Code-Schnipsel. |
| **Gemischt (Profi)** | Wörter, Großbuchstaben, Satzzeichen, Zahlen und Sonderzeichen durcheinander. |
| **Zitate & Sprichwörter** | Sprichwörter und berühmte Textstellen, z. B. von Goethe, Schiller, Kafka oder den Brüdern Grimm. |
| **Schwächen-Training** | Erzeugt Text mit genau den Tasten, bei denen du die meisten Fehler machst. |
| **Eigener Text** | Du fügst einen Text ein oder lädst eine `.txt`-Datei. Lange Texte werden in Abschnitten geübt, und der Trainer merkt sich, wo du stehst. |

Im Hauptmenü wählst du Länge oder Variante direkt mit **← →** aus.

## Tasten beim Tippen

| Taste | Wirkung |
|---|---|
| Rücktaste | letztes Zeichen löschen |
| Strg + Rücktaste (macOS: Option + Rücktaste) | ganzes Wort löschen |
| Tab | Test mit neuem Text neu starten |
| Esc | zurück ins Menü (im freien Modus: beenden und speichern) |

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
- **24 Erfolge** gibt es, z. B. für 50/70/90/110 WPM, fehlerfreie Tests,
  7 Tage am Stück oder 10 Minuten im freien Modus.

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
- Farbstufe des Kalenders: 256 Farben, True Color oder 16 Farben
- Tagesziel von 5 bis 60 Minuten
- Statistiken zurücksetzen

## Wo werden die Daten gespeichert?

Alles liegt in einer einzigen Datei: `~/.tipptrainer/daten.json`. Unter Windows
ist das `C:\Users\<Name>\.tipptrainer\daten.json`. Mit `--daten PFAD` oder der
Umgebungsvariable `TIPPTRAINER_HOME` kannst du einen anderen Ort wählen.

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
tipptrainer/
  app.py       Programmablauf, Modi, Speichern der Ergebnisse
  engine.py    Tipp-Logik und Berechnungen (ohne Ein-/Ausgabe)
  textgen.py   Textgenerator: Wörter, Sätze, Zahlen, Sonderzeichen, Zitate
  words.py     Wortlisten, Satzbausteine, Zitate
  stats.py     Rekorde, Serien, schwache Tasten, Erfolge
  storage.py   Einstellungen und Verlauf als JSON
  screens.py   alle Bildschirme
  ui.py        Farben, Menüs, Diagramme, Kalenderfarben
  terminal.py  Tastatur-Eingabe für Windows, Linux und macOS
```
