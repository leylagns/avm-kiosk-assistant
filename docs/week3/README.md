# Hafta 3: Veri ve AI Baseline

- [../../notebooks/02_colab_week3.ipynb](../../notebooks/02_colab_week3.ipynb): Colab'da çalıştırılan E1 + E2 (BERTurk) karşılaştırması
- [baseline-report.md](baseline-report.md): E1 baseline sonuçları, hata analizi (yerelde üretilen ilk sürüm)
- [../../notebooks/01_eda.ipynb](../../notebooks/01_eda.ipynb): keşifsel veri analizi
- `figures/`: karışıklık matrisleri ve EDA grafikleri
- Veri: `data/processed/` (üretici: `src/kiosk_nlu/generate_dataset.py`)

## Sınıfta 5 dk demo akışı
1. Veri setini ve zor testi göster (EDA grafikleri).
2. `python -m kiosk_nlu.evaluate` çalıştır; rapordaki tabloyu göster.
3. Dağılım içi %100 ile zor test %66 arasındaki farkı anlat; hedefin (Q1/Q2 ≥ %85) nasıl kapatılacağını (E2, E3) söyle.
