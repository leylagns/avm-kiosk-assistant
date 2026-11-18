# Hafta 2: Figma tıklanabilir prototip (AVM Rehber web sitesi)

**Figma dosyası:** https://www.figma.com/design/l62Wlur5iwBOSl0ak7DEWj

Sunum için: dosyayı aç, sağ üstte **Present (▶)** düğmesine bas. Akış "Kiosk web sitesi akışı" adıyla Giriş ekranından başlar.

## 6 ekran

| # | Ekran | Amaç |
|---|---|---|
| 1 | Giriş | E-posta/şifre ile giriş veya misafir olarak devam |
| 2 | Ana sayfa | Doğal dil arama kutusu, hızlı sorular, sık kullanılan yerler |
| 3 | Arama / sohbet | Algılanan niyet, varlık ve güven; öneri kartları; "Şunu mu demek istediniz?" |
| 4 | Rota | Adım adım yönlendirme ve kat haritasında en kısa yol |
| 5 | Mağazalar | Kat ve kategori filtreli mağaza/tesis dizini |
| 6 | Yönetim | KPI'lar, niyet dağılımı, model karşılaştırma, son sorgular |

## Tıklanabilir akış

- Giriş → "Giriş Yap" veya "Misafir olarak devam et" → Ana sayfa
- Ana sayfa → arama kutusu, "Sor", hızlı soru çipleri veya yer kartları → Arama
- Arama → "Yol tarifi" veya önerilen seçenekler → Rota; "Ana sayfa" → Ana sayfa
- Rota → "Aramaya dön" → Arama; "Yeni arama yap" → Ana sayfa
- Mağazalar → herhangi bir "Yol tarifi" → Rota
- Üst menü (Ana Sayfa / Mağazalar / Yönetim / Çıkış) tüm ekranlardan çalışır

## Tasarım kararları

- **Güven eşiği arayüzde görünür (Ekran 3):** Model emin değilse sonuç doğrudan gösterilmez, kullanıcıya "Şunu mu demek istediniz?" ile onaylatılır. Hafta 3'teki risk–kapsama analizinin ürün karşılığıdır.
- **Yönetim ekranı (Ekran 6):** Sayılar tasarım amaçlı örnek veridir. Model karşılaştırma kutusu Hafta 3 1. koşu sonuçlarını kullanır.
- **Tasarım sistemi:** Inter yazı tipi, ana renk indigo, vurgu amber; düğme, çip ve rozet yerel bileşenlerdir.
