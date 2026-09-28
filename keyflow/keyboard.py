"""Bildschirm-Tastatur: zeigt, welche Taste als Nächstes gedrückt werden muss."""

import sys

MAC = sys.platform == "darwin"

# Zeichen-Tasten je Reihe (klein geschrieben = Grundbelegung)
ROWS = {
    "de": ("^1234567890ß´", "qwertzuiopü+", "asdfghjklöä#", "<yxcvbnm,.-"),
    "en": ("`1234567890-=", "qwertyuiop[]\\", "asdfghjkl;'", "zxcvbnm,./"),
}

# Finger je Taste: L/R = Hand, 2 = Zeige-, 3 = Mittel-, 4 = Ring-, 5 = kleiner Finger
FINGERS = {
    "de": (
        ("L5", "L5", "L4", "L3", "L2", "L2", "R2", "R2", "R3", "R4", "R5", "R5", "R5"),
        ("L5", "L4", "L3", "L2", "L2", "R2", "R2", "R3", "R4", "R5", "R5", "R5"),
        ("L5", "L4", "L3", "L2", "L2", "R2", "R2", "R3", "R4", "R5", "R5", "R5"),
        ("L5", "L5", "L4", "L3", "L2", "L2", "R2", "R2", "R3", "R4", "R5"),
    ),
    "en": (
        ("L5", "L5", "L4", "L3", "L2", "L2", "R2", "R2", "R3", "R4", "R5", "R5", "R5"),
        ("L5", "L4", "L3", "L2", "L2", "R2", "R2", "R3", "R4", "R5", "R5", "R5", "R5"),
        ("L5", "L4", "L3", "L2", "L2", "R2", "R2", "R3", "R4", "R5", "R5"),
        ("L5", "L4", "L3", "L2", "L2", "R2", "R2", "R3", "R4", "R5"),
    ),
}

FINGER_NAMES = {
    "L5": "linker kleiner Finger", "L4": "linker Ringfinger", "L3": "linker Mittelfinger",
    "L2": "linker Zeigefinger", "R2": "rechter Zeigefinger", "R3": "rechter Mittelfinger",
    "R4": "rechter Ringfinger", "R5": "rechter kleiner Finger", "T": "Daumen",
}

# Umschalt-Zeichen -> Grundtaste
SHIFTED = {
    "de": dict(zip('°!"§$%&/()=?`*\'>;:_', "^1234567890ß´+#<,.-")),
    "en": dict(zip('~!@#$%^&*()_+{}|:"<>?', "`1234567890-=[]\\;',./")),
}

# Zeichen über AltGr (Windows/Linux) bzw. Wahltaste ⌥ (Mac): Zeichen -> (Taste, mit Umschalt?)
ALT = {
    "de": {"@": ("q", False), "€": ("e", False), "{": ("7", False), "[": ("8", False),
           "]": ("9", False), "}": ("0", False), "\\": ("ß", False), "~": ("+", False),
           "|": ("<", False)},
    "en": {},
}
ALT_MAC = {
    "de": {"@": ("l", False), "€": ("e", False), "[": ("5", False), "]": ("6", False),
           "{": ("8", False), "}": ("9", False), "|": ("7", False), "\\": ("7", True),
           "~": ("n", False)},
    "en": {},
}


def alt_map(lang):
    return (ALT_MAC if MAC else ALT)[lang]


def finger_of(key, lang):
    if key == " ":
        return "T"
    for row, fingers in zip(ROWS[lang], FINGERS[lang]):
        i = row.find(key)
        if i != -1:
            return fingers[i]
    return None


def base_key(ch, lang):
    """Die Taste (ohne Umschalt/Alt), auf der ein Zeichen liegt, oder None."""
    if ch == " ":
        return " "
    low = ch.lower() if len(ch.lower()) == 1 else ch
    for row in ROWS[lang]:
        if low in row:
            return low
    if ch in SHIFTED[lang]:
        return SHIFTED[lang][ch]
    if ch in alt_map(lang):
        return alt_map(lang)[ch][0]
    return None


def keys_for(ch, lang):
    """Welche Tasten für ein Zeichen leuchten sollen und welcher Finger sie drückt.

    Gibt (menge_der_tasten, hinweistext) zurück. Modifikatoren heißen
    "shift_l", "shift_r", "mod_l", "mod_r"."""
    if ch is None:
        return set(), ""
    if ch == " ":
        return {" "}, "Leertaste  ·  Daumen"
    key, shift, alt = None, False, False
    low = ch.lower() if len(ch.lower()) == 1 else ch
    if any(low in row for row in ROWS[lang]):
        key = low
        shift = ch != low
    elif ch in SHIFTED[lang]:
        key, shift = SHIFTED[lang][ch], True
    elif ch in alt_map(lang):
        key, shift = alt_map(lang)[ch]
        alt = True
    if key is None:
        return set(), "„%s“ gibt es auf dieser Tastatur nicht direkt" % ch
    finger = finger_of(key, lang) or "L2"
    left = finger.startswith("L")
    keys = {key}
    label = key.upper() if len(key.upper()) == 1 else key
    hint = "%s  ·  %s" % (label, FINGER_NAMES[finger])
    if shift:
        keys.add("shift_r" if left else "shift_l")
        hint += "  +  ⇧ %s" % ("rechts" if left else "links")
    if alt:
        if MAC:
            keys.add("mod_r" if left else "mod_l")
            hint += "  +  ⌥ %s" % ("rechts" if left else "links")
        else:
            keys.add("mod_r")
            hint += "  +  AltGr"
    return keys, hint


def layout(lang):
    """Tastatur als Reihen von (beschriftung, tasten-id, breite). Tasten ohne
    Beschriftung (Tab, Feststell, Enter, Rücktaste) halten nur den Versatz."""
    rows = ROWS[lang]

    def keys(row):
        return [((k.upper() if len(k.upper()) == 1 else k), k, 3) for k in row]

    mod_l, mod_r = ("⌥", "⌥") if MAC else ("Alt", "AltGr" if lang == "de" else "Alt")
    if lang == "de":
        return [
            keys(rows[0]) + [("", "back", 5)],
            [("", "tab", 5)] + keys(rows[1]) + [("", "enter", 3)],
            [("", "caps", 6)] + keys(rows[2]) + [("", "enter", 2)],
            [("⇧", "shift_l", 4)] + keys(rows[3]) + [("⇧", "shift_r", 8)],
            [("", None, 7), (mod_l, "mod_l", 5), ("", " ", 29), (mod_r, "mod_r", 5)],
        ]
    return [
        keys(rows[0]) + [("", "back", 5)],
        [("", "tab", 5)] + keys(rows[1]),
        [("", "caps", 6)] + keys(rows[2]) + [("", "enter", 6)],
        [("⇧", "shift_l", 8)] + keys(rows[3]) + [("⇧", "shift_r", 8)],
        [("", None, 7), (mod_l, "mod_l", 5), ("", " ", 29), (mod_r, "mod_r", 5)],
    ]
