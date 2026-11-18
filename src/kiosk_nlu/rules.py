"""E0: kural tabanlı alt sınır (öğrenme yok): sözlük eşleştirme + anahtar kelime kuralları.

Amaç: "makine öğrenmesi gerçekten bir şey katıyor mu?" sorusuna cevap veren en basit referans.
Sıra: olanak -> mağaza (+saat ipucu) -> AVM saatleri -> kat -> kategori -> selamlama -> kapsam dışı.
"""
import re

from .gazetteer import FLOOR_MAP, FLOOR_RE, Gazetteer
from .text import normalize

HOURS_RE = re.compile(r"\b(acik|kapali|kapan\w*|kacta|kaca kadar|calisma|calisiyor|calisir|mesai|acilis|aciliyor|acilir|hizmet)\b")
GREET = {"merhaba", "merhabalar", "selam", "selamlar", "slm", "mrb", "gunaydin", "naber", "nasilsin", "hey", "yardim",
         "tesekkur", "tesekkurler", "tesekkurler", "eyvallah", "gorusuruz", "hoscakal", "hoscakalin", "sagol", "sagolun",
         "iyi", "kolay", "yardimci", "yapabilirsin"}
GREET_PHRASES = ("iyi gunler", "iyi aksamlar", "sag ol", "hos cakal", "kolay gelsin", "yardim eder", "ne yapabilirsin")
AVM_RE = re.compile(r"\b(avm|alisveris merkezi)\b")
FLOOR_CUE = re.compile(r"\b(neler|ne var|magaza\w*|rehber\w*|plan\w*|harita\w*|liste\w*|dukkan\w*)\b")


class RuleNLU:
    def __init__(self, gazetteer: Gazetteer | None = None):
        self.gaz = gazetteer or Gazetteer()

    def fit(self, *args, **kwargs):  # öğrenme yok; arayüz uyumu için
        return self

    def predict_intents(self, texts):
        return [self.parse(t)["intent"] for t in texts]

    def parse(self, text: str) -> dict:
        n = normalize(text)
        def res(intent, etype=None, val=None):
            return {"intent": intent, "confidence": 1.0, "entity_type": etype, "entity_value": val}

        fac = self.gaz._match(text, "facility")
        if fac:
            return res("find_facility", "facility", fac)
        store = self.gaz._match(text, "store")
        hours = bool(HOURS_RE.search(n))
        if store:
            return res("opening_hours" if hours else "find_store", "store", store)
        if hours and AVM_RE.search(n):
            return res("opening_hours")
        m = FLOOR_RE.search(n)
        if m and FLOOR_CUE.search(n):
            return res("floor_directory", "floor", FLOOR_MAP[m.group(1)])
        cat = self.gaz._match(text, "category")
        if cat:
            return res("recommend_category", "category", cat)
        if set(n.split()) & GREET or any(p in n for p in GREET_PHRASES):
            return res("greeting_help")
        return res("out_of_scope")
