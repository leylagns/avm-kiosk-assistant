/* Ortak yardımcılar: oturum, üst menü, sorgu kaydı, katalog erişimi */
const KEY_USER = "avm_user", KEY_LOG = "avm_log";
const store = {
  get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
};
const getUser = () => store.get(KEY_USER, null);
function requireLogin() { if (!getUser()) location.replace("index.html"); }
function logout() { try { localStorage.removeItem(KEY_USER); } catch (e) {} location.href = "index.html"; }
const getLog = () => store.get(KEY_LOG, []);
function addLog(entry) { const l = getLog(); l.unshift(entry); store.set(KEY_LOG, l.slice(0, 200)); }

const FLOOR_NAMES = { 0: "Kat 0 (Zemin)", 1: "Kat 1", 2: "Kat 2" };
const storeById = id => AVM.stores.find(s => s.id === id);
const facById = id => AVM.facilities.find(f => f.id === id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const initials = n => n.split(" ").map(w => w[0]).join("").slice(0, 2).toUpperCase();
const TYPE_LABEL = { tuvalet: "Tuvalet", atm: "ATM", otopark: "Otopark", "asansör": "Asansör", mescit: "Mescit", "bebek bakım odası": "Bebek bakım odası", "danışma": "Danışma" };
const PALETTE = [["#3d4ddb", "#eef0ff"], ["#0ea5e9", "#e0f2fe"], ["#f59e0b", "#fef3c7"], ["#15803d", "#dcfce7"], ["#7c3aed", "#ede9fe"], ["#db2777", "#fce7f3"]];

function isOpen(hours, now = new Date()) {
  const m = /(\d\d):(\d\d)-(\d\d):(\d\d)/.exec(hours || ""); if (!m) return true;
  const t = now.getHours() * 60 + now.getMinutes(), a = +m[1] * 60 + +m[2], b = +m[3] * 60 + +m[4];
  return t >= a && t < b;
}

function renderNav(active) {
  const u = getUser() || { name: "Misafir" };
  const link = (href, label, key) => `<a href="${href}" class="${active === key ? "on" : ""}">${label}</a>`;
  document.getElementById("nav").innerHTML = `
  <header class="topbar">
    <a class="logo" href="ana.html"><i>A</i>AVM Rehber</a>
    <nav class="menu">${link("ana.html", "Ana Sayfa", "ana")}${link("magazalar.html", "Mağazalar", "magaza")}${link("yonetim.html", "Yönetim", "yonetim")}</nav>
    <div class="user"><span class="avatar">${esc(initials(u.name))}</span><span>${esc(u.name)}</span><button class="btn sm" onclick="logout()">Çıkış</button></div>
  </header>`;
}
