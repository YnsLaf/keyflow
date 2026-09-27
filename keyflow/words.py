"""Wortlisten, Satzbausteine und Zitate für die Textgenerierung."""


def _unique(text):
    return tuple(dict.fromkeys(text.split()))


GERMAN_WORDS = _unique("""
der die das und ist nicht ein eine zu es sich mit auf für von dem den im in
auch als an wie was noch nach bei aus so nur oder aber wenn man schon dann
mehr sehr hier alle da doch um vor zum zur über unter durch gegen ohne weil
dass immer wieder jetzt heute morgen bald oft nie viel wenig gut neu alt groß
klein lang kurz schnell langsam hoch tief warm kalt hell dunkel leicht schwer
schön richtig falsch frei ganz halb erst andere eigene gleich wichtig möglich
einfach klar sicher genau fast selbst ich du er sie wir ihr mein dein unser
kein jeder dieser welche wer wo wann warum dort oben unten links rechts
vielleicht natürlich zusammen allein zuerst später danach deshalb trotzdem
sein haben werden können müssen sollen wollen dürfen machen gehen kommen sehen
sagen geben nehmen finden denken wissen stehen liegen sitzen lassen bleiben
bringen halten laufen spielen lernen arbeiten leben lesen schreiben sprechen
hören fragen antworten suchen zeigen kaufen essen trinken schlafen fahren
fliegen öffnen schließen beginnen helfen tragen ziehen legen stellen fallen
rufen singen tanzen lachen warten treffen vergessen verstehen erklären glauben
hoffen bauen kochen waschen tippen üben erzählen gewinnen verlieren wählen
träumen
Zeit Jahr Tag Mensch Hand Auge Haus Welt Leben Stadt Land Frau Mann Kind
Schule Arbeit Weg Wasser Buch Freund Familie Frage Antwort Wort Bild Name Ende
Geld Straße Baum Wald Berg Meer Himmel Sonne Mond Stern Nacht Woche Monat
Abend Zimmer Tür Fenster Tisch Stuhl Bett Küche Garten Auto Zug Fahrrad Brief
Musik Lied Spiel Sport Brot Kaffee Tee Milch Apfel Hund Katze Vogel Pferd
Blume Farbe Tastatur Computer Bildschirm Finger Taste Übung Ziel Idee Problem
Lösung Beispiel Geschichte Sprache Reise Urlaub Wetter Regen Schnee Wind Feuer
Luft Erde Stimme Herz Kopf Fuß Glück Spaß Ruhe Kraft Schlüssel Brücke Märchen
Gemüse Käse Bär Löwe Mädchen Junge Lehrer Ärztin Nachbar Hütte Flughafen
Bahnhof Fußball Größe Gefühl Kühlschrank Frühstück Überraschung Gespräch
glücklich traurig müde wach fröhlich ruhig laut leise stark schwach klug
freundlich wunderbar spannend lustig gemütlich bunt grün blau rot gelb weiß
schwarz süß sauer frisch sauber fertig bereit ehrlich höflich nützlich
gefährlich
""")

ENGLISH_WORDS = _unique("""
the be to of and a in that have it for not on with he as you do at this but
his by from they we say her she or an will my one all would there their what
so up out if about who get which go me when make can like time no just him
know take people into year your good some could them see other than then now
look only come its over think also back after use two how our work first well
way even new want because any these give day most us
life world school house water hand place point week number home family story
fact month night group word problem question money light music book friend
letter garden river mountain window table morning evening teacher student
keyboard computer screen finger practice travel summer winter weather animal
flower forest island ocean planet journey kitchen library village market
bridge picture history language answer
write read speak listen learn play run walk jump swim drive open close begin
finish help carry bring build cook clean laugh sing dance dream wait meet
forget remember understand explain believe choose wonder
happy quiet little great small large young early late strong simple bright
gentle careful quick slow warm cold clever friendly strange famous modern
ancient curious honest perfect special different important possible beautiful
wonderful difficult interesting
""")

# --- Satzbausteine Deutsch -------------------------------------------------
# Alle Subjekte stehen in der 3. Person Singular, damit die Verben passen.
DE_SUBJECTS = (
    "Der Hund", "Die Katze", "Mein Nachbar", "Unsere Lehrerin", "Das Kind",
    "Der alte Mann", "Eine junge Frau", "Der Koch", "Die Ärztin", "Mein Bruder",
    "Meine Schwester", "Der Bäcker", "Die Programmiererin", "Das ganze Team",
    "Jeder Schüler", "Ein Tourist", "Die Musikerin", "Der Pilot",
)

# (Verb, Rest) – der Rest darf eine abgetrennte Vorsilbe enthalten ("auf", "nach").
DE_VERBS = (
    ("liest", "ein spannendes Buch"),
    ("trinkt", "einen heißen Kaffee"),
    ("wartet", "geduldig auf den Bus"),
    ("schreibt", "einen langen Brief"),
    ("kocht", "eine leckere Suppe"),
    ("spielt", "Gitarre"),
    ("sucht", "den verlorenen Schlüssel"),
    ("plant", "eine große Reise"),
    ("repariert", "das alte Fahrrad"),
    ("singt", "ein fröhliches Lied"),
    ("malt", "ein buntes Bild"),
    ("denkt", "über die Zukunft nach"),
    ("räumt", "die Küche auf"),
    ("kauft", "frisches Brot"),
    ("beobachtet", "die Sterne"),
    ("erzählt", "eine lustige Geschichte"),
    ("übt", "fleißig Klavier"),
    ("tippt", "schnell auf der Tastatur"),
    ("lernt", "eine neue Sprache"),
    ("isst", "einen frischen Apfel"),
    ("ruft", "die Großmutter an"),
    ("füttert", "die hungrigen Enten"),
)

DE_PLACES = (
    "im Park", "in der Küche", "am See", "auf dem Balkon", "im Büro",
    "in der Stadt", "im Garten", "am Bahnhof", "zu Hause", "in der Bibliothek",
    "im Café",
)

DE_TIMES = (
    "Heute", "Jeden Morgen", "Am Wochenende", "Am Abend", "Nach der Arbeit",
    "Im Sommer", "Manchmal", "Um acht Uhr", "Oft", "Morgen früh",
)

DE_QUESTIONS = ("Warum", "Wann", "Wo", "Wie oft")

# --- Satzbausteine Englisch ------------------------------------------------
EN_SUBJECTS = (
    "The dog", "The cat", "My neighbor", "The teacher", "A young woman",
    "The old man", "The cook", "The doctor", "My brother", "Her sister",
    "The baker", "The programmer", "Every student", "A tourist", "The musician",
    "The pilot",
)

# (3. Person, Grundform, Rest)
EN_VERBS = (
    ("reads", "read", "an exciting book"),
    ("drinks", "drink", "a hot coffee"),
    ("waits", "wait", "patiently for the bus"),
    ("writes", "write", "a long letter"),
    ("cooks", "cook", "a delicious soup"),
    ("plays", "play", "the guitar"),
    ("looks", "look", "for the lost keys"),
    ("plans", "plan", "a long trip"),
    ("fixes", "fix", "the old bicycle"),
    ("sings", "sing", "a happy song"),
    ("paints", "paint", "a colorful picture"),
    ("thinks", "think", "about the future"),
    ("cleans", "clean", "the kitchen"),
    ("buys", "buy", "fresh bread"),
    ("watches", "watch", "the stars"),
    ("tells", "tell", "a funny story"),
    ("practices", "practice", "the piano"),
    ("types", "type", "quickly on the keyboard"),
    ("learns", "learn", "a new language"),
    ("feeds", "feed", "the hungry ducks"),
)

EN_PLACES = (
    "in the park", "in the kitchen", "by the lake", "on the balcony",
    "at the office", "in the city", "in the garden", "at the station",
    "at home", "in the library", "at the cafe",
)

EN_TIMES = (
    "Every morning", "Today", "On the weekend", "In the evening", "After work",
    "In the summer", "Sometimes", "At eight o'clock", "Tomorrow",
)

EN_QUESTIONS = ("Why does", "When does", "Where does", "How often does")

# --- Zahlen & Sonderzeichen ------------------------------------------------
UNITS = {
    "de": ("kg", "km", "m", "cm", "mm", "ml", "l", "g", "GB", "MB", "°C", "Std.", "Min."),
    "en": ("kg", "km", "mi", "lb", "oz", "ml", "GB", "MB", "ft", "in", "mph"),
}

IDENTIFIERS = (
    "name", "wert", "liste", "datei", "zahl", "text", "user", "data", "item",
    "index", "count", "max", "min", "sum", "pfad", "ziel", "start", "ende",
    "config", "value", "result", "key", "id", "total", "info", "tmp", "x", "y",
)

# --- Zitate & Sprichwörter (gemeinfrei) -------------------------------------
QUOTES = {
    "de": (
        ("Übung macht den Meister.", "Sprichwort"),
        ("Wer rastet, der rostet.", "Sprichwort"),
        ("Aller Anfang ist schwer.", "Sprichwort"),
        ("Morgenstund hat Gold im Mund.", "Sprichwort"),
        ("Steter Tropfen höhlt den Stein.", "Sprichwort"),
        ("Ohne Fleiß kein Preis.", "Sprichwort"),
        ("Gut Ding will Weile haben.", "Sprichwort"),
        ("Rom wurde auch nicht an einem Tag erbaut.", "Sprichwort"),
        ("Wo ein Wille ist, ist auch ein Weg.", "Sprichwort"),
        ("Geduld bringt Rosen.", "Sprichwort"),
        ("Was du heute kannst besorgen, das verschiebe nicht auf morgen.", "Sprichwort"),
        ("Früh übt sich, was ein Meister werden will.", "Friedrich Schiller, Wilhelm Tell"),
        ("Der kluge Mann baut vor.", "Friedrich Schiller, Wilhelm Tell"),
        ("Grau, teurer Freund, ist alle Theorie, und grün des Lebens goldner Baum.",
         "Johann Wolfgang von Goethe, Faust"),
        ("Was man schwarz auf weiß besitzt, kann man getrost nach Hause tragen.",
         "Johann Wolfgang von Goethe, Faust"),
        ("Es ist nicht genug zu wissen, man muss auch anwenden; es ist nicht genug "
         "zu wollen, man muss auch tun.", "Johann Wolfgang von Goethe"),
        ("Der Mensch spielt nur, wo er in voller Bedeutung des Worts Mensch ist, und "
         "er ist nur da ganz Mensch, wo er spielt.", "Friedrich Schiller"),
        ("Ich weiß nicht, ob es besser wird, wenn es anders wird. Aber so viel kann "
         "ich sagen: Es muss anders werden, wenn es gut werden soll.",
         "Georg Christoph Lichtenberg"),
        ("Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich "
         "in seinem Bett zu einem ungeheueren Ungeziefer verwandelt.",
         "Franz Kafka, Die Verwandlung"),
        ("In den alten Zeiten, wo das Wünschen noch geholfen hat, lebte ein König, "
         "dessen Töchter waren alle schön, aber die jüngste war so schön, dass die "
         "Sonne selber, die doch so vieles gesehen hat, sich verwunderte, sooft sie "
         "ihr ins Gesicht schien.", "Brüder Grimm, Der Froschkönig"),
        ("Es war einmal eine kleine süße Dirne, die hatte jedermann lieb, der sie nur "
         "ansah, am allerliebsten aber ihre Großmutter, die wusste gar nicht, was sie "
         "alles dem Kinde geben sollte.", "Brüder Grimm, Rotkäppchen"),
    ),
    "en": (
        ("Practice makes perfect.", "Proverb"),
        ("The quick brown fox jumps over the lazy dog.", "Pangram"),
        ("Where there is a will, there is a way.", "Proverb"),
        ("Rome was not built in a day.", "Proverb"),
        ("Actions speak louder than words.", "Proverb"),
        ("The early bird catches the worm.", "Proverb"),
        ("Well begun is half done.", "Proverb"),
        ("Knowledge is power.", "Proverb"),
        ("A journey of a thousand miles begins with a single step.", "Proverb"),
        ("There is nothing either good or bad, but thinking makes it so.",
         "William Shakespeare, Hamlet"),
        ("All the world's a stage, and all the men and women merely players.",
         "William Shakespeare, As You Like It"),
        ("Happy families are all alike; every unhappy family is unhappy in its own way.",
         "Leo Tolstoy, Anna Karenina"),
        ("It is a truth universally acknowledged, that a single man in possession of "
         "a good fortune, must be in want of a wife.",
         "Jane Austen, Pride and Prejudice"),
        ("Alice was beginning to get very tired of sitting by her sister on the bank, "
         "and of having nothing to do.", "Lewis Carroll, Alice in Wonderland"),
        ("It was the best of times, it was the worst of times, it was the age of "
         "wisdom, it was the age of foolishness, it was the epoch of belief, it was "
         "the epoch of incredulity, it was the season of Light, it was the season of "
         "Darkness, it was the spring of hope, it was the winter of despair.",
         "Charles Dickens, A Tale of Two Cities"),
        ("Call me Ishmael. Some years ago, never mind how long precisely, having "
         "little or no money in my purse, and nothing particular to interest me on "
         "shore, I thought I would sail about a little and see the watery part of "
         "the world.", "Herman Melville, Moby-Dick"),
    ),
}
