"""
Multilingual floating chatbot widget (V-Bot).

- Floating bubble (bottom-right) that opens into a 380x560 chat panel.
- Language auto-detect: Urdu script -> Urdu, Devanagari -> Hindi,
  Arabic script -> Arabic, Roman-Urdu keywords -> Roman Urdu, else English.
- Smalltalk (salam / haal / thanks / bye) in the user's language, and EVERY
  answer also includes an accurate vehicle answer (budget search, vehicle
  lookup, cheapest / most expensive / fastest, family cars, ...).
- Chat history persists in localStorage ("vbot_chat").
"""
import json

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import images


@st.cache_data(show_spinner=False)
def _build_html(df: pd.DataFrame) -> str:
    """Widget HTML with vehicle data embedded (cached - rebuilt only when data changes).

    10,000+ rows me poori list widget me embed karna bara JSON banata hai -
    is liye representative subset: har category ke saste + mehnge vehicles.
    """
    if len(df) <= 600:
        sub = df
    else:
        parts = []
        for cat, g in df.groupby("category"):
            parts.append(g.nsmallest(30, "price_pkr"))
            parts.append(g.nlargest(15, "price_pkr"))
        sub = pd.concat(parts).drop_duplicates(subset="name")
    vehicles = [
        {
            "n": r["name"],
            "c": r["category"],
            "b": r["brand"],
            "p": float(r["price_pkr"]),
            "f": r["fuel_type"],
            "s": int(r["seats"]),
            "t": int(r["top_speed_kmh"]),
            "u": r["pakwheels_url"],
            "g": ("" if pd.isna(r["features_good"]) else str(r["features_good"]).split(";")[0].strip()),
            "d": ("" if pd.isna(r["features_bad"]) else str(r["features_bad"]).split(";")[0].strip()),
            "i": images.image_for(r["name"], r["category"]),
        }
        for _, r in sub.iterrows()
    ]
    data_json = json.dumps(vehicles, ensure_ascii=False)
    return _WIDGET_HTML.replace("__DATA__", data_json)


def render_chatbot(df: pd.DataFrame):
    """Renders the floating chatbot widget. Call it once, at the end of app.py."""
    components.html(
        _build_html(df),
        height=72,
        width=380,
        scrolling=False,
    )


_WIDGET_HTML = r"""
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: "Segoe UI", system-ui, sans-serif; }
  html, body { width: 380px; height: 560px; background: transparent; overflow: hidden; }

  /* ---- bubble ---- */
  #bubble { display: none; position: fixed; bottom: 0; right: 0; width: 64px; height: 64px;
            border-radius: 50%; border: none; cursor: pointer; font-size: 1.7rem;
            background: linear-gradient(135deg, #16a34a, #4ade80); color: #fff;
            box-shadow: 0 10px 26px rgba(34,197,94,.5); transition: transform .25s; }
  #bubble:hover { transform: scale(1.09); }

  /* ---- panel ---- */
  #panel { display: flex; flex-direction: column; position: fixed; bottom: 0; right: 0;
           width: 380px; height: 560px; border-radius: 18px; overflow: hidden;
           background: #060906; border: 1px solid rgba(134,239,172,.22);
           box-shadow: 0 24px 60px rgba(0,0,0,.6), 0 0 40px rgba(34,197,94,.08); }
  #head { display: flex; align-items: center; gap: 9px; padding: 11px 13px;
          background: #0b0f0b; color: #fff; border-bottom: 1px solid rgba(134,239,172,.18); }
  #head .dot { width: 30px; height: 30px; border-radius: 50%;
               background: linear-gradient(135deg, #16a34a, #4ade80);
               display: flex; align-items: center; justify-content: center; font-size: 1.05rem; }
  #head .t { flex: 1; line-height: 1.2; }
  #head .t b { font-size: .92rem; } #head .t span { font-size: .68rem; opacity: .85; display: block; }
  #head button { background: rgba(255,255,255,.18); color: #fff; border: none; width: 28px;
                 height: 28px; border-radius: 8px; cursor: pointer; font-size: .85rem; }
  #head button:hover { background: rgba(255,255,255,.3); }

  #msgs { flex: 1; overflow-y: auto; padding: 11px 11px 4px; display: flex;
          flex-direction: column; gap: 8px; }
  #msgs::-webkit-scrollbar { width: 5px; } #msgs::-webkit-scrollbar-thumb { background: rgba(255,255,255,.15); border-radius: 4px; }

  .m { max-width: 88%; padding: 8px 11px; border-radius: 14px; font-size: .8rem;
       line-height: 1.5; color: #e7ecff; white-space: pre-wrap; word-break: break-word; }
  .m.bot { background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.09);
           border-bottom-left-radius: 4px; align-self: flex-start; }
  .m.user { background: linear-gradient(90deg, #16a34a, #15803d); border-bottom-right-radius: 4px;
            align-self: flex-end; }
  .m.rtl { direction: rtl; text-align: right; }

  .card { margin: 5px 0 2px; padding: 8px 10px; background: rgba(255,255,255,.05);
          border: 1px solid rgba(134,239,172,.16); border-radius: 11px; overflow: hidden; }
  .card::after { content: ""; display: block; clear: both; }
  .thumb { float: left; width: 56px; height: 40px; object-fit: cover; border-radius: 7px;
           margin: 2px 9px 0 0; border: 1px solid rgba(255,255,255,.2); }
  .card .row { display: flex; justify-content: space-between; align-items: baseline; gap: 6px; }
  .card b { font-size: .79rem; color: #fff; }
  .card .price { color: #4ade80; font-weight: 800; font-size: .78rem; white-space: nowrap; }
  .card .hint { color: #9db2a4; font-size: .68rem; margin-top: 2px; line-height: 1.45; }
  .card a { color: #86efac; font-size: .7rem; font-weight: 700; text-decoration: none; }

  #chips { display: flex; gap: 6px; padding: 4px 11px 7px; flex-wrap: wrap; }
  #chips button { font-size: .68rem; padding: 5px 10px; border-radius: 999px; cursor: pointer;
                  background: rgba(34,197,94,.14); color: #b9e6c4;
                  border: 1px solid rgba(134,239,172,.28); }
  #chips button:hover { background: rgba(34,197,94,.3); }

  #inrow { display: flex; gap: 7px; padding: 8px 11px 11px; background: rgba(255,255,255,.04);
           border-top: 1px solid rgba(134,239,172,.14); }
  #inp { flex: 1; background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.14);
         color: #fff; border-radius: 12px; padding: 9px 12px; font-size: .8rem; outline: none; }
  #inp::placeholder { color: #6f8274; }
  #send { width: 40px; border: none; border-radius: 12px; cursor: pointer; font-size: .95rem;
          background: linear-gradient(135deg, #16a34a, #4ade80); color: #fff; }
</style></head>
<body>
  <button id="bubble" title="V-Bot chat">🤖</button>
  <div id="panel">
    <div id="head">
      <div class="dot">🤖</div>
      <div class="t"><b>V-Bot</b><span id="headsub">Vehicle Expert</span></div>
      <button id="clear" title="Clear chat">🗑</button>
      <button id="close" title="Close">✕</button>
    </div>
    <div id="msgs"></div>
    <div id="chips"></div>
    <div id="inrow">
      <input id="inp" type="text" autocomplete="off">
      <button id="send">➤</button>
    </div>
  </div>
<script>
const VEH = __DATA__;
const $ = (id) => document.getElementById(id);

/* ================= language detection ================= */
const URDU_EXTRA = /[ٹڈڑںہۃگچپژیے؛]/;
const ROMAN_URDU = /\b(salam|assalam|asalam|asslam|salaam|kya|kia|kaise|kaisay|kaisa|kahan|kitna|kitne|kitni|hai|hain|acha|achha|nahi|nai|mujhe|mujhay|mera|meri|aap|ap|chahiye|batao|batayen|dekha|dekhna|wala|wali|konsa|kaunsa|theek|shukriya|khuda|hafiz|paisa|paise|paison|ki|ka|ke)\b/i;

function detectLang(t) {
  t = t || "";
  if (/[\u0900-\u097F]/.test(t)) return "hi";
  if (URDU_EXTRA.test(t) || /[\u0600-\u06FF]/.test(t)) {
    if (URDU_EXTRA.test(t)) return "ur";          // Urdu script (reply in Roman Urdu)
    return "ar";                                   // Arabic-only script
  }
  if (ROMAN_URDU.test(t)) return "ur";
  return "en";
}
const RTL = (l) => l === "ar" || (/[\u0600-\u06FF\u0900-\u097F]/.test(""));

/* ================= language strings ================= */
const L = {
  en: {
    wel: "Hi! I'm V-Bot 🤖\nAsk me anything about vehicles — I always reply with a real vehicle suggestion too!",
    how: "I'm great, thanks for asking! How are you doing?",
    thx: "You're very welcome! 😊",
    bye: "Goodbye! Drive safe 🚗",
    greet: "Hello! 👋",
    inBudget: "Best matches under",
    found: "Here's what I found for you",
    cheapest: "The most affordable option right now",
    expensive: "The most expensive one on the list",
    fastest: "The fastest vehicle in the list",
    family: "Great 7-seaters for families",
    def: "Here's a popular choice these days",
    askBudget: "Tell me your budget (like \"5 lakh\" or \"1 crore\") and I'll show the best options!",
    price: "Price",
    pros: "Pro", cons: "Con", buy: "Buy on PakWheels",
    notFound: "I couldn't find that vehicle. Popular picks:",
    chips: ["5 lakh ki car", "Sab se sasti bike", "Civic ka price", "Fastest vehicle"],
  },
  ur: {
    wel: "Assalam-o-Alaikum! Main V-Bot hoon 🤖\nVehicles ke bare me kuch bhi poochein — har jawab ke sath ek asli vehicle ki suggestion bhi mile gi!",
    how: "Main bilkul theek hoon, shukriya! Aap kaise hain?",
    thx: "Khush rahiye! 😊",
    bye: "Khuda Hafiz! Safe drive karein 🚗",
    greet: "Assalam-o-Alaikum! 👋",
    inBudget: "Aap ke budget ke andar ye behtareen options hain",
    found: "Yahan dekhein jo aap ne poocha",
    cheapest: "Sab se sasti option abhi ye hai",
    expensive: "Sab se mehnga vehicle ye hai",
    fastest: "Sab se tez vehicle ye hai",
    family: "Family ke liye behtareen 7-seat vehicles",
    def: "Aaj kal ye option sab se zyada pasand ho raha hai",
    askBudget: "Apna budget batayein (jaise \"5 lakh\" ya \"1 crore\") to main best options dikhaon!",
    price: "Qeemat",
    pros: "Faida", cons: "Nuqsan", buy: "PakWheels par kharidein",
    notFound: "Ye vehicle mujhe nahi mili. Mashhoor options ye hain:",
    chips: ["5 lakh ki bike", "Sab se sasti car", "Alto ki price", "Sab se tez vehicle"],
  },
  hi: {
    wel: "नमस्ते! मैं V-Bot हूँ 🤖\nवाहनों के बारे में कुछ भी पूछें — हर जवाब के साथ एक असली वाहन सुझाव भी मिलेगा!",
    how: "मैं बिल्कुल ठीक हूँ, धन्यवाद! आप कैसे हैं?",
    thx: "आपका स्वागत है! 😊",
    bye: "अलविदा! सुरक्षित ड्राइव करें 🚗",
    greet: "नमस्ते! 👋",
    inBudget: "आपके बजट में ये बेहतरीन विकल्प हैं",
    found: "आपने जो पूछा, ये रहा",
    cheapest: "सबसे सस्ता विकल्प यह है",
    expensive: "सबसे महंगा वाहन यह है",
    fastest: "सबसे तेज़ वाहन यह है",
    family: "परिवार के लिए बेहतरीन 7-सीटर",
    def: "आजकल यह विकल्प सबसे लोकप्रिय है",
    askBudget: "अपना बजट बताएं (जैसे \"5 लाख\" या \"1 करोड़\") तो मैं बेस्ट विकल्प दिखाऊं!",
    price: "कीमत", pros: "फायदा", cons: "नुकसान", buy: "PakWheels पर खरीदें",
    notFound: "यह वाहन नहीं मिला। लोकप्रिय विकल्प:",
    chips: ["5 लाख की कार", "सबसे सस्ती बाइक", "Civic की कीमत", "सबसे तेज़ वाहन"],
  },
  ar: {
    wel: "مرحباً! أنا فـ-بوت 🤖\nاسألني أي شيء عن المركبات — وسيأتي كل رد مع اقتراح مركبة حقيقية!",
    how: "بخير، شكراً! وكيف حالك؟",
    thx: "على الرحب والسعة! 😊",
    bye: "إلى اللقاء! قُد بحذر 🚗",
    greet: "أهلاً! 👋",
    inBudget: "أفضل الخيارات ضمن ميزانية",
    found: "إليك ما وجدته لك",
    cheapest: "الخيار الأرخص حالياً",
    expensive: "أغلى مركبة في القائمة",
    fastest: "أسرع مركبة في القائمة",
    family: "أفضل مركبات 7 مقاعد للعائلة",
    def: "هذا الخيار من الأكثر رواجاً هذه الأيام",
    askBudget: "أخبرني بميزانيتك (مثل \"5 لاكھ\" أو \"1 كرور\") لأعرض لك أفضل الخيارات!",
    price: "السعر", pros: "الميزة", cons: "العيب", buy: "اشترِ على PakWheels",
    notFound: "لم أجد هذه المركبة. خيارات شائعة:",
    chips: ["سيارة بـ 5 لاك", "أرخص دراجة", "سعر سيفيك", "أسرع مركبة"],
  },
};

/* ================= helpers ================= */
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const norm = (s) => String(s || "").toLowerCase().replace(/[^\w\u0600-\u06FF\u0900-\u097F .]+/g, " ").replace(/\s+/g, " ").trim();
const GENERIC = new Set(["used", "import", "imported", "class", "(used", "import)"]);
const aliasOf = (v) => v.n.toLowerCase().split(/[\s()]+/).filter((w) => w.length > 1 && !GENERIC.has(w) && !w.startsWith("("));
const ALIAS = [];
VEH.forEach((v, i) => { aliasOf(v).forEach((a) => ALIAS.push({ a, i })); });

function money(p) {
  if (p >= 1e7) return (p / 1e7).toFixed(2) + " Crore";
  if (p >= 1e5) return (p / 1e5).toFixed(2) + " Lakh";
  return p.toLocaleString("en-PK") + " PKR";
}
function card(v, l) {
  const img = v.i ? '<img class="thumb" src="' + v.i + '" onerror="this.style.display=\'none\'">' : "";
  return '<div class="card">' + img +
    '<div class="row"><b>' + esc(v.n) + '</b><span class="price">' + money(v.p) + '</span></div>' +
    '<div class="hint">' + esc(v.c) + " · " + esc(v.f) + " · " + v.s + " seats · " + v.t + ' km/h</div>' +
    '<div class="hint">✔ ' + esc(v.g) + ' · ✖ ' + esc(v.d) + '</div>' +
    '<a href="' + v.u + '" target="_blank" rel="noopener">' + esc(l.buy) + " →</a></div>";
}
function listCard(vs, l, intro) {
  let s = intro + ":";
  vs.forEach((v) => (s += "\n" + card(v, l)));
  return s;
}

/* budget parsing: "5 lakh", "1 crore", "12,50,000", "200000" */
function parseBudget(t) {
  t = norm(t).replace(/[,.](?=\d{3})/g, "");
  let m = t.match(/(\d+(?:\.\d+)?)\s*(crore|karor|كرور|करोड़)/);
  if (m) return Math.round(parseFloat(m[1]) * 1e7);
  m = t.match(/(\d+(?:\.\d+)?)\s*(lakh|lac|لاک|लाख)/);
  if (m) return Math.round(parseFloat(m[1]) * 1e5);
  m = t.match(/(\d{4,12})/);
  if (m) return parseInt(m[1]);
  return 0;
}
function findVehicle(t) {
  const n = norm(t);
  let full = -1;
  VEH.forEach((v, i) => { if (full < 0 && n.includes(norm(v.n))) full = i; });
  if (full >= 0) return full;
  let best = -1, bestScore = 0;
  VEH.forEach((v, i) => {
    let s = 0;
    aliasOf(v).forEach((a) => { if (n.includes(a)) s += a.length; });
    if (s > bestScore) { bestScore = s; best = i; }
  });
  return best;
}

/* user's category wish, if any ("sab se sasti BIKE" should not return a cycle) */
function catWish(n) {
  if (/bicycle|\bcycle\b/.test(n)) return ["Cycle"];
  if (/bike|motorcycle/.test(n)) return ["Petrol Bike", "Heavy Bike", "Electric Bike", "Scooter"];
  if (/\bcar\b|gaari|gari|car batao|سيارة|कार/.test(n)) return ["Car"];
  return null;
}

/* ================= brain ================= */
function answer(text) {
  const lang = detectLang(text);
  const l = L[lang];
  const n = norm(text);
  let small = "";

  if (/\b(salam|assalam|asalam|asslam|salaam|hello|hi|hey)\b/.test(n) || /سلام|नमस्ते|مرحبا|السلام/.test(n)) small = l.greet + " " + l.wel.split("\n")[0];
  else if (/\b(how are you|kaise ho|kaise hain|kya haal|haal)\b/.test(n) || /كيف حالك|कैसे हो|कैसे हैं/.test(n)) small = l.how;
  else if (/\b(thanks|thank you|shukriya|shukria)\b/.test(n) || /شكرا|धन्यवाद/.test(n)) small = l.thx;
  else if (/\b(bye|goodbye|khuda hafiz|alvida)\b/.test(n) || /الوداع|अलविदा|خدا حافظ/.test(n)) small = l.bye;

  /* --- vehicle part (ALWAYS present) --- */
  let veh = "";
  const bud = parseBudget(text);

  if (bud >= 50_000) {
    const pool = VEH.filter((v) => v.p <= bud).sort((a, b) => b.p - a.p);
    veh = pool.length
      ? listCard(pool.slice(0, 3), l, l.inBudget + " " + money(bud))
      : l.askBudget + "\n" + listCard(VEH.slice().sort((a, b) => a.p - b.p).slice(0, 2), l, l.cheapest);
  } else if (/sab se sasta|sab se sasti|cheapest|सबसे सस्त|أرخص|سستی/.test(n)) {
    const wish = catWish(n);
    const v = VEH.filter((v) => !wish || wish.includes(v.c)).sort((a, b) => a.p - b.p)[0];
    veh = l.cheapest + ":\n" + card(v, l);
  } else if (/mehnga|mehngi|expensive|सबसे महंग|أغلى/.test(n)) {
    const wish = catWish(n);
    const v = VEH.filter((v) => !wish || wish.includes(v.c)).sort((a, b) => b.p - a.p)[0];
    veh = l.expensive + ":\n" + card(v, l);
  } else if (/fast|tez|speed|तेज|أسرع/.test(n)) {
    const wish = catWish(n);
    const v = VEH.filter((v) => !wish || wish.includes(v.c)).sort((a, b) => b.t - a.t)[0];
    veh = l.fastest + ":\n" + card(v, l);
  } else if (/family|7 seat|parivar|عائلة/.test(n)) {
    const pool = VEH.filter((v) => v.s >= 7).sort((a, b) => a.p - b.p);
    veh = listCard(pool.slice(0, 3), l, l.family);
  } else {
    const idx = findVehicle(text);
    if (idx >= 0) {
      veh = l.found + ":\n" + card(VEH[idx], l);
    } else {
      const pop = VEH.filter((v) => /Alto|Swift|CD 70 Dream|Sportage/.test(v.n)).slice(0, 3);
      veh = l.notFound + "\n" + listCard(pop, l, l.def) + "\n\n💬 " + l.askBudget;
    }
  }
  return { lang, html: (small ? small + "\n\n" : "") + veh };
}

/* ================= UI ================= */
let open = false;
let history = [];
try { history = JSON.parse(localStorage.getItem("vbot_chat") || "[]"); } catch (e) { history = []; }

function setMode(o) {
  open = o;
  const f = window.frameElement;
  if (!f) return;
  f.style.position = "fixed"; f.style.bottom = "18px"; f.style.right = "18px"; f.style.zIndex = 999999;
  f.style.width = o ? "380px" : "72px";
  f.style.height = o ? "560px" : "72px";
  f.style.background = "transparent";
  $("bubble").style.display = o ? "none" : "block";
  $("panel").style.display = o ? "flex" : "none";
  if (o) { renderMsgs(); $("inp").focus(); }
}
function bubbleMode() {
  const f = window.frameElement;
  if (!f) return;
  f.style.position = "fixed"; f.style.bottom = "18px"; f.style.right = "18px"; f.style.zIndex = 999999;
  f.style.width = "72px"; f.style.height = "72px";
  $("bubble").style.display = "block";
  $("panel").style.display = "none";
}

function renderMsgs() {
  const box = $("msgs");
  box.innerHTML = "";
  history.forEach((m) => {
    const d = document.createElement("div");
    d.className = "m " + (m.u ? "user" : "bot") + (m.r ? " rtl" : "");
    d.innerHTML = m.h;
    box.appendChild(d);
  });
  box.scrollTop = box.scrollHeight;
}
function push(userHtml, botObj) {
  if (userHtml) history.push({ u: 1, h: esc(userHtml), r: /[\u0600-\u06FF\u0900-\u097F]/.test(userHtml) });
  if (botObj) history.push({ u: 0, h: botObj.html, r: /[\u0600-\u06FF\u0900-\u097F]/.test(textOf(botObj.html)) });
  try { localStorage.setItem("vbot_chat", JSON.stringify(history)); } catch (e) {}
  renderMsgs();
}
function textOf(html) { const d = document.createElement("div"); d.innerHTML = html; return d.textContent || ""; }

function send() {
  const t = $("inp").value.trim();
  if (!t) return;
  setChips(detectLang(t));   // chips follow the user's language
  $("inp").value = "";
  push(t, answer(t));
}

/* chips per last detected language */
function setChips(lang) {
  const box = $("chips");
  box.innerHTML = "";
  (L[lang] || L.en).chips.forEach((c) => {
    const b = document.createElement("button");
    b.textContent = c;
    b.onclick = () => { $("inp").value = c; send(); };
    box.appendChild(b);
  });
  $("headsub").textContent = { en: "Vehicle Expert", ur: "Vehicle Expert (Urdu)", hi: "वाहन विशेषज्ञ", ar: "خبير المركبات" }[lang] || "Vehicle Expert";
}

$("send").onclick = send;
$("inp").addEventListener("keydown", (e) => { if (e.key === "Enter") send(); });
$("bubble").onclick = () => setMode(true);
$("close").onclick = () => setMode(false);
$("clear").onclick = () => { history = []; try { localStorage.removeItem("vbot_chat"); } catch (e) {} renderMsgs(); };

/* boot: welcome message in English, first chip set */
if (!history.length) {
  const a = answer("hello");
  history.push({ u: 0, h: a.html, r: false });
  try { localStorage.setItem("vbot_chat", JSON.stringify(history)); } catch (e) {}
}
bubbleMode();
renderMsgs();
setChips("en");
</script>
</body></html>
"""
