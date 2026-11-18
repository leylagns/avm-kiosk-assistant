"""Sözlük (gazetteer) tabanlı varlık çıkarımı: bulanık (fuzzy) eşleştirme ile."""
import re
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

from .text import normalize

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "avm"
FLOOR_RE = re.compile(r"\b(zemin|giris|0|1|bir|birinci|2|iki|ikinci)\s*kat")
FLOOR_MAP = {"zemin": 0, "giris": 0, "0": 0, "1": 1, "bir": 1, "birinci": 1, "2": 2, "iki": 2, "ikinci": 2}

# Hangi niyet hangi varlık tipini bekliyor?
INTENT_ENTITY = {
    "find_store": "store",
    "opening_hours": "store",
    "find_facility": "facility",
    "recommend_category": "category",
    "floor_directory": "floor",
}


class Gazetteer:
    def __init__(self, data_dir: Path = DATA_DIR, threshold: float = 0.8):
        self.threshold = threshold
        stores = pd.read_csv(data_dir / "stores.csv")
        fac = pd.read_csv(data_dir / "facility_aliases.csv")
        cat = pd.read_csv(data_dir / "category_aliases.csv")
        self.stores = stores
        self.forms = {
            "store": [(normalize(r.name), r.store_id) for r in stores.itertuples()],
            "facility": [(normalize(r.alias), r.type) for r in fac.itertuples()],
            "category": [(normalize(r.alias), r.category) for r in cat.itertuples()],
        }

    def _match(self, text: str, kind: str):
        tokens = normalize(text).split()
        best_score, best_val, best_len = 0.0, None, 0
        for form, value in self.forms[kind]:
            n_form = len(form.split())
            for n in {n_form - 1, n_form, n_form + 1}:
                if n < 1:
                    continue
                for i in range(len(tokens) - n + 1):
                    span = " ".join(tokens[i : i + n])
                    if len(form) <= 3:  # çok kısa biçimler (wc, atm) yalnızca birebir eşleşir
                        score = 1.0 if span == form else 0.0
                    else:
                        score = SequenceMatcher(None, span, form).ratio()
                    if score >= self.threshold and (score, len(form)) > (best_score, best_len):
                        best_score, best_val, best_len = score, value, len(form)
        return best_val

    def extract(self, text: str, intent: str):
        """(varlık_tipi, değer) döndürür; bulunamazsa (tip, None)."""
        kind = INTENT_ENTITY.get(intent)
        if kind is None:
            return None, None
        if kind == "floor":
            m = FLOOR_RE.search(normalize(text))
            return kind, (FLOOR_MAP[m.group(1)] if m else None)
        return kind, self._match(text, kind)
