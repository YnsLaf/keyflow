"""40 kurze Geschichten zum Abtippen – je 10 einfache, mittlere, schwere und extreme.

Einfach:  kurze Sätze, bekannte Wörter.
Mittel:   längere Sätze, Kommas, wörtliche Rede.
Schwer:   verschachtelte Sätze, Zahlen, Semikolons, Anführungszeichen.
Extrem:   lange Texte voller Zahlen, Einheiten, Klammern, Sonderzeichen und Fachwörter.
"""

LEVELS = ("easy", "medium", "hard", "extreme")
LEVEL_LABELS = {"easy": "einfach", "medium": "mittel", "hard": "schwer", "extreme": "extrem"}

STORIES = {
    "easy": (
        ("Der kleine Hund",
         "Max ist ein kleiner Hund. Er wohnt mit Lena in einem Haus am Wald. Jeden Morgen "
         "gehen die beiden in den Park. Max rennt über die Wiese und sucht Stöcke. Lena lacht "
         "und wirft den Ball. Am Abend ist Max sehr müde. Er schläft in seinem Korb und träumt "
         "vom nächsten Tag."),
        ("Der rote Apfel",
         "Im Garten steht ein alter Baum. An einem Ast hängt ein roter Apfel. Ein Vogel sieht "
         "ihn und will ihn haben. Auch eine Raupe will den Apfel. Da kommt der Wind, und der "
         "Apfel fällt ins Gras. Ein Junge findet ihn und teilt ihn mit seiner Schwester. Der "
         "Vogel und die Raupe bekommen die Reste."),
        ("Der erste Schnee",
         "Heute Nacht hat es geschneit. Als Tom aus dem Fenster schaut, ist alles weiß. Er zieht "
         "schnell seine Jacke an und läuft nach draußen. Der Schnee ist kalt und weich. Tom baut "
         "einen Schneemann mit einer Nase aus einer Karotte. Seine Mutter bringt ihm einen warmen "
         "Tee. Es ist der schönste Tag im Winter."),
        ("Die verlorene Katze",
         "Mia sucht ihre Katze. Sie ruft laut ihren Namen, aber die Katze kommt nicht. Mia schaut "
         "unter dem Bett und hinter dem Sofa. Dann sucht sie im Keller und im Garten. Am Ende hört "
         "sie ein leises Miauen. Die Katze sitzt im Wäschekorb und schläft auf den warmen "
         "Handtüchern."),
        ("Ein Tag am Meer",
         "Die Sonne scheint, und die Familie fährt ans Meer. Papa trägt die Tasche und Mama den "
         "Schirm. Die Kinder rennen sofort ins Wasser. Die Wellen sind klein, und das Wasser ist "
         "klar. Später bauen sie eine große Burg aus Sand. Am Abend essen sie Eis und schauen, wie "
         "die Sonne im Meer versinkt."),
        ("Der neue Freund",
         "Ben ist neu in der Klasse. Er kennt noch niemanden und sitzt allein. In der Pause steht "
         "er am Rand und schaut zu. Da kommt Emma zu ihm und fragt, ob er mitspielen will. Ben "
         "nickt und lächelt. Sie spielen Fangen, bis die Glocke läutet. Nach der Schule gehen sie "
         "zusammen nach Hause."),
        ("Das Brot vom Bäcker",
         "Jeden Morgen steht der Bäcker früh auf. Es ist noch dunkel, wenn er den Ofen anmacht. Er "
         "knetet den Teig mit seinen großen Händen. Bald riecht die ganze Straße nach frischem "
         "Brot. Die ersten Kunden warten schon vor der Tür. Der Bäcker ist müde, aber er ist auch "
         "glücklich."),
        ("Der kleine Stern",
         "Am Himmel wohnte ein kleiner Stern. Er war nicht so hell wie die anderen und oft "
         "traurig. Eines Nachts sah ein Kind aus dem Fenster. Es suchte lange und fand genau diesen "
         "kleinen Stern. Das Kind winkte ihm zu und sagte gute Nacht. Seitdem leuchtet der kleine "
         "Stern jede Nacht ein bisschen heller."),
        ("Regen im Sommer",
         "Es ist heiß, und alle warten auf Regen. Die Blumen im Garten lassen die Köpfe hängen. Am "
         "Nachmittag ziehen graue Wolken auf. Dann fallen die ersten Tropfen auf das Dach. Die "
         "Kinder laufen barfuß in die Pfützen und lachen. Nach dem Regen riecht die Luft frisch, "
         "und die Blumen stehen wieder gerade."),
        ("Oma kocht Suppe",
         "Am Sonntag besucht Paul seine Oma. Sie wohnt in einem kleinen Haus mit einem großen "
         "Garten. Zusammen holen sie Gemüse aus dem Beet. Paul wäscht die Karotten, und Oma "
         "schneidet die Zwiebeln. Die Suppe kocht lange auf dem Herd. Beim Essen erzählt Oma "
         "Geschichten aus ihrer Kindheit."),
    ),
    "medium": (
        ("Der Schlüssel im Schnee",
         "Als Jonas am Freitagabend nach Hause kam, merkte er, dass sein Schlüssel fehlte. Er "
         "durchsuchte jede Tasche seiner Jacke, doch er fand nur ein altes Kaugummipapier. Draußen "
         "schneite es, und die Straßenlaternen warfen gelbes Licht auf den Gehweg. Langsam ging er "
         "den Weg zurück, den er gekommen war. Vor der Bäckerei blieb er stehen, denn im Schnee "
         "glänzte etwas. \"Da bist du ja\", murmelte er erleichtert und steckte den Schlüssel tief "
         "in die Hosentasche."),
        ("Das blaue Fahrrad",
         "Lisa hatte monatelang gespart, um sich ein gebrauchtes Fahrrad zu kaufen. Es war blau, "
         "ein wenig verrostet und quietschte bei jeder Umdrehung. Ihr Nachbar, ein alter "
         "Mechaniker, sah es und schüttelte lachend den Kopf. \"Gib mir einen Nachmittag\", sagte "
         "er. Gemeinsam ölten sie die Kette, wechselten die Bremsen und pumpten die Reifen auf. Am "
         "Abend fuhr Lisa die erste Runde um den Block, und das Rad schnurrte leise wie eine "
         "zufriedene Katze."),
        ("Die Bibliothek",
         "In der alten Stadtbibliothek gab es einen Raum, den kaum jemand betrat. Die Regale "
         "reichten bis zur Decke, und es roch nach Staub und Papier. Clara entdeckte ihn an einem "
         "verregneten Dienstag, als sie vor dem Gewitter Schutz suchte. Zwischen zwei dicken "
         "Atlanten fand sie ein dünnes Heft mit handgeschriebenen Rezepten. Auf der letzten Seite "
         "stand: \"Für den, der es findet.\" Clara lächelte und nahm das Heft mit nach Hause."),
        ("Der Zug nach Norden",
         "Der Zug hatte bereits zwanzig Minuten Verspätung, als er endlich den Bahnhof verließ. "
         "Moritz saß am Fenster und beobachtete, wie die Stadt langsam kleiner wurde. Felder, "
         "Wälder und kleine Dörfer zogen an ihm vorbei. Gegenüber saß eine ältere Dame, die "
         "Kreuzworträtsel löste. \"Wissen Sie ein Wort für Sehnsucht mit sieben Buchstaben?\", "
         "fragte sie plötzlich. Moritz dachte kurz nach und sagte: \"Fernweh.\" Die Dame nickte "
         "zufrieden und schrieb es ein."),
        ("Die Nachtwache",
         "Im Leuchtturm am Ende der Insel brannte jede Nacht ein Licht. Hanna war die jüngste "
         "Wärterin, die es dort je gegeben hatte. Sie liebte die Stille, das Rauschen der Wellen "
         "und den Geruch von Salz. In einer stürmischen Nacht fiel plötzlich der Strom aus. Ohne zu "
         "zögern, stieg Hanna die schmale Treppe hinauf und zündete die alte Öllampe an. Am Morgen "
         "erfuhr sie, dass ein Fischerboot dank ihres Lichts sicher den Hafen erreicht hatte."),
        ("Der Geburtstagskuchen",
         "Zum Geburtstag seiner Mutter wollte Leon zum ersten Mal einen Kuchen backen. Er las das "
         "Rezept dreimal, bevor er anfing. Trotzdem verwechselte er Zucker und Salz, und der Teig "
         "schmeckte furchtbar. Leon wollte schon aufgeben, doch dann fing er einfach von vorne an. "
         "Diesmal klappte alles, und der Kuchen duftete herrlich. Seine Mutter sagte später, es sei "
         "der beste Kuchen gewesen, den sie je gegessen habe."),
        ("Die Briefe auf dem Dachboden",
         "Beim Aufräumen des Dachbodens fand Sophie eine Kiste voller alter Briefe. Sie waren mit "
         "einem roten Band zusammengebunden und schon ganz vergilbt. Der oberste Brief war an ihre "
         "Großmutter adressiert, geschrieben in einem Sommer vor über sechzig Jahren. Neugierig "
         "begann Sophie zu lesen. Es war ein Liebesbrief, aber nicht von ihrem Großvater. Sophie "
         "legte den Brief vorsichtig zurück und beschloss, ihre Großmutter beim nächsten Besuch "
         "danach zu fragen."),
        ("Der Stadtlauf",
         "Seit Wochen trainierte Aylin für den Stadtlauf. Jeden Morgen um sechs Uhr lief sie durch "
         "den Park, bei Regen, Wind und Kälte. Am Tag des Rennens war sie so aufgeregt, dass sie "
         "kaum frühstücken konnte. Nach dem Startschuss rannte sie viel zu schnell los und wurde "
         "bald müde. Doch sie gab nicht auf und fand ihren eigenen Rhythmus. Sie wurde nicht Erste, "
         "aber auf den letzten Metern unterbot sie ihre eigene Bestzeit."),
        ("Der Garten auf dem Dach",
         "Mitten in der Stadt, auf dem Dach eines grauen Hochhauses, lag ein kleiner Garten. Herr "
         "Yilmaz hatte ihn vor Jahren angelegt, mit Tomaten, Kräutern und einem winzigen "
         "Apfelbaum. Die Nachbarn hielten ihn zuerst für verrückt. Doch mit der Zeit kamen immer "
         "mehr von ihnen nach oben, um zu gießen, zu ernten oder einfach die Aussicht zu genießen. "
         "Heute gehört der Garten allen im Haus, und im Sommer feiern sie dort gemeinsam ihre "
         "Feste."),
        ("Das erste Konzert",
         "Noah hatte schreckliches Lampenfieber. In wenigen Minuten sollte er zum ersten Mal vor "
         "Publikum Klavier spielen. Seine Hände waren kalt, und sein Herz klopfte laut. Als er auf "
         "die Bühne trat, sah er in der ersten Reihe seine Lehrerin, die ihm aufmunternd zunickte. "
         "Er setzte sich, atmete tief ein und begann zu spielen. Nach dem letzten Ton war es kurz "
         "ganz still, dann brach lauter Applaus aus."),
    ),
    "hard": (
        ("Die Expedition",
         "Am 14. März 1911 brach eine kleine Gruppe von Forschern zu einer Reise auf, die sie "
         "weiter in den Norden führen sollte als je zuvor. Ihr Proviant reichte, so hatten sie "
         "berechnet, für genau 63 Tage; jede Verzögerung konnte gefährlich werden. Schon in der "
         "zweiten Woche zwang sie ein Schneesturm, drei Tage lang in ihren Zelten auszuharren. "
         "\"Wir müssen umkehren\", sagte der Jüngste leise, doch der Expeditionsleiter schüttelte "
         "nur den Kopf. Stattdessen teilten sie die Rationen neu ein, verzichteten auf Umwege und "
         "marschierten fortan bei jedem Wetter. Als sie nach 58 Tagen zurückkehrten, waren sie "
         "abgemagert, erschöpft und unendlich stolz."),
        ("Das Vorstellungsgespräch",
         "Frau Berger blickte über den Rand ihrer Brille und fragte: \"Warum sollten wir "
         "ausgerechnet Sie einstellen?\" Tim hatte sich auf diese Frage vorbereitet, hatte "
         "Antworten auswendig gelernt und vor dem Spiegel geübt. Doch in diesem Moment war sein "
         "Kopf vollkommen leer. Statt einer einstudierten Rede erzählte er ehrlich, wie er im "
         "letzten Sommer 3 Wochen lang die Buchhaltung des Sportvereins gerettet hatte, nachdem der "
         "Kassenwart plötzlich ausgefallen war. Frau Berger lächelte zum ersten Mal. Zwei Tage "
         "später klingelte sein Telefon; er hatte die Stelle."),
        ("Der letzte Uhrmacher",
         "In einer engen Gasse der Altstadt lag die Werkstatt von Anton Keller, dem letzten "
         "Uhrmacher des Viertels. Seit über vierzig Jahren reparierte er Taschenuhren, Pendeluhren "
         "und Wecker, deren Besitzer längst aufgegeben hatten. Seine Werkzeuge waren winzig: "
         "Pinzetten, Schraubendreher mit 0,6 Millimetern Klingenbreite und eine Lupe, die er nie "
         "abnahm. Eines Tages brachte ihm ein Mädchen eine Uhr, die seit 1987 stillstand. \"Sie "
         "gehörte meinem Opa\", erklärte sie. Anton arbeitete eine ganze Woche daran. Als die Uhr "
         "wieder tickte, gab er sie dem Mädchen zurück, ohne einen Cent zu verlangen."),
        ("Stromausfall",
         "Um 19:42 Uhr ging in der ganzen Stadt das Licht aus. Kühlschränke verstummten, "
         "Bildschirme wurden schwarz, und für einen Moment schien die Welt den Atem anzuhalten. Im "
         "dritten Stock eines Mietshauses zündete Familie Novak Kerzen an und holte ein altes "
         "Brettspiel aus dem Schrank. Nach einer Weile klopfte es: Die Nachbarin von gegenüber "
         "stand mit einer Taschenlampe vor der Tür und fragte, ob sie mitspielen dürfe. Bald saßen "
         "elf Menschen um den Küchentisch, lachten, stritten über die Regeln und aßen den Kuchen, "
         "der sonst im warmen Kühlschrank verdorben wäre. Als der Strom um 23:10 Uhr zurückkam, war "
         "fast jeder ein bisschen enttäuscht."),
        ("Die Prüfung",
         "Die Mathematikprüfung begann pünktlich um 8:00 Uhr, und Selin starrte auf die erste "
         "Aufgabe, als wäre sie in einer fremden Sprache geschrieben: Ein Zug fährt mit 120 km/h "
         "von A nach B; ein zweiter startet 30 Minuten später mit 150 km/h. Wann holt er den "
         "ersten ein? Selin schloss die Augen, zählte langsam bis zehn und erinnerte sich an den "
         "Rat ihres Bruders: \"Zeichne es einfach auf.\" Sie malte zwei Linien, beschriftete sie, "
         "und plötzlich ergab alles einen Sinn. Nach zwei Stunden gab sie als eine der Letzten ab, "
         "müde, aber mit dem sicheren Gefühl, bestanden zu haben."),
        ("Das Geheimnis des Kapitäns",
         "Kapitän Jansen sprach nie über die Nacht im Oktober 1976, in der sein Schiff beinahe "
         "gesunken wäre. Die Mannschaft kannte nur Gerüchte: von einer Welle, höher als ein Haus, "
         "von einem gebrochenen Mast und von einem Funkspruch, der nie beantwortet wurde. Erst an "
         "seinem 80. Geburtstag, als die ganze Familie am Tisch saß, räusperte er sich und begann "
         "zu erzählen. Er sprach leise und langsam, manchmal machte er lange Pausen. Am Ende sagte "
         "er: \"Angst hatte ich nicht vor dem Meer, sondern davor, euch nie wiederzusehen.\" "
         "Niemand am Tisch sagte ein Wort; nur die Wanduhr tickte weiter."),
        ("Die Reste-App",
         "Drei Studierende hatten eine Idee, die sie für genial hielten: eine App, die Reste aus "
         "dem Kühlschrank in Rezepte verwandelt. Sie programmierten nächtelang, tranken literweise "
         "Kaffee und stritten über Farben, Schriftarten und den richtigen Namen. Nach 4 Monaten war "
         "die erste Version fertig. Am Starttag luden genau 17 Menschen die App herunter, und 12 "
         "davon waren Verwandte. Enttäuscht wollten sie das Projekt schon beenden, als eine "
         "bekannte Köchin zufällig darüber berichtete. Innerhalb einer Woche stiegen die Downloads "
         "auf über 40.000; die Server brachen zweimal zusammen, doch diesmal lachten alle darüber."),
        ("Der Fund im Moor",
         "Als die Bauarbeiter im Frühjahr 2019 den Boden für eine neue Straße aushoben, stießen "
         "sie in 2,5 Metern Tiefe auf etwas Hartes. Zuerst hielten sie es für einen Stein, doch "
         "dann erkannten sie die Form eines hölzernen Rades. Die Arbeiten wurden sofort gestoppt, "
         "und ein Team von Archäologen reiste an. Wochenlang legten sie mit Pinseln und kleinen "
         "Spachteln Stück für Stück frei. Das Ergebnis war erstaunlich: Es handelte sich um einen "
         "Wagen, der vermutlich über 3.000 Jahre alt war. \"So etwas findet man einmal im Leben\", "
         "sagte die Grabungsleiterin, und ihre Stimme zitterte dabei ein wenig."),
        ("Der Umzug",
         "Nach zwölf Jahren in derselben Wohnung packte Familie Hoffmann ihre Sachen in 86 "
         "Kartons. Jeder Karton wurde beschriftet: \"Küche - zerbrechlich\", \"Bücher - schwer!\" "
         "oder einfach \"Verschiedenes\", was später niemand mehr verstand. Am Umzugstag regnete es "
         "in Strömen, der Lastwagen kam zwei Stunden zu spät, und im neuen Haus funktionierte die "
         "Heizung nicht. Trotzdem saßen am Abend alle auf dem Boden des leeren Wohnzimmers, aßen "
         "Pizza aus dem Karton und schmiedeten Pläne. \"Irgendwie fühlt es sich schon wie zu Hause "
         "an\", sagte die kleine Marie, bevor sie auf einem Stapel Decken einschlief."),
        ("Das Schachturnier",
         "Im Finale des Jugendturniers saß die elfjährige Paula einem Gegner gegenüber, der fast "
         "doppelt so alt war wie sie. Nach 34 Zügen stand sie schlecht: Ihr fehlte ein Turm, und "
         "ihr König war eingeengt. Die Zuschauer flüsterten bereits, das Spiel sei entschieden. "
         "Paula aber blieb ruhig, rechnete Variante um Variante durch und entdeckte schließlich eine "
         "versteckte Möglichkeit; sie opferte ihre Dame. Ihr Gegner nahm das Opfer an, ohne lange "
         "nachzudenken, und drei Züge später war er matt. Der Saal war einen Moment lang still, "
         "dann applaudierten alle, sogar der Verlierer."),
    ),
    "extreme": (
        ("Das Protokoll von Station 7",
         "Protokoll, Forschungsstation 7 (Antarktis), Eintrag Nr. 214 - 03.08., 06:15 Uhr "
         "Ortszeit: Außentemperatur -47,3 °C; Windgeschwindigkeit 92 km/h aus Südost. Die "
         "Funkverbindung zur Basis ist seit 38 Stunden unterbrochen; unsere Notstromaggregate "
         "laufen mit 64 % Leistung. Dr. Okonkwo hat heute Nacht die Eisbohrkerne aus 1.200 m Tiefe "
         "katalogisiert (Proben A-17 bis A-43) und dabei eine merkwürdige Anomalie festgestellt: "
         "Die Schichten zwischen 812 m und 815 m enthalten Pollen, die dort - nach allem, was wir "
         "wissen - nicht sein dürften. \"Entweder ist die Messung falsch\", sagte sie, \"oder "
         "unsere Lehrbücher.\" Wir haben die Proben versiegelt, doppelt beschriftet und im "
         "Kühlraum (Fach 3/B) eingelagert. Vorräte: Konserven für ca. 41 Tage, Treibstoff für 29 "
         "Tage bei sparsamem Verbrauch. Stimmung im Team: angespannt, aber konzentriert. Nächster "
         "Kontrollgang um 12:00 Uhr; sollte die Verbindung bis dahin nicht stehen, aktivieren wir "
         "gemäß Notfallplan (§ 4, Abs. 2) das Satellitenleuchtfeuer."),
        ("Neunzig Sekunden Panik",
         "Am Morgen des 17. Mai, um exakt 09:31:04 Uhr, fiel der Kurs der Helix & Partner AG "
         "innerhalb von 90 Sekunden um 37,8 %. Auf den Handelsbildschirmen blinkten rote Zahlen: "
         "-12,40 €, -18,95 €, schließlich -23,10 € pro Aktie. Im Großraumbüro der Investmentbank "
         "herrschte ein ohrenbetäubendes Durcheinander aus Telefonklingeln, Tastaturgeklapper und "
         "Rufen wie \"Verkaufen! Sofort!\" oder \"Wer hat die Stop-Loss-Order gesetzt?!\" Nur die "
         "Analystin Mara Lindqvist blieb sitzen, öffnete die Quartalszahlen (Umsatz Q1: 4,2 Mrd. €; "
         "EBIT-Marge: 11,3 %) und begann zu rechnen. Nach 7 Minuten war sie sich sicher: Der "
         "Absturz beruhte auf einer fehlerhaften Meldung - einem Tippfehler in einer automatischen "
         "Nachricht, die \"Umsatzrückgang\" statt \"Umsatzrückstellung\" enthielt. Sie kaufte, "
         "während alle anderen verkauften. Um 15:45 Uhr stand die Aktie wieder bei 98,6 % ihres "
         "Ausgangswertes, und Maras Abteilung erlebte den profitabelsten Tag des Jahres."),
        ("Die Festrede",
         "Sehr geehrte Damen und Herren, liebe Bürgerinnen und Bürger, verehrte Ehrengäste! Als "
         "unsere Gemeinde im Jahr 1348 zum ersten Mal urkundlich erwähnt wurde, zählte sie kaum 200 "
         "Einwohner; heute sind es 14.736 - Tendenz steigend. Diese Entwicklung ist keineswegs "
         "selbstverständlich. Sie verdankt sich der unermüdlichen Beharrlichkeit zahlloser "
         "Generationen, die Hochwasser, Missernten, Kriege und wirtschaftliche Umbrüche überstanden "
         "haben. (Zwischenruf: \"Und dem Bier!\" - Gelächter.) Ja, auch dem Bier, das seit nunmehr "
         "412 Jahren in unserer Brauerei hergestellt wird. Doch Tradition allein genügt nicht: Die "
         "Sanierung des Rathauses (Gesamtkosten: 3,7 Mio. €), der Ausbau des Glasfasernetzes auf "
         "98 % aller Haushalte und die Umgestaltung des Marktplatzes verlangen Mut, Weitsicht und - "
         "ich sage es offen - Kompromissbereitschaft. Lassen Sie uns daher gemeinsam, "
         "parteiübergreifend und generationenverbindend, an einer Zukunft arbeiten, auf die unsere "
         "Nachfahren ebenso stolz zurückblicken können wie wir heute. Vielen Dank!"),
        ("Ein einziges Gleichheitszeichen",
         "Es war Freitag, 23:47 Uhr, als Jana den Fehler endlich fand. Seit drei Tagen stürzte der "
         "Server im Abstand von exakt 4.096 Sekunden ab, und niemand im Team konnte erklären, "
         "warum. Die Log-Dateien (insgesamt 2,3 GB!) enthielten nur kryptische Einträge wie "
         "\"ERR_0x7F3A: buffer overflow @ net/socket.c:218\". Jana öffnete die Datei, scrollte zu "
         "Zeile 218 und starrte auf die Bedingung: if (count <= MAX_SIZE) { buffer[count] = data; } "
         "- da war es! Das Kleiner-gleich-Zeichen hätte ein einfaches Kleiner-Zeichen sein müssen; "
         "so schrieb das Programm genau ein Element über das Ende des Speichers hinaus. Ein einziges "
         "\"=\" hatte das gesamte System lahmgelegt, 17 Kunden verärgert und ihr Wochenende "
         "ruiniert. Sie korrigierte die Zeile, startete die Tests (412/412 bestanden, 100 %) und "
         "schrieb in die Commit-Nachricht: \"fix: off-by-one in socket buffer (#1337)\". Dann "
         "klappte sie den Laptop zu und schwor sich, am Montag als Erstes einen Kuchen für das Team "
         "zu kaufen."),
        ("Die Zeitmaschine",
         "Professor Dr. Ignaz Wendelin-Brückner (73) behauptete seit Jahrzehnten, die Zeitreise sei "
         "\"kein physikalisches, sondern ein rein ingenieurtechnisches Problem\". Seine Kollegen "
         "belächelten ihn; die Universität strich ihm 2009 sämtliche Mittel. Unbeirrt baute er in "
         "seiner Garage weiter - aus Kupferspulen, einem ausrangierten Teilchenzähler, 1.428 Metern "
         "Glasfaserkabel und, wie er betonte, \"einer gehörigen Portion Trotz\". Am 29. Februar um "
         "04:00 Uhr (ein Datum, das er aus Symmetriegründen gewählt hatte) setzte er sich in die "
         "Kapsel, stellte die Anzeige auf \"-00:05:00\" und drückte den roten Knopf. Es knallte, es "
         "roch nach verbranntem Gummi, und sämtliche Sicherungen im Viertel flogen heraus. Als er "
         "benommen aus der Kapsel kletterte, zeigte seine Armbanduhr 03:55 Uhr. War er fünf Minuten "
         "in die Vergangenheit gereist - oder war die Uhr beim Kurzschluss stehen geblieben? Der "
         "Professor notierte beide Hypothesen gewissenhaft in sein Laborbuch (Seite 347) und kochte "
         "sich erst einmal einen Kaffee."),
        ("Saal 114",
         "Saal 114 des Landgerichts war bis auf den letzten Platz gefüllt, als Staatsanwältin Dr. "
         "Henrike Albers-Zöllner am 12. November um 10:17 Uhr ihr Plädoyer begann. \"Hohes Gericht, "
         "meine Damen und Herren Schöffen\", sagte sie, \"der Angeklagte hat - das hat die "
         "Beweisaufnahme zweifelsfrei ergeben - zwischen Januar 2021 und März 2023 insgesamt 1.284 "
         "gefälschte Rechnungen ausgestellt und dadurch einen Schaden von 2.739.518,40 € "
         "verursacht.\" Sie legte eine Pause ein, blätterte in ihren Unterlagen und fuhr fort: "
         "\"Die Verteidigung behauptet, es habe sich um bedauerliche Buchungsfehler gehandelt. Doch "
         "wie erklärt sich dann, dass sämtliche Beträge auf ein Konto im Ausland (Endziffern "
         "...4471) überwiesen wurden?\" Ein Raunen ging durch den Saal. Der Angeklagte, ein "
         "unscheinbarer Mann im grauen Jackett, flüsterte seinem Anwalt etwas zu; dieser schüttelte "
         "kaum merklich den Kopf. Gemäß § 263 Abs. 3 StGB beantragte die Staatsanwaltschaft "
         "schließlich eine Freiheitsstrafe von 4 Jahren und 6 Monaten. Das Urteil wurde für den "
         "19. November, 14:00 Uhr, angekündigt."),
        ("T minus 10",
         "\"T minus 00:00:10\" - die Stimme aus dem Kontrollzentrum klang ruhig, fast gelangweilt. "
         "Kommandantin Aiko Tanaka-Brenner überprüfte ein letztes Mal die Anzeigen: Treibstoffdruck "
         "312 bar, Kabinentemperatur 21,4 °C, Sauerstoffsättigung 99 %. Neben ihr murmelte "
         "Bordingenieur Pjotr Wassiljew die Checkliste herunter, als wäre es ein Gebet. Bei T minus "
         "3 zündeten die Triebwerke; ein Beben erfasste das gesamte Raumschiff, und die "
         "Beschleunigung presste sie mit dem 3,8-fachen ihres Körpergewichts in die Sitze. Nach 8 "
         "Minuten und 42 Sekunden verstummten die Triebwerke, und Stille breitete sich aus. Ein "
         "Kugelschreiber schwebte langsam an Aikos Gesicht vorbei. \"Willkommen in der "
         "Schwerelosigkeit\", sagte sie und grinste. Vor ihnen lagen 384.400 km bis zum Mond, drei "
         "Tage Flug und eine Landung in einem Krater, den bisher kein Mensch betreten hatte. Ins "
         "Logbuch schrieb sie: \"Start nominal. Crew wohlauf. Kaffee leider verschüttet (Beutel "
         "Nr. 4/12).\""),
        ("Das Testament",
         "Notar Ferdinand Quast räusperte sich, rückte seine Brille zurecht und entfaltete das "
         "Dokument mit spürbarer Feierlichkeit. \"Ich, Walburga Theodora von Eschenbach-Liebenau, "
         "geboren am 02.04.1931, verfüge hiermit im Vollbesitz meiner geistigen Kräfte Folgendes: "
         "Erstens: Mein Anwesen (Flurstück 88/3, Gemarkung Unterwiesenbach) samt Inventar geht zu "
         "gleichen Teilen an meine Neffen Konstantin und Leopold - unter der Bedingung, dass sie "
         "sich nicht mehr streiten. Zweitens: Meine Briefmarkensammlung (geschätzter Wert: ca. "
         "48.000 €) erhält meine Haushälterin, Frau Kowalczyk, die mir 27 Jahre lang treu gedient "
         "hat. Drittens: Meinem Kater Bartholomäus steht eine lebenslange Rente von 350 € pro Monat "
         "zu; über die Verwendung wacht der Tierschutzverein.\" Im Raum war es totenstill. Dann "
         "begann Leopold schallend zu lachen, Konstantin verdrehte die Augen, und der Kater, der auf "
         "dem Fensterbrett lag, gähnte demonstrativ. Die Testamentseröffnung dauerte insgesamt 43 "
         "Minuten; der Streit darüber, wer den Kater versorgen dürfe, allerdings drei Wochen."),
        ("Die Generalprobe",
         "Die Generalprobe der 9. Sinfonie war eine Katastrophe: Die zweiten Violinen setzten in "
         "Takt 137 zu früh ein, das Fagott klang, als hätte es Schnupfen, und der Paukist hatte "
         "seine Noten (Satz IV, Seiten 12-19) im Taxi liegen lassen. Dirigent Maximilian "
         "Oberhäuser-Castellani klopfte mit dem Taktstock so heftig auf das Pult, dass dieser "
         "zerbrach. \"Meine Damen und Herren\", rief er, \"in 26 Stunden sitzen 2.400 zahlende "
         "Zuschauer in diesem Saal - und wir klingen wie eine Blaskapelle nach dem dritten "
         "Festzelt!\" Die Konzertmeisterin, Dr. Ilse Brandauer, erhob sich ruhig: \"Maestro, wir "
         "sind müde; wir proben seit 09:00 Uhr ohne nennenswerte Pause.\" Eine lange Stille folgte. "
         "Dann legte der Dirigent die Reste seines Taktstocks beiseite, atmete hörbar aus und "
         "ordnete eine Pause von 45 Minuten an - samt Kaffee, Brezeln & Streuselkuchen auf Kosten "
         "des Hauses. Am nächsten Abend gab es 11 Minuten stehende Ovationen."),
        ("Die Schatzkarte",
         "Die Karte war auf Pergament gezeichnet, an den Rändern verkohlt und mit einer Handschrift "
         "versehen, die sich nur mit einer Lupe entziffern ließ: \"Vom alten Wegkreuz 340 Schritte "
         "gen Nordnordost; dort, wo die dreistämmige Buche steht, 7 Ellen tief - doch hüte dich vor "
         "dem Wasser!\" Lukas und seine Cousine Ida (beide 14) fanden sie im Sommer 2024 in einem "
         "Hohlraum hinter der Wandvertäfelung ihres Großvaters. Mit Kompass, Maßband, zwei Spaten "
         "und einem Rucksack voller Butterbrote machten sie sich auf den Weg. Das Wegkreuz "
         "existierte tatsächlich; die Buche ebenfalls, wenngleich nur noch 2 ihrer 3 Stämme "
         "standen. Nach viereinhalb Stunden Graben (und 1 gebrochenen Spatenstiel) stießen sie auf "
         "eine eiserne Kiste. Darin lagen weder Gold noch Edelsteine, sondern 23 vergilbte Briefe, "
         "ein Taschenmesser mit Hirschhorngriff und ein Zettel: \"Wer das hier findet, hat Geduld "
         "bewiesen - und das ist wertvoller als jeder Schatz.\" Ida lachte; Lukas dagegen wollte "
         "unbedingt herausfinden, was es mit der Warnung vor dem Wasser auf sich hatte."),
    ),
}


def story_id(level, index):
    return "%s-%d" % (level, index + 1)
