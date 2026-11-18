# avm-kiosk-assistant

AVM kiosk için Türkçe doğal dil asistanı: kullanıcının cümlesinden **niyeti ve varlığı** (mağaza, olanak, kategori, kat) çıkarır, kat planı grafında rota bulur. Yapay Zeka ve Veri Mühendisliği Tasarımı dersi bitirme projesidir.

## Durum (haftalara göre)

| Hafta | Konu | Nerede |
|---|---|---|
| 0 | Konu + öneri formu | ders sistemi / `docs/` |
| 1 | Diyagramlar, isterler | [docs/week1](docs/week1) |
| 2 | Mockup, veritabanı | [docs/week2](docs/week2) |
| 3 | Veri, EDA, baseline | [docs/week3](docs/week3), [notebooks/01_eda.ipynb](notebooks/01_eda.ipynb) |

## Kurulum ve çalıştırma

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export PYTHONPATH=src              # Windows PowerShell: $env:PYTHONPATH="src"
python -m kiosk_nlu.generate_dataset   # veri setini üretir (data/processed/)
python -m kiosk_nlu.evaluate           # baseline'ı eğitir ve raporu yazar
pytest                                 # testler
```

## Yapı

```
data/avm/         AVM kataloğu (mağaza, olanak, takma adlar)  - kurgusal AVM
data/processed/   üretilen veri seti: train, val, test, test_hard
src/kiosk_nlu/    metin normalizasyonu, sözlük eşleştirme, baseline, veri üretici, değerlendirme
notebooks/        EDA
docs/             haftalık teslimler
results/          metrikler ve hata listeleri
scripts/          yardımcı betikler (GitHub Issues aktarımı)
tests/            birim testleri
```

## Veri seti

7 niyet: `find_store`, `find_facility`, `recommend_category`, `opening_hours`, `floor_directory`, `greeting_help`, `out_of_scope`.
Veri **sentetiktir** (şablon + gürültü, seed=42). Asıl ölçüt `test_hard` kümesidir (eğitimde olmayan şablonlar, örtük ifadeler, ağır gürültü). Gerçek kullanıcı sorguları toplandıkça bu kümeye eklenecektir.

## İlk baseline (E1: TF-IDF + Lojistik Regresyon)

| Küme | Niyet doğruluğu | Varlık doğruluğu |
|---|---|---|
| test (dağılım içi) | 1.000 | 0.974 |
| test_hard | 0.664 | 0.601 |

Ayrıntılar: [docs/week3/baseline-report.md](docs/week3/baseline-report.md)
