# AVM Rehber: web arayüzü (çalışan kod)

Figma tasarımının ([bağlantı](../docs/week2/figma-prototype.md)) HTML/CSS/JS karşılığı. Derleme veya sunucu gerekmez.

## Çalıştırma

```bash
cd web
python -m http.server 8000      # sonra http://localhost:8000 adresini aç
```
(`index.html` dosyasını doğrudan tarayıcıda açmak da çalışır.)

## Sayfalar

| Dosya | Sayfa |
|---|---|
| `index.html` | Giriş / misafir |
| `ana.html` | Ana sayfa, arama kutusu |
| `arama.html` | Sohbet: niyet, varlık, güven, öneri kartları, "Şunu mu demek istediniz?" |
| `rota.html` | Adım adım rota ve kat haritası |
| `magazalar.html` | Arama ve kat/kategori filtreli mağaza dizini |
| `yonetim.html` | Sorgu istatistikleri ve model karşılaştırma |

## Neler gerçek, neler demo?

- **Gerçek:** mağaza/tesis verisi (`data/avm/*.csv` → `js/data.js`, `python scripts/build_web_data.py`), Dijkstra ile kat grafında en kısa rota (`js/route.js`), açık/kapalı hesabı, sorgu kaydı (tarayıcı `localStorage`).
- **Demo:** `js/nlu.js` tarayıcıda çalışan kural + bulanık eşleşme tabanlı küçük NLU'dur. Çıktı biçimi API sözleşmesiyle aynıdır; Hafta 6'da BERTurk modeli FastAPI üzerinden bu yerin yerine geçecek (Hafta 4: backend iskeleti).
- **Demo:** giriş şu an her e-postayı kabul eder; gerçek kimlik doğrulama Hafta 4'te gelecek. Rota mesafeleri örnek değerlerdir.

## Canlı adres

https://leylagns.github.io/avm-kiosk-assistant/
