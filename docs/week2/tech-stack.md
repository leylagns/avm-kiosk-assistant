# Teknoloji Yığını

| Katman | Teknoloji | Neden |
|---|---|---|
| Dil | Python 3.10+ | NLP kütüphaneleri, FastAPI |
| Klasik NLU (E1) | scikit-learn | Hızlı baseline |
| Transformer (E2) | Hugging Face Transformers, BERTurk | Türkçe önceden eğitilmiş model |
| Küçük dil modeli (E3) | Transformers + PEFT (LoRA), küçük LLM | Hafif ince ayar |
| Eğitim ortamı | Google Colab / Kaggle (ücretsiz GPU) | Yerel GPU yok |
| Backend | FastAPI, Uvicorn | Hızlı, otomatik Swagger |
| Veritabanı | PostgreSQL, SQLAlchemy, Alembic | İlişkisel veri, migration |
| Rota | Python (heapq ile Dijkstra) | Küçük graf, bağımlılık yok |
| Arayüz | Web (React + Vite veya düz HTML/JS) | Kiosk tarayıcıda tam ekran |
| Tasarım | Figma | Tıklanabilir prototip |
| Test | pytest, Locust (stres) | Birim ve yük testi |
| Dağıtım | Docker Compose | Tek komutla kurulum |
| Sürüm kontrol | GitHub, Issues, `v1.0` etiketi | Ders gereksinimi |
