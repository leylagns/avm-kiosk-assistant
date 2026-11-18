# Sistem Mimarisi

```mermaid
flowchart TB
    subgraph Kiosk[Kiosk ekranı - tarayıcı, tam ekran]
        UI[Web arayüzü<br/>sorgu girişi, harita, tarif]
    end
    subgraph Sunucu[Kiosk sunucusu - Docker Compose]
        API[FastAPI<br/>/query /route /catalog /auth]
        NLU[NLU modülü<br/>E1 / E2 / E3]
        ROUTE[Rota modülü<br/>kat grafı + Dijkstra]
        DB[(PostgreSQL<br/>katalog, graf, kullanıcı, log)]
    end
    ADMIN[Yönetici paneli]
    UI -->|HTTPS/JSON| API
    ADMIN -->|JWT ile| API
    API --> NLU
    API --> ROUTE
    API --> DB
    NLU -->|varlık doğrulama| DB
    ROUTE --> DB
```

| Katman | Teknoloji | Görev |
|---|---|---|
| Arayüz | Web (tarayıcı) | Sorgu girişi, harita, adım adım tarif |
| API | FastAPI | İstek doğrulama, kimlik doğrulama, orkestrasyon |
| NLU | scikit-learn / Transformers | Niyet ve varlık çıkarımı |
| Rota | Python (Dijkstra) | Kat grafında en kısa yol |
| Veri | PostgreSQL | Katalog, graf, yönetici, anonim loglar |
| Dağıtım | Docker Compose | Tek komutla kurulum |

**Gizlilik:** Sorgu metni kişisel veri içermez; loglar anonim ve kapatılabilir (R9).
