"""Sentetik Türkçe kiosk sorgu veri seti üretici (tekrarlanabilir: sabit seed).

Çıktılar (data/processed/): train.csv, val.csv, test.csv, test_hard.csv
- train/val/test : aynı şablon ailesi, hafif gürültü (dağılım içi)
- test_hard      : eğitimde GÖRÜLMEYEN şablonlar + örtük ifadeler + ağır gürültü

Çalıştırma:  PYTHONPATH=src python -m kiosk_nlu.generate_dataset
"""
import random
from pathlib import Path

import pandas as pd

from .text import tr_lower

ROOT = Path(__file__).resolve().parents[2]
AVM = ROOT / "data" / "avm"
OUT = ROOT / "data" / "processed"
SEED = 42

INTENTS = ["find_store", "find_facility", "recommend_category", "opening_hours",
           "floor_directory", "greeting_help", "out_of_scope"]

FLOORS = [("zemin", 0), ("1.", 1), ("2.", 2), ("birinci", 1), ("ikinci", 2), ("giriş", 0)]

# ---------------- Eğitim şablonları ----------------
TRAIN = {
    "find_store": ["{s} nerede", "{s} nerde", "{s} hangi katta", "{s} nasıl gidilir", "{s} yol tarifi",
                   "{s} mağazasına nasıl giderim", "{s} mağazası nerede", "{s} yerini söyler misin",
                   "{s} bulmak istiyorum", "{s} konumu", "{s} mağazasına gitmek istiyorum", "{s} neresi"],
    "find_facility": ["{f} nerede", "en yakın {f} nerede", "{f} nerde", "en yakın {f} nereye", "{f} var mı",
                      "{f} arıyorum", "{f} hangi katta", "{f} yolunu tarif eder misin", "{f} nasıl bulurum"],
    "recommend_category": ["{c} önerir misin", "{c} var mı burada", "{c} arıyorum", "{c} tavsiye eder misin",
                           "bana {c} göster", "burada {c} bulabilir miyim", "{c} için nereye gitmeliyim",
                           "{c} için hangi mağazalar var", "{c} için nereye gidebilirim"],
    "opening_hours": ["{s} kaçta açılıyor", "{s} kaça kadar açık", "{s} saat kaçta kapanıyor", "{s} çalışma saatleri",
                      "{s} şu an açık mı", "{s} açık mı", "{s} kaça kadar çalışıyor",
                      "avm kaçta kapanıyor", "avm kaça kadar açık", "alışveriş merkezi çalışma saatleri",
                      "avm kaçta açılıyor", "avm çalışma saatleri nedir"],
    "floor_directory": ["{k} katta neler var", "{k} katta hangi mağazalar var", "{k} kat mağazaları",
                        "{k} kat rehberi", "{k} katta ne var", "{k} kattaki mağazalar", "{k} kat haritası"],
    "greeting_help": ["merhaba", "selam", "iyi günler", "günaydın", "merhaba yardım eder misin", "selamlar",
                      "iyi akşamlar", "hey", "nasılsın", "yardım", "bana yardımcı olur musun", "ne yapabilirsin",
                      "teşekkürler", "sağ ol", "teşekkür ederim", "görüşürüz", "iyi günler dilerim"],
    "out_of_scope": ["hava durumu nasıl", "bugün maç kaçta", "dolar kaç tl", "bana fıkra anlat", "başkent neresi",
                     "kod yaz", "en iyi telefon hangisi", "yarın yağmur yağacak mı", "ödevimi yap", "bana şiir yaz",
                     "bitcoin ne kadar", "kaç yaşındasın", "türkiye nüfusu kaç", "pizza tarifi ver",
                     "otobüs kaçta geçer", "uçak bileti bul", "ankara'ya nasıl gidilir", "bugün günlerden ne",
                     "en yakın hastane nerede", "kargo takibi yap"],
}

# ---------------- Zor test şablonları (eğitimde yok) ----------------
HARD = {
    "find_store": ["{s} diye bir yer arıyorum", "{s} tarafına nasıl geçerim", "{s} neresi yardım eder misiniz",
                   "{s} nerelerde acaba", "{s} için yönlendirir misin", "{s} diye bir yer var mıydı",
                   "arkadaşımla {s} önünde buluşacağız yerini bilmiyorum", "{s} için ne tarafa yürümem lazım"],
    "find_facility": ["{f} tarafı hangisi", "{f} için ne tarafa gideyim", "bi {f} lazım", "{f} yerini gösterir misiniz",
                      "{f} bulamadım"],
    "recommend_category": ["{c} bakmak istiyorum bir fikrin var mı", "{c} konusunda ne önerirsin",
                           "{c} alacağım nereler iyi", "{c} için iyi bir yer biliyor musun"],
    "opening_hours": ["{s} akşam açık mı acaba", "{s} bu saatte hizmet veriyor mu", "{s} mesai saatleri nelerdir",
                      "bugün {s} kaça kadar çalışıyor", "avm bu akşam kaça kadar hizmet veriyor",
                      "alışveriş merkezi akşam kaçta kapanır"],
    "floor_directory": ["{k} kata çıkınca neler görürüm", "{k} katı gezmek istiyorum",
                        "{k} kattaki dükkanları listeler misin", "{k} katın planı var mı"],
    "greeting_help": ["slm", "mrb", "selamun aleyküm", "kolay gelsin", "yardımcı olabilir misiniz", "tesekkurler",
                      "eyvallah", "hoşça kal", "sağolun", "merhabalar nasılsınız", "kolay gelsin yardım lazım"],
    "out_of_scope": ["lahmacun nasıl yapılır", "kahve falı baktırır mısın", "bu telefon kaç gb", "sinema filmi öner evde izlerim",
                     "ayakkabı numarası nasıl ölçülür", "altın fiyatları ne kadar", "saat kaç şu an", "kitap yazarı kim",
                     "elazığ'da hava nasıl", "market alışverişi nasıl bütçelenir", "bana bir şarkı söyle"],
}

# Örtük (anahtar kelime içermeyen) zor örnekler: (metin, varlık_tipi, değer)
HARD_IMPLICIT = {
    "find_facility": [
        ("elimi yıkamam lazım", "facility", "tuvalet"), ("çok sıkıştım nereye gideyim", "facility", "tuvalet"),
        ("para çekmem gerekiyor", "facility", "atm"), ("nakit lazım nereden bulurum", "facility", "atm"),
        ("namaz kılacağım uygun bir yer var mı", "facility", "mescit"),
        ("abdest alıp namaz kılmak istiyorum", "facility", "mescit"),
        ("bebeğimin bezini değiştirmem lazım", "facility", "bebek bakım odası"),
        ("bebeğimi emzirmem gerekiyor", "facility", "bebek bakım odası"),
        ("arabamı nereye park ederim", "facility", "otopark"),
        ("tekerlekli sandalyeyle üst kata nasıl çıkarım", "facility", "asansör"),
        ("kayıp eşya için kime gideyim", "facility", "danışma"),
    ],
    "recommend_category": [
        ("acıktım", "category", "yemek"), ("karnım çok aç", "category", "yemek"),
        ("bir şeyler atıştıracağım", "category", "yemek"), ("canım tatlı çekti", "category", "tatlı"),
        ("çocuğuma bir şeyler bakacağım", "category", "çocuk giyim"),
        ("arkadaşıma doğum günü için bir şey alacağım", "category", "hediye"),
        ("uykum var bir şey içmek istiyorum", "category", "kahve"),
    ],
}

PREFIX = ["lütfen", "acaba", "pardon", "bi sorabilir miyim", "abi", "hocam", "merhaba", "iyi günler"]
SUFFIX = ["lütfen", "acaba", "teşekkürler", "yardım eder misin"]


def load():
    stores = pd.read_csv(AVM / "stores.csv")
    fac = pd.read_csv(AVM / "facility_aliases.csv")
    cat = pd.read_csv(AVM / "category_aliases.csv")
    return stores, fac, cat


def add_typo(tok: str, rng: random.Random) -> str:
    if len(tok) < 4:
        return tok
    i = rng.randrange(1, len(tok) - 1)
    op = rng.choice(["drop", "swap", "dup"])
    if op == "drop":
        return tok[:i] + tok[i + 1:]
    if op == "swap":
        return tok[:i] + tok[i + 1] + tok[i] + tok[i + 2:]
    return tok[:i] + tok[i] + tok[i:]


def noise(text: str, rng: random.Random, p_ascii: float, p_typo: float, p_filler: float) -> str:
    text = tr_lower(text)
    if rng.random() < p_ascii:
        text = text.translate(str.maketrans("ıöüçşğ", "ioucsg"))
    text = " ".join(add_typo(t, rng) if rng.random() < p_typo else t for t in text.split())
    if rng.random() < p_filler:
        text = (rng.choice(PREFIX) + " " + text) if rng.random() < 0.6 else (text + " " + rng.choice(SUFFIX))
    if rng.random() < 0.3:
        text += rng.choice(["?", "??", "!", "."])
    return text


def make_row(intent, template, ctx, rng):
    stores, fac, cat = ctx
    etype, value, slots = None, None, {}
    if "{s}" in template:
        r = stores.iloc[rng.randrange(len(stores))]
        slots["s"], etype, value = r["name"], "store", r["store_id"]
    if "{f}" in template:
        r = fac.iloc[rng.randrange(len(fac))]
        slots["f"], etype, value = r["alias"], "facility", r["type"]
    if "{c}" in template:
        r = cat.iloc[rng.randrange(len(cat))]
        slots["c"], etype, value = r["alias"], "category", r["category"]
    if "{k}" in template:
        surf, fl = rng.choice(FLOORS)
        slots["k"], etype, value = surf, "floor", fl
    return template.format(**slots), etype, value


def build_split(templates, n_per_intent, ctx, rng, seen, p_ascii, p_typo, p_filler, implicit=None):
    rows = []
    for intent in INTENTS:
        got, tries = 0, 0
        pool = list(implicit.get(intent, [])) if implicit else []
        while got < n_per_intent and tries < n_per_intent * 30:
            tries += 1
            if pool and rng.random() < 0.35:
                text, etype, value = rng.choice(pool)
            else:
                text, etype, value = make_row(intent, rng.choice(templates[intent]), ctx, rng)
            text = noise(text, rng, p_ascii, p_typo, p_filler)
            if text in seen:
                continue
            seen.add(text)
            rows.append({"text": text, "intent": intent, "entity_type": etype, "entity_value": value})
            got += 1
    return pd.DataFrame(rows).sample(frac=1, random_state=SEED).reset_index(drop=True)


def main():
    rng = random.Random(SEED)
    ctx = load()
    seen: set = set()
    OUT.mkdir(parents=True, exist_ok=True)
    splits = {
        "train": build_split(TRAIN, 220, ctx, rng, seen, 0.25, 0.04, 0.25),
        "val": build_split(TRAIN, 35, ctx, rng, seen, 0.25, 0.04, 0.25),
        "test": build_split(TRAIN, 40, ctx, rng, seen, 0.25, 0.04, 0.25),
        "test_hard": build_split(HARD, 40, ctx, rng, seen, 0.5, 0.12, 0.4, implicit=HARD_IMPLICIT),
    }
    for name, df in splits.items():
        df.to_csv(OUT / f"{name}.csv", index=False)
        print(f"{name}: {len(df)} satır")


if __name__ == "__main__":
    main()
