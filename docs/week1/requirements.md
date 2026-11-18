# İsterler (R1–R10)

| ID | İster | Kabul ölçütü |
|---|---|---|
| R1 | Sorgu girişi: kiosk ekranından yazılı Türkçe sorgu alınır | Boş veya 200 karakterden uzun girdi uyarı verir; Türkçe karakterler korunur |
| R2 | Niyet ve varlık çıkarımı: 7 niyet; mağaza, olanak, kategori, kat | Zor testte makro-F1 ≥ %85 (Q1), varlık doğruluğu ≥ %85 (Q2) |
| R3 | Kapsam dışı ve belirsizlik: ret ve açıklayıcı soru | Kapsam dışı örneklerin ≥ %90'ı reddedilir; düşük güvende rota üretilmez |
| R4 | Katalog yönetimi: yönetici mağaza/olanak/saat ekler, düzenler, siler | Yetkisiz istek 403 döner; geçersiz alan hata verir |
| R5 | Rota: kat grafında en kısa rota; katlar arası asansör/yürüyen merdiven | 50 çiftte en kısa yolla uyum ≥ %95 (Q4) |
| R6 | Sonuç gösterimi: harita üzerinde rota ve adım adım tarif | Kat değişimi tarifte açıkça belirtilir |
| R7 | Bilgi sorguları: çalışma saati ve kat rehberi | Katalogdaki saat/kat bilgisiyle birebir uyumlu |
| R8 | Model yönetimi: E1/E2/E3 yapılandırmayla değişir; sürüm kaydedilir | Model değişimi servisi yeniden yazmadan yapılır |
| R9 | Kayıt ve gizlilik: kişisel veri yok; anonim, kapatılabilir ve silinebilir loglar | Log kapalıyken sorgu metni saklanmaz |
| R10 | Hata yönetimi: model zaman aşımı, bilinmeyen mağaza, rota yok, DB hatası | Her durumda kullanıcıya anlaşılır mesaj; kiosk boşta başlangıca döner |

## GitHub Issues'a aktarma
Bilgisayarında `gh` (GitHub CLI) kurulu ve giriş yapılmış olmalı:

```bash
gh auth login
bash scripts/create_issues.sh
```

Betik her isteri bir issue olarak açar ve `requirement` etiketi ekler.
