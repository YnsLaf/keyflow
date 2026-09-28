"""On-screen keyboard: shows which key has to be pressed next."""

import sys

from .i18n import pick, tr

MAC = sys.platform == "darwin"

# character keys per row (lowercase = base layer)
ROWS = {
    "de": ("^1234567890ß´", "qwertzuiopü+", "asdfghjklöä#", "<yxcvbnm,.-"),
    "en": ("`1234567890-=", "qwertyuiop[]\\", "asdfghjkl;'", "zxcvbnm,./"),
}

# finger per key: L/R = hand, 2 = index, 3 = middle, 4 = ring, 5 = pinky
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
    "L5": ("linker kleiner Finger", "left pinky"), "L4": ("linker Ringfinger", "left ring finger"),
    "L3": ("linker Mittelfinger", "left middle finger"), "L2": ("linker Zeigefinger", "left index finger"),
    "R2": ("rechter Zeigefinger", "right index finger"), "R3": ("rechter Mittelfinger", "right middle finger"),
    "R4": ("rechter Ringfinger", "right ring finger"), "R5": ("rechter kleiner Finger", "right pinky"),
    "T": ("Daumen", "thumb"),
}

# shifted character -> base key
SHIFTED = {
    "de": dict(zip('°!"§$%&/()=?`*\'>;:_', "^1234567890ß´+#<,.-")),
    "en": dict(zip('~!@#$%^&*()_+{}|:"<>?', "`1234567890-=[]\\;',./")),
}

# characters via AltGr (Windows/Linux) or Option ⌥ (Mac): char -> (key, with shift?)
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
    """The key (without Shift/Alt) a character lives on, or None."""
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
    """Which keys light up for a character and which finger presses them.

    Returns (set_of_keys, hint). Modifiers are called
    "shift_l", "shift_r", "mod_l", "mod_r"."""
    if ch is None:
        return set(), ""
    if ch == " ":
        return {" "}, tr("Leertaste  ·  Daumen", "Space  ·  thumb")
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
        return set(), tr("„%s“ gibt es auf dieser Tastatur nicht direkt",
                         "\"%s\" is not on this keyboard") % ch
    finger = finger_of(key, lang) or "L2"
    left = finger.startswith("L")
    keys = {key}
    label = key.upper() if len(key.upper()) == 1 else key
    hint = "%s  ·  %s" % (label, pick(FINGER_NAMES[finger]))
    right, left_word = tr("rechts", "right"), tr("links", "left")
    if shift:
        keys.add("shift_r" if left else "shift_l")
        hint += "  +  ⇧ %s" % (right if left else left_word)
    if alt:
        if MAC:
            keys.add("mod_r" if left else "mod_l")
            hint += "  +  ⌥ %s" % (right if left else left_word)
        else:
            keys.add("mod_r")
            hint += "  +  AltGr"
    return keys, hint


PITCH = 3  # distance from key to key in characters


def _cap(key):
    return key.upper() if len(key.upper()) == 1 else key


def layout(lang):
    """Keyboard as rows of (x, label, key_id, width).

    Even grid with a slight offset per row like on a real keyboard;
    Shift left/right, below that the space bar with ⌥ or Alt/AltGr."""
    rows = ROWS[lang]
    offsets = (3, 5, 6, 4) if lang == "de" else (3, 5, 6, 7)
    out = []
    for r, (row, off) in enumerate(zip(rows, offsets)):
        cells = [(off + i * PITCH, _cap(k), k, 3) for i, k in enumerate(row)]
        if r == 3:
            cells.insert(0, (off - 4, "⇧", "shift_l", 3))
            cells.append((off + len(row) * PITCH + 1, "⇧", "shift_r", 3))
        out.append(cells)
    # space bar: from C to comma, modifiers left and right of it
    bottom = rows[3]
    x_c = offsets[3] + bottom.index("c") * PITCH
    x_comma = offsets[3] + bottom.index(",") * PITCH + PITCH
    mod_l, mod_r = ("⌥", "⌥") if MAC else ("Alt", "AltGr" if lang == "de" else "Alt")
    out.append([
        (x_c - 4, mod_l, "mod_l", 3),
        (x_c, "", " ", x_comma - x_c),
        (x_comma + 1, mod_r, "mod_r", max(3, len(mod_r))),
    ])
    return out
