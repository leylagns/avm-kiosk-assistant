/* Kat grafı + Dijkstra. Düğümler: "<kat><bölge>" (ör. "0B"). Asansör B bölgesinde, her katı dikey bağlar.
   Mesafeler metre cinsinden örnek değerlerdir (gerçek ölçek Hafta 4'te veritabanından gelecek). */
const KIOSK = { floor: 0, zone: "B", name: "Kiosk 1, giriş katı" };
const ROUTE = (() => {
  const edges = {}; const add = (a, b, w, kind) => { (edges[a] ??= []).push({ to: b, w, kind }); (edges[b] ??= []).push({ to: a, w, kind }); };
  for (const f of [0, 1, 2]) { add(`${f}A`, `${f}B`, 45, "walk"); add(`${f}B`, `${f}C`, 45, "walk"); }
  for (const f of [0, 1]) add(`${f}B`, `${f + 1}B`, 40, "lift");
  function dijkstra(src, dst) {
    const dist = { [src]: 0 }, prev = {}, todo = new Set([src]);
    while (todo.size) {
      let u = null; for (const n of todo) if (u === null || dist[n] < dist[u]) u = n; todo.delete(u);
      if (u === dst) break;
      for (const e of edges[u] || []) { const nd = dist[u] + e.w; if (dist[e.to] === undefined || nd < dist[e.to]) { dist[e.to] = nd; prev[e.to] = { from: u, kind: e.kind, w: e.w }; todo.add(e.to); } }
    }
    const path = []; for (let n = dst; n; n = prev[n]?.from) { path.unshift({ node: n, via: prev[n] }); if (n === src) break; }
    return { path, meters: dist[dst] };
  }
  function plan(dest) { // dest: {name, floor, zone}
    const src = `${KIOSK.floor}${KIOSK.zone}`, dst = `${dest.floor}${dest.zone}`, r = dijkstra(src, dst);
    const steps = [{ t: `Buradasınız: ${KIOSK.name}`, s: `Kat ${KIOSK.floor}, ${KIOSK.zone} bölgesi` }];
    for (const p of r.path.slice(1)) {
      const f = +p.node[0], z = p.node[1];
      steps.push(p.via.kind === "lift"
        ? { t: `Asansörle ${f > +p.via.from[0] ? f + ". kata çıkın" : f === 0 ? "zemin kata inin" : f + ". kata inin"}`, s: `Kat ${p.via.from[0]} → Kat ${f}` }
        : { t: `${z} bölgesine doğru ilerleyin`, s: `${p.via.w} m` });
    }
    steps.push({ t: `${dest.name} bu bölgede, ${["sağ", "sol"][dest.name.length % 2]} tarafınızda`, s: "Vardınız" });
    const floors = [...new Set(r.path.map(p => +p.node[0]))];
    const bySeg = {}; r.path.forEach(p => (bySeg[p.node[0]] ??= []).push(p.node[1]));
    const lifts = r.path.filter(p => p.via?.kind === "lift").length;
    return { steps, meters: r.meters, minutes: Math.max(1, Math.round(r.meters / 60 + lifts * 0.5)), floors, bySeg };
  }
  return { plan };
})();
