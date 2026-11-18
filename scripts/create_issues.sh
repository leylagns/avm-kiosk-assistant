#!/usr/bin/env bash
# docs/week1/requirements.md içindeki R1-R10 isterlerini GitHub Issues'a aktarır.
# Kullanım (repo klasöründe): gh auth login && bash scripts/create_issues.sh
set -euo pipefail
gh label create requirement --color 1d76db --description "Proje isteri" 2>/dev/null || true

create() { gh issue create --title "$1" --label requirement --body "$2"; }

create "R1 Sorgu girişi" "Kiosk ekranından yazılı Türkçe sorgu alınır.

**Kabul:** Boş veya 200 karakterden uzun girdi uyarı verir; Türkçe karakterler korunur."
create "R2 Niyet ve varlık çıkarımı" "7 niyet; mağaza, olanak, kategori, kat varlıkları.

**Kabul:** Zor testte makro-F1 >= %85 (Q1), varlık doğruluğu >= %85 (Q2)."
create "R3 Kapsam dışı ve belirsizlik" "Kapsam dışı sorgu reddedilir; düşük güvende açıklayıcı soru sorulur.

**Kabul:** Kapsam dışı örneklerin >= %90'ı reddedilir; düşük güvende rota üretilmez."
create "R4 Katalog yönetimi" "Yönetici mağaza/olanak/saat ekler, düzenler, siler.

**Kabul:** Yetkisiz istek 403 döner; geçersiz alan hata verir."
create "R5 Rota" "Kat grafında en kısa rota; katlar arası asansör/yürüyen merdiven.

**Kabul:** 50 çiftte en kısa yolla uyum >= %95 (Q4)."
create "R6 Sonuç gösterimi" "Rota harita üzerinde ve adım adım tarif olarak gösterilir.

**Kabul:** Kat değişimi tarifte açıkça belirtilir."
create "R7 Bilgi sorguları" "Çalışma saati ve kat rehberi yanıtlanır.

**Kabul:** Katalogdaki bilgiyle birebir uyumlu."
create "R8 Model yönetimi" "E1/E2/E3 yapılandırmayla değişir; model sürümü kaydedilir.

**Kabul:** Model değişimi servisi yeniden yazmadan yapılır."
create "R9 Kayıt ve gizlilik" "Kişisel veri tutulmaz; loglar anonim, kapatılabilir ve silinebilir.

**Kabul:** Log kapalıyken sorgu metni saklanmaz."
create "R10 Hata yönetimi" "Model zaman aşımı, bilinmeyen mağaza, rota yok, DB hatası kontrollü ele alınır.

**Kabul:** Her durumda anlaşılır mesaj; kiosk boşta başlangıç ekranına döner."
