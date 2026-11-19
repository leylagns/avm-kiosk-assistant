"""data/avm/*.csv -> web/js/data.js  (tarayıcıda dosya okumadan çalışsın diye).
Kullanım: python scripts/build_web_data.py"""
import csv, json, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
def rd(n): return list(csv.DictReader(open(root / "data/avm" / n, encoding="utf-8")))
stores = [{"id": r["store_id"], "name": r["name"], "category": r["category"], "floor": int(r["floor"]), "zone": r["zone"], "hours": r["opening_hours"]} for r in rd("stores.csv")]
facs = [{"id": r["facility_id"], "type": r["type"], "floor": int(r["floor"]), "zone": r["zone"], "desc": r["description"]} for r in rd("facilities.csv")]
fa = [{"type": r["type"], "alias": r["alias"]} for r in rd("facility_aliases.csv")]
ca = [{"category": r["category"], "alias": r["alias"]} for r in rd("category_aliases.csv")]
out = "// Otomatik üretildi: scripts/build_web_data.py (elle düzenlemeyin)\nconst AVM = " + json.dumps({"stores": stores, "facilities": facs, "facilityAliases": fa, "categoryAliases": ca}, ensure_ascii=False, indent=1) + ";\n"
(root / "web/js/data.js").write_text(out, encoding="utf-8")
print(len(stores), "mağaza,", len(facs), "tesis ->", "web/js/data.js")
