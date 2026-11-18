# Figma Prototipi: Ekran Tarifleri (7 ekran)

Kiosk: 1080×1920 dikey ekran. Yönetici paneli: 1440×900 masaüstü. Büyük dokunmatik hedefler (en az 64 px), yüksek kontrast.

| # | Ekran | Bileşenler | Tıklama akışı |
|---|---|---|---|
| 1 | **Karşılama** | Logo, "Merhaba, size nasıl yardımcı olabilirim?", büyük "Soru sor" düğmesi, 4 örnek soru çipi ("Tuvalet nerede?", "Yemek yiyebileceğim yerler") | Soru sor / çip → Ekran 2 |
| 2 | **Soru girişi** | Metin kutusu, Türkçe ekran klavyesi, "Gönder", "Geri" | Gönder → Ekran 3 (yükleniyor) → Ekran 4 / 5 / 6 |
| 3 | **Yükleniyor** | Dönen gösterge, "Anlıyorum..." | Otomatik → sonuç ekranı |
| 4 | **Rota sonucu** | Kat planı haritası üzerinde çizgi, "Buradasınız" ve hedef işareti, adım adım tarif listesi (kat değişimi ikonlu), "Yeni soru" | Yeni soru → Ekran 1 |
| 5 | **Liste sonucu** | Kategori/kat sonucu mağaza kartları (ad, kat, çalışma saati), karta dokununca rota | Kart → Ekran 4 |
| 6 | **Anlaşılamadı / kapsam dışı** | Nazik mesaj, "Şunu mu demek istediniz?" öneri düğmeleri, "Danışmaya yönlendir" | Öneri → Ekran 3; Yeni soru → Ekran 2 |
| 7 | **Yönetici paneli** | Giriş formu; katalog tablosu (mağaza/olanak ekle-düzenle-sil); model sürümü seçimi ve metrikleri; kullanım istatistikleri | Giriş → panel sekmeleri |

**Hata durumları (ekran 6 varyantları):** boş girdi uyarısı, sunucu yanıt vermiyor, rota bulunamadı.

**Boşta davranışı:** 60 sn dokunma yoksa Ekran 1'e dönülür.
