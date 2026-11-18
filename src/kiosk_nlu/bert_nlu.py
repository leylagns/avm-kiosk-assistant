"""E2: BERTurk ile niyet sınıflandırma + varlık sınıflandırma (iki ince ayarlı baş).

- Niyet başı: 7 niyetten birini tahmin eder.
- Varlık başı: "store:S17", "facility:tuvalet", "category:yemek", "floor:2" gibi etiketlerden birini tahmin eder.
  Çıkarım sırasında yalnızca tahmin edilen niyetin beklediği türdeki etiketler değerlendirilir.
  Böylece "acıktım" gibi anahtar kelime içermeyen cümlelerde de varlık bulunabilir (sözlük bunu yapamaz).

Not: torch ve transformers gerektirir (Colab'da hazır / pip install transformers).
"""
import random
import time

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

from .gazetteer import INTENT_ENTITY
from .generate_dataset import INTENTS

DEFAULT_MODEL = "dbmdz/bert-base-turkish-cased"  # BERTurk


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


class BertNLU:
    def __init__(self, model_name: str = DEFAULT_MODEL, max_len: int = 48, epochs: int = 4,
                 lr: float = 3e-5, batch_size: int = 32, seed: int = 42, device: str | None = None):
        self.model_name, self.max_len, self.epochs = model_name, max_len, epochs
        self.lr, self.batch_size, self.seed = lr, batch_size, seed
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tok = AutoTokenizer.from_pretrained(model_name)
        self.intent_model = None
        self.entity_model = None
        self.entity_labels: list[str] = []

    # ---------- eğitim ----------
    def _encode(self, texts):
        enc = self.tok(list(texts), truncation=True, max_length=self.max_len, padding="max_length", return_tensors="pt")
        return enc["input_ids"], enc["attention_mask"]

    def _train_head(self, texts, labels, label_list, name):
        set_seed(self.seed)
        label_to_id = {l: i for i, l in enumerate(label_list)}
        y = torch.tensor([label_to_id[l] for l in labels])
        ids, mask = self._encode(texts)
        loader = DataLoader(TensorDataset(ids, mask, y), batch_size=self.batch_size, shuffle=True)
        model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=len(label_list))
        model.to(self.device).train()
        opt = torch.optim.AdamW(model.parameters(), lr=self.lr, weight_decay=0.01)
        total = len(loader) * self.epochs
        sched = get_linear_schedule_with_warmup(opt, int(0.1 * total), total)
        for ep in range(self.epochs):
            running = 0.0
            for b_ids, b_mask, b_y in loader:
                b_ids, b_mask, b_y = b_ids.to(self.device), b_mask.to(self.device), b_y.to(self.device)
                out = model(input_ids=b_ids, attention_mask=b_mask, labels=b_y)
                out.loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                opt.step(); sched.step(); opt.zero_grad()
                running += out.loss.item()
            print(f"[{name}] epoch {ep + 1}/{self.epochs}  loss={running / len(loader):.4f}")
        model.eval()
        return model

    def fit(self, df: pd.DataFrame):
        """df: text, intent, entity_type, entity_value sütunları (train.csv)."""
        self.intent_model = self._train_head(df.text, df.intent, INTENTS, "niyet")
        ent = df[df.entity_type.notna()]
        labels = [f"{t}:{v}" for t, v in zip(ent.entity_type, ent.entity_value.astype(str))]
        self.entity_labels = sorted(set(labels))
        self.entity_model = self._train_head(ent.text, labels, self.entity_labels, "varlık")
        return self

    # ---------- çıkarım ----------
    @torch.no_grad()
    def _logits(self, model, text):
        ids, mask = self._encode([text])
        return model(input_ids=ids.to(self.device), attention_mask=mask.to(self.device)).logits[0].float().cpu()

    def parse(self, text: str) -> dict:
        proba = torch.softmax(self._logits(self.intent_model, text), dim=-1)
        i = int(proba.argmax())
        intent, conf = INTENTS[i], float(proba[i])
        etype, value = INTENT_ENTITY.get(intent), None
        if etype is not None:
            logits = self._logits(self.entity_model, text)
            allowed = [j for j, l in enumerate(self.entity_labels) if l.startswith(etype + ":")]
            if allowed:
                best = max(allowed, key=lambda j: float(logits[j]))
                value = self.entity_labels[best].split(":", 1)[1]
        return {"intent": intent, "confidence": conf, "entity_type": etype, "entity_value": value}

    def n_params(self) -> int:
        """İki başın toplam parametre sayısı."""
        return sum(p.numel() for m in (self.intent_model, self.entity_model) for p in m.parameters())

    def predict_intents(self, texts):
        return [self.parse(t)["intent"] for t in texts]
