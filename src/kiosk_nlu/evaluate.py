"""Baseline değerlendirmesi: metrikleri ölçer, grafik ve rapor üretir.

Çalıştırma:  PYTHONPATH=src python -m kiosk_nlu.evaluate
"""
import json
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

from .baseline import BaselineNLU
from .generate_dataset import INTENTS

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"
RES = ROOT / "results"
FIG = ROOT / "docs" / "week3" / "figures"

# Hedefler: öneri formundaki nicel hedeflerle AYNI olmalı (Q1, Q2, Q3)
TARGETS = {"intent_macro_f1_hard": 0.85, "entity_acc_hard": 0.85, "p95_latency_ms": 500.0}


def same(a, b):
    if pd.isna(a) and pd.isna(b):
        return True
    return str(a) == str(b)


def evaluate_split(model, df):
    lat, parsed = [], []
    for text in df.text:
        s = time.perf_counter()
        parsed.append(model.parse(text))
        lat.append((time.perf_counter() - s) * 1000)
    pred = pd.DataFrame(parsed)
    out = df.copy()
    out["pred_intent"] = pred["intent"]
    out["pred_entity"] = pred["entity_value"]
    out["confidence"] = pred["confidence"]
    has_ent = out["entity_type"].notna()
    ent_ok = [same(g, p) if (isinstance(p, str) or pd.isna(p)) else same(str(g), str(p))
              for g, p in zip(out["entity_value"], out["pred_entity"])]
    out["intent_ok"] = out.intent == out.pred_intent
    out["entity_ok"] = ent_ok
    ent_acc = float(np.mean(np.array(ent_ok)[has_ent.values]))
    e2e = float(np.mean((out.intent_ok & (out.entity_ok | ~has_ent)).values))
    return out, {
        "intent_acc": float(accuracy_score(out.intent, out.pred_intent)),
        "intent_macro_f1": float(f1_score(out.intent, out.pred_intent, average="macro")),
        "entity_acc": ent_acc,
        "end_to_end_acc": e2e,
        "latency_mean_ms": float(np.mean(lat)),
        "latency_p95_ms": float(np.percentile(lat, 95)),
        "n": int(len(out)),
    }


def plot_cm(out, path, title):
    cm = confusion_matrix(out.intent, out.pred_intent, labels=INTENTS)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(INTENTS)), INTENTS, rotation=45, ha="right")
    ax.set_yticks(range(len(INTENTS)), INTENTS)
    for i in range(len(INTENTS)):
        for j in range(len(INTENTS)):
            ax.text(j, i, cm[i, j], ha="center", va="center", color="white" if cm[i, j] > cm.max() / 2 else "black")
    ax.set_xlabel("Tahmin"); ax.set_ylabel("Gerçek"); ax.set_title(title)
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)


def main():
    RES.mkdir(exist_ok=True); FIG.mkdir(parents=True, exist_ok=True)
    train, val, test, hard = (pd.read_csv(DATA / f"{n}.csv") for n in ["train", "val", "test", "test_hard"])

    # C seçimi doğrulama setiyle (test setleri model seçiminde kullanılmaz)
    best_c, best_f1 = None, -1
    for c in [1, 10, 100]:
        m = BaselineNLU(C=c).fit(train.text, train.intent)
        f1 = f1_score(val.intent, m.predict_intents(val.text), average="macro")
        if f1 > best_f1:
            best_c, best_f1 = c, f1
    model = BaselineNLU(C=best_c).fit(train.text, train.intent)

    maj = DummyClassifier(strategy="most_frequent").fit(train.text, train.intent)
    maj_hard = float(accuracy_score(hard.intent, maj.predict(hard.text)))

    out_t, m_test = evaluate_split(model, test)
    out_h, m_hard = evaluate_split(model, hard)
    metrics = {"best_C": best_c, "val_macro_f1": float(best_f1), "majority_acc_hard": maj_hard,
               "test": m_test, "test_hard": m_hard, "targets": TARGETS}
    (RES / "baseline_metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    plot_cm(out_t, FIG / "confusion_test.png", "Karışıklık matrisi: test (dağılım içi)")
    plot_cm(out_h, FIG / "confusion_test_hard.png", "Karışıklık matrisi: test_hard")
    errs = out_h[~(out_h.intent_ok & (out_h.entity_ok | out_h.entity_type.isna()))]
    errs.to_csv(RES / "errors_test_hard.csv", index=False)
    rep = classification_report(out_h.intent, out_h.pred_intent, labels=INTENTS, output_dict=True, zero_division=0)

    def ok(v, t, lower=True):
        return "✅" if (v >= t if lower else v <= t) else "❌"

    lines = [
        "# Hafta 3: Baseline (E1) Raporu", "",
        "Model: **TF-IDF (karakter 2-5 gram) + Lojistik Regresyon** (niyet) ve **sözlük + bulanık eşleştirme** (varlık).",
        f"Hiperparametre `C={best_c}` doğrulama setinde seçildi; test setleri model seçiminde kullanılmadı.",
        "Veri sentetiktir (bkz. `src/kiosk_nlu/generate_dataset.py`); gerçek kullanıcı sorguları eklenince zor test güncellenecek.", "",
        "## Sonuçlar", "",
        "| Metrik | test (dağılım içi) | test_hard | Hedef (öneri formu) | Durum (hard) |", "|---|---|---|---|---|",
        f"| Niyet doğruluğu | {m_test['intent_acc']:.3f} | {m_hard['intent_acc']:.3f} | - | - |",
        f"| Niyet makro-F1 (Q1) | {m_test['intent_macro_f1']:.3f} | {m_hard['intent_macro_f1']:.3f} | ≥ {TARGETS['intent_macro_f1_hard']} | {ok(m_hard['intent_macro_f1'], TARGETS['intent_macro_f1_hard'])} |",
        f"| Varlık doğruluğu (Q2) | {m_test['entity_acc']:.3f} | {m_hard['entity_acc']:.3f} | ≥ {TARGETS['entity_acc_hard']} | {ok(m_hard['entity_acc'], TARGETS['entity_acc_hard'])} |",
        f"| Uçtan uca doğruluk (niyet+varlık) | {m_test['end_to_end_acc']:.3f} | {m_hard['end_to_end_acc']:.3f} | - | - |",
        f"| Gecikme ort. (ms) | {m_test['latency_mean_ms']:.2f} | {m_hard['latency_mean_ms']:.2f} | - | - |",
        f"| Gecikme p95 (ms), yalnızca NLU (Q3'ün parçası) | {m_test['latency_p95_ms']:.2f} | {m_hard['latency_p95_ms']:.2f} | ≤ {TARGETS['p95_latency_ms']:.0f} | {ok(m_hard['latency_p95_ms'], TARGETS['p95_latency_ms'], lower=False)} |",
        "", f"Referans: çoğunluk sınıfı tahmini test_hard üzerinde {maj_hard:.3f} doğruluk verir.", "",
        "**Yorum:** Dağılım içi testte neredeyse mükemmel sonuç, şablon verisinde başarının doygunluğa ulaştığını gösterir; "
        "asıl ölçüt zor testtir. Q1 ve Q2 hedefleri E2 (BERTurk) ve E3 (küçük dil modeli) ile karşılanmaya çalışılacaktır.", "",
        "## test_hard sınıf bazlı F1", "", "| Niyet | Precision | Recall | F1 |", "|---|---|---|---|",
    ]
    for k in INTENTS:
        r = rep[k]
        lines.append(f"| {k} | {r['precision']:.2f} | {r['recall']:.2f} | {r['f1-score']:.2f} |")
    lines += ["", "![test_hard](figures/confusion_test_hard.png)", "",
              "## Hata analizi (test_hard, ilk 12 hata)", "", "| Metin | Gerçek | Tahmin | Gerçek varlık | Tahmin varlık |", "|---|---|---|---|---|"]
    for r in errs.head(12).itertuples():
        lines.append(f"| {r.text} | {r.intent} | {r.pred_intent} | {r.entity_value} | {r.pred_entity} |")
    lines += ["", f"Toplam hatalı örnek: {len(errs)} / {len(out_h)} (tamamı: `results/errors_test_hard.csv`).", ""]
    (ROOT / "docs" / "week3" / "baseline-report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
