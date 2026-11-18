import pandas as pd
import pytest

from kiosk_nlu.gazetteer import Gazetteer
from kiosk_nlu.text import normalize
from kiosk_nlu.generate_dataset import INTENTS, OUT


@pytest.fixture(scope="module")
def gaz():
    return Gazetteer()


def test_normalize_turkish():
    assert normalize("Moda Sokağı'nda") == "moda sokaginda"
    assert normalize("İSTANBUL") == "istanbul"
    assert normalize("1. kat!") == "1 kat"


def test_store_exact_and_fuzzy(gaz):
    assert gaz.extract("Moda Sokağı nerede", "find_store") == ("store", "S01")
    assert gaz.extract("moda sokagi nerde", "find_store") == ("store", "S01")
    assert gaz.extract("kebap saryı nerede", "find_store") == ("store", "S17")  # yazım hatası


def test_facility_and_category(gaz):
    assert gaz.extract("en yakın wc nerede", "find_facility") == ("facility", "tuvalet")
    assert gaz.extract("bankamatik var mı", "find_facility") == ("facility", "atm")
    assert gaz.extract("ayakkabı önerir misin", "recommend_category") == ("category", "ayakkabı")


def test_floor(gaz):
    assert gaz.extract("zemin katta neler var", "floor_directory") == ("floor", 0)
    assert gaz.extract("ikinci kat rehberi", "floor_directory") == ("floor", 2)


def test_no_entity_for_greeting(gaz):
    assert gaz.extract("merhaba", "greeting_help") == (None, None)


def test_unknown_store_returns_none(gaz):
    assert gaz.extract("olmayan dükkan nerede", "find_store") == ("store", None)


def test_dataset_files_valid():
    for name in ["train", "val", "test", "test_hard", "test_llm"]:
        df = pd.read_csv(OUT / f"{name}.csv")
        assert set(df.intent) <= set(INTENTS)
        assert df.text.notna().all()


def test_no_leakage_between_splits():
    sets = {n: set(pd.read_csv(OUT / f"{n}.csv").text) for n in ["train", "val", "test", "test_hard", "test_llm"]}
    names = list(sets)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            assert not (sets[a] & sets[b]), f"{a} ve {b} arasında aynı metin var"


def test_rule_model_basics():
    from kiosk_nlu.rules import RuleNLU
    m = RuleNLU()
    assert m.parse("kebap sarayı nerede")["intent"] == "find_store"
    assert m.parse("pizza fırını kaça kadar açık")["intent"] == "opening_hours"
    assert m.parse("en yakın wc")["entity_value"] == "tuvalet"
    assert m.parse("bugün hava nasıl")["intent"] == "out_of_scope"
