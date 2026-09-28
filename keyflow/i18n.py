"""Language of the user interface (English or German).

Texts are written inline as pairs: tr("Deutsch", "English")."""

_STATE = {"ui": "en"}


def set_language(lang):
    _STATE["ui"] = "de" if lang == "de" else "en"


def language():
    return _STATE["ui"]


def tr(de, en):
    return de if _STATE["ui"] == "de" else en


def pick(pair):
    """Resolves a (de, en) pair; plain strings are returned unchanged."""
    if isinstance(pair, tuple):
        return tr(*pair)
    return pair
