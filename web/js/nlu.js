/* TARAYICIDA ÇALIŞAN DEMO NLU (kural + bulanık eşleşme).
   Gerçek model (BERTurk, notebooks/02_colab_week3.ipynb) Hafta 6'da FastAPI üzerinden bağlanacak.
   Çıktı biçimi API sözleşmesiyle aynıdır: {intent, confidence, entity_type, entity_value}. */
const NLU = (() => {
  const fold = s => s.toLocaleLowerCase("tr").replace(/['’]/g, "").replace(/ı/g, "i").replace(/ş/g, "s").replace(/ğ/g, "g")
    .replace(/ü/g, "u").replace(/ö/g, "o").replace(/ç/g, "c").replace(/[^a-z0-9 ]+/g, " ").replace(/\s+/g, " ").trim();
  function lev(a, b) {
    const d = Array.from({ length: a.length + 1 }, (_, i) => [i, ...Array(b.length).fill(0)]);
    for (let j = 1; j <= b.length; j++) d[0][j] = j;
    for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++)
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    return d[a.length][b.length];
  }
  const sim = (a, b) => 1 - lev(a, b) / Math.max(a.length, b.length);

  const cands = {
    store: AVM.stores.map(s => ({ key: fold(s.name), value: s.id, label: s.name })),
    facility: AVM.facilityAliases.map(a => ({ key: fold(a.alias), value: a.type, label: TYPE_LABEL[a.type] || a.type })),
    category: AVM.categoryAliases.map(a => ({ key: fold(a.alias), value: a.category, label: a.category })),
  };
  const IMPLICIT = [[/\b(acikti|aciktim|aciktik|karnim ac|yemek yiyelim|bir seyler yiyelim|yemek yiyecek)/, "yemek"], [/\b(cay|kahve) (icelim|icecegim|icmek)/, "kahve"]];

  // metinde aday arar: tam/ekli eşleşme (güven yüksek) veya bulanık eşleşme (güven düşük)
  function match(text, list, minSim = 0.8) {
    const toks = text.split(" "); let best = null;
    for (const c of list) {
      const long = c.key.length > 3;
      const re = new RegExp(`(^| )${c.key}${long ? "[a-z]{0,5}" : ""}( |$)`);
      if (re.test(text)) { const sc = 1 + c.key.length / 100; if (!best || sc > best.score) best = { ...c, sim: 1, score: sc, exact: true }; continue; }
      if (!long) continue;
      const n = c.key.split(" ").length;
      for (let i = 0; i + n <= toks.length; i++) {
        const w = toks.slice(i, i + n).join(" "), s = Math.max(sim(w, c.key), n === 1 && w.length > c.key.length ? sim(w.slice(0, c.key.length + 1), c.key) : 0);
        if (w.length > 3 && s >= minSim && (!best || (!best.exact && s > best.score))) best = { ...c, sim: s, score: s, exact: false };
      }
    }
    return best;
  }
  const fuzzyConf = s => Math.max(0.35, 0.5 + (s - 0.8));
  const HOURS = /(kacta|saat kac|acik mi|kapan|acilis|kapanis|mesai|kaca kadar|ne zamana kadar|acik)/;
  const FLOOR = /(zemin|\b[0-2] ?\.? ?kat|birinci kat|ikinci kat|ust kat|alt kat|kat \d)/;
  const GREET = /^(merhaba|selam|gunaydin|iyi (aksamlar|gunler)|yardim|nasil kullan|ne yapabilirsin|sen kimsin|kimsin)/;

  function parse(raw) {
    const t = fold(raw), out = (intent, conf, type, value, extra = {}) => ({ intent, confidence: +conf.toFixed(2), entity_type: type, entity_value: value, ...extra });
    if (!t) return out("out_of_scope", 0, null, null);
    const f = match(t, cands.facility); if (f) return out("find_facility", f.exact ? 0.94 : fuzzyConf(f.sim), "facility", f.value, { label: f.label, fuzzy: !f.exact });
    const s = match(t, cands.store);
    if (s) return out(HOURS.test(t) ? "opening_hours" : "find_store", s.exact ? 0.95 : fuzzyConf(s.sim), "store", s.value, { label: s.label, fuzzy: !s.exact });
    if (/(avm|alisveris merkezi|merkez)/.test(t) && HOURS.test(t)) return out("opening_hours", 0.9, null, null);
    if (FLOOR.test(t)) { const m = /([0-2])/.exec(t); const fl = /zemin/.test(t) ? 0 : /birinci|alt kat/.test(t) ? 1 : /ikinci|ust kat/.test(t) ? 2 : m ? +m[1] : null; if (fl !== null) return out("floor_directory", 0.9, "floor", String(fl)); }
    const c = match(t, cands.category, 0.86); if (c) return out("recommend_category", c.exact ? 0.88 : fuzzyConf(c.sim), "category", c.value, { label: c.label, fuzzy: !c.exact });
    for (const [re, cat] of IMPLICIT) if (re.test(t)) return out("recommend_category", 0.82, "category", cat, { label: cat });
    if (GREET.test(t)) return out("greeting_help", 0.9, null, null);
    return out("out_of_scope", 0.6, null, null);
  }
  // "Şunu mu demek istediniz?" için aynı türden en yakın alternatifler
  function alternatives(res, raw) {
    if (!res.entity_type || !cands[res.entity_type]) return [];
    const t = fold(raw), seen = new Set([res.entity_value]), arr = [];
    for (const c of cands[res.entity_type]) { if (seen.has(c.value)) continue; const best = Math.max(...t.split(" ").map(w => sim(w, c.key.split(" ")[0]))); arr.push({ c, best }); }
    arr.sort((a, b) => b.best - a.best);
    return arr.filter((x, i, a) => a.findIndex(y => y.c.value === x.c.value) === i).slice(0, 2).map(x => x.c);
  }
  return { parse, alternatives, fold };
})();
