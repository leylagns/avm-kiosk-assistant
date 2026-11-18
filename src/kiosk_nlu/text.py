"""Türkçe metin normalizasyonu (küçük harf, ASCII katlama, noktalama temizliği)."""
import re

_FOLD = str.maketrans({"ı": "i", "ş": "s", "ğ": "g", "ü": "u", "ö": "o", "ç": "c", "â": "a", "î": "i", "û": "u"})


def tr_lower(s: str) -> str:
    """Türkçe'ye uygun küçük harfe çevirme (İ -> i, I -> ı)."""
    return s.replace("İ", "i").replace("I", "ı").lower()


def normalize(s: str) -> str:
    """Küçük harf + ASCII katlama + noktalama temizliği.

    "Moda Sokağı'nda" -> "moda sokaginda"; "1. kat" -> "1 kat".
    """
    s = re.sub(r"['’]", "", tr_lower(s)).translate(_FOLD)  # kesme işareti: bitişik yaz
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()
