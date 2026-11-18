"""Baseline (E1): TF-IDF (karakter n-gram) + Lojistik Regresyon + sözlük tabanlı varlık çıkarımı."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

from .gazetteer import Gazetteer
from .text import normalize


class BaselineNLU:
    def __init__(self, C: float = 10.0, gazetteer: Gazetteer | None = None):
        self.gaz = gazetteer or Gazetteer()
        self.clf = make_pipeline(
            TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), preprocessor=normalize, sublinear_tf=True),
            LogisticRegression(C=C, max_iter=2000),
        )

    def fit(self, texts, intents):
        self.clf.fit(list(texts), list(intents))
        return self

    def predict_intents(self, texts):
        return self.clf.predict(list(texts))

    def parse(self, text: str) -> dict:
        proba = self.clf.predict_proba([text])[0]
        i = int(proba.argmax())
        intent = str(self.clf.classes_[i])
        etype, value = self.gaz.extract(text, intent)
        return {"intent": intent, "confidence": float(proba[i]), "entity_type": etype, "entity_value": value}
