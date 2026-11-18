# Veri Sözlüğü

## Veritabanı tabloları

| Tablo | Alan | Tür | Açıklama |
|---|---|---|---|
| floors | floor_no | INT, PK | Kat numarası (0 = zemin) |
| floors | name | TEXT | Kat adı |
| graph_nodes | node_id | SERIAL, PK | Kat planındaki düğüm |
| graph_nodes | floor_no | INT, FK | Düğümün katı |
| graph_nodes | kind | TEXT | corridor, store, facility, elevator, escalator, entrance, kiosk |
| graph_nodes | x, y | REAL | Kat planı koordinatı |
| graph_edges | from_node, to_node | INT, FK | Bağlanan düğümler |
| graph_edges | weight_m | REAL | Yürüme mesafesi (metre), > 0 |
| graph_edges | edge_type | TEXT | walk, elevator, escalator |
| categories | name | TEXT, UNIQUE | Mağaza kategorisi (yemek, giyim...) |
| category_aliases | alias | TEXT | Kategori için kullanıcı ifadesi (restoran, lokanta...) |
| facility_types | name | TEXT, UNIQUE | Olanak türü (tuvalet, atm, mescit...) |
| facility_aliases | alias | TEXT | Olanak için kullanıcı ifadesi (wc, bankamatik...) |
| stores | store_id | TEXT, PK | Mağaza kodu (S01...) |
| stores | name | TEXT, UNIQUE | Mağaza adı |
| stores | category_id | INT, FK | Kategori |
| stores | node_id | INT, FK | Mağazanın graf düğümü |
| stores | zone | TEXT | Bölge (A, B, C) |
| stores | opens_at, closes_at | TIME | Çalışma saatleri |
| facilities | facility_id | TEXT, PK | Olanak kodu (F01...) |
| facilities | type_id, node_id | INT, FK | Tür ve konum |
| admin_users | username, password_hash, role | TEXT | Yönetici; parola yalnızca hash olarak saklanır |
| model_versions | name, kind | TEXT | Model adı, E1/E2/E3 |
| model_versions | val_macro_f1 | REAL | Doğrulama makro-F1 |
| model_versions | is_active | BOOL | Aynı anda yalnızca bir aktif model |
| query_logs | created_at | TIMESTAMPTZ | Sorgu zamanı |
| query_logs | query_text | TEXT, NULL | Anonim sorgu metni; log kapalıysa NULL |
| query_logs | intent, confidence | TEXT, REAL | Tahmin edilen niyet ve güven |
| query_logs | latency_ms | INT | Uçtan uca yanıt süresi |

## Veri seti dosyaları (`data/processed/*.csv`)

| Sütun | Açıklama |
|---|---|
| text | Kullanıcı sorgusu (gürültülü, küçük harf) |
| intent | find_store, find_facility, recommend_category, opening_hours, floor_directory, greeting_help, out_of_scope |
| entity_type | store, facility, category, floor veya boş (varlık yok) |
| entity_value | store_id, olanak türü, kategori adı veya kat numarası; boş olabilir |

## Bölünmeler

| Dosya | Satır | Amaç |
|---|---|---|
| train.csv | 1540 | Eğitim |
| val.csv | 245 | Eşik/hiperparametre seçimi |
| test.csv | 280 | Dağılım içi kontrol |
| test_hard.csv | 280 | Zor değerlendirme: yeni şablonlar, örtük ifade, ağır gürültü (şablonla üretilmiş) |
| test_llm.csv | 100'e yakın | Şablonlardan bağımsız, gerçek ziyaretçi tarzında cümleler. **Bir dil modeli (LLM) tarafından yazıldı, gerçek kullanıcı verisi değildir**; eğitime hiç girmez. Gerçek sorgular toplanınca `test_real.csv` olarak eklenecek. |
