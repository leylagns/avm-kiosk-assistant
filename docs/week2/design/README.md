# Web arayüzü tasarımı (Figma)

**Figma dosyası:** https://www.figma.com/design/l62Wlur5iwBOSl0ak7DEWj
(Dosya sahibi Leyla Güneş. Tıklanabilir prototip için Figma'da sağ üstteki **Present (▶)** düğmesine bas; akış "Kiosk web sitesi akışı" adıyla Giriş ekranından başlar.)

## 6 ekran

| # | Ekran | Amaç | Önizleme |
|---|---|---|---|
| 1 | Giriş | E-posta/şifre ile giriş veya misafir olarak devam | `01-giris.png` |
| 2 | Ana sayfa | Doğal dil arama kutusu, hızlı sorular, sık kullanılan yerler | `02-ana-sayfa.png` |
| 3 | Arama / sohbet | Algılanan niyet, varlık ve güven; öneri kartları; "Şunu mu demek istediniz?" | `03-arama.png` |
| 4 | Rota | Adım adım yönlendirme ve kat haritasında en kısa yol | (Figma'da) |
| 5 | Mağazalar | Kat ve kategori filtreli mağaza/tesis dizini | `05-magazalar.png` |
| 6 | Yönetim | KPI'lar, niyet dağılımı, model karşılaştırma, son sorgular | `06-yonetim.png` |

## Tıklanabilir akış

- Giriş → "Giriş Yap" veya "Misafir olarak devam et" → Ana sayfa
- Ana sayfa → arama kutusu, "Sor", hızlı soru çipleri veya yer kartları → Arama
- Arama → "Yol tarifi" veya önerilen seçenekler → Rota; "Ana sayfa" → Ana sayfa
- Rota → "Aramaya dön" → Arama; "Yeni arama yap" → Ana sayfa
- Mağazalar → herhangi bir "Yol tarifi" → Rota
- Üst menü (Ana Sayfa / Mağazalar / Yönetim / Çıkış) tüm ekranlardan çalışır

## Notlar

- Tasarım sistemi: Inter yazı tipi, ana renk indigo (`#3D4DDB`), vurgu amber (`#F59E0B`); düğme, çip ve rozet yerel bileşen olarak tanımlıdır ("Bileşenler" bölümü).
- Yönetim ekranındaki sayılar **tasarım amaçlı örnek veridir**, gerçek ölçüm değildir. Model karşılaştırma kutusundaki değerler Hafta 3 1. koşu sonuçlarıdır (`docs/week3/comparison.md`).
- Rota ekranının önizleme görseli henüz eklenmedi; Figma'dan dışa aktarılacak.
