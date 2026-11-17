"""
ChatGPT-powered chat for Vhology (ai.py).

- render_chat(df)    : native Streamlit chat UI (wired at the end of app.py)
- ask_openai()       : real ChatGPT answer via the OpenAI API (gpt-4o-mini),
                       the vehicle dataset is passed as system context
- fallback_answer()  : built-in multilingual rule engine (English / Roman Urdu /
                       Hindi / Arabic) - the SAME brain as the floating V-Bot
- ZERO ERRORS: if no API key is configured, or the API call fails for any
  reason, the chat silently falls back to the rule engine - it never crashes.
"""
import os
import re

import pandas as pd
import requests
import streamlit as st

import ml

# ---------------------------------------------------------------- settings
_MODEL = "gpt-4o-mini"
_API_URL = "https://api.openai.com/v1/chat/completions"


def _key():
    """OPENAI_API_KEY from Streamlit secrets or environment (never raises)."""
    try:
        return st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        pass
    return os.environ.get("OPENAI_API_KEY", "")


def _data_text(df: pd.DataFrame) -> str:
    """Compact dataset context for the ChatGPT system prompt.

    10,000+ rows me poora dataset bhejna API ke liye bohat bara hota hai -
    is liye representative subset: har category ke saste + mehnge vehicles.
    """
    if len(df) <= 400:
        sub = df
    else:
        parts = []
        for cat, g in df.groupby("category"):
            parts.append(g.nsmallest(8, "price_pkr"))
            parts.append(g.nlargest(5, "price_pkr"))
        sub = pd.concat(parts).drop_duplicates(subset="name")
    lines = []
    for _, r in sub.iterrows():
        lines.append(
            f"{r['name']} | {r['category']} | {r['brand']} | {ml.money(r['price_pkr'])}"
            f" | {r['fuel_type']} | {r['seats']} seats | {r['top_speed_kmh']} km/h"
            f" | buy: {r['pakwheels_url']}"
        )
    return "\n".join(lines)


def ask_openai(question: str, df: pd.DataFrame):
    """Real ChatGPT answer, or None when unavailable (no key / any error)."""
    key = _key()
    if not key:
        return None
    try:
        resp = requests.post(
            _API_URL,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": _MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are V-Bot, the friendly vehicle expert of Vhology, a Pakistani "
                            "vehicle budget advisor app. Answer ANY question the user asks "
                            "(general chat, jokes, studies, anything) - and when it is about "
                            "vehicles, money or buying, ALWAYS ground your answer in this exact "
                            "vehicle dataset (do not invent vehicles or prices):\n\n"
                            + _data_text(df)
                            + "\n\nRules: reply in the SAME language the user writes in "
                            "(English, Roman Urdu, Urdu, Hindi or Arabic). Keep answers short "
                            "(max ~120 words). For vehicle suggestions give 1-3 concrete "
                            "vehicles with their price and the PakWheels link from the dataset. "
                            "Mention a pro (faida) and a con (nuqsan) when suggesting vehicles."
                        ),
                    },
                    {"role": "user", "content": question},
                ],
                "max_tokens": 500,
                "temperature": 0.6,
            },
            timeout=25,
        )
        if resp.status_code != 200:
            return None
        return (resp.json()["choices"][0]["message"]["content"] or "").strip() or None
    except Exception:
        return None


# ================================================================ fallback
# (multilingual rule engine - same logic as the floating V-Bot widget)

URDU_EXTRA = re.compile(r"[ٹڈڑںہۃگچپژیے؛]")
ROMAN_URDU = re.compile(
    r"\b(salam|assalam|asalam|asslam|salaam|kya|kia|kaise|kaisay|kaisa|kahan|kitna|kitne"
    r"|kitni|hai|hain|acha|achha|nahi|nai|mujhe|mujhay|mera|meri|aap|ap|chahiye|batao"
    r"|batayen|dekha|dekhna|wala|wali|konsa|kaunsa|theek|shukriya|khuda|hafiz|paisa"
    r"|paise|paison|ki|ka|ke)\b",
    re.IGNORECASE,
)

L = {
    "en": {
        "how": "I'm great, thanks for asking! How are you doing?",
        "thx": "You're very welcome! 😊",
        "bye": "Goodbye! Drive safe 🚗",
        "greet": "Hello! 👋 I'm V-Bot, ask me anything — vehicles, prices, anything at all!",
        "buy": "Buy on PakWheels",
        "inBudget": "Best matches under",
        "found": "Here's what I found for you",
        "cheapest": "The most affordable option right now",
        "expensive": "The most expensive one on the list",
        "fastest": "The fastest vehicle in the list",
        "family": "Great 7-seaters for families",
        "def": "Here's a popular choice these days",
        "askBudget": "Tell me your budget (like \"5 lakh\" or \"1 crore\") and I'll show the best options!",
        "notFound": "I couldn't find that vehicle. Popular picks:",
    },
    "ur": {
        "how": "Main bilkul theek hoon, shukriya! Aap kaise hain?",
        "thx": "Khush rahiye! 😊",
        "bye": "Khuda Hafiz! Safe drive karein 🚗",
        "greet": "Assalam-o-Alaikum! 👋 Main V-Bot hoon — kuch bhi poochein, vehicle ya aur bhi kuch!",
        "buy": "PakWheels par kharidein",
        "inBudget": "Aap ke budget ke andar ye behtareen options hain",
        "found": "Yahan dekhein jo aap ne poocha",
        "cheapest": "Sab se sasti option abhi ye hai",
        "expensive": "Sab se mehnga vehicle ye hai",
        "fastest": "Sab se tez vehicle ye hai",
        "family": "Family ke liye behtareen 7-seat vehicles",
        "def": "Aaj kal ye option sab se zyada pasand ho raha hai",
        "askBudget": "Apna budget batayein (jaise \"5 lakh\" ya \"1 crore\") to main best options dikhaon!",
        "notFound": "Ye vehicle mujhe nahi mili. Mashhoor options ye hain:",
    },
    "hi": {
        "how": "मैं बिल्कुल ठीक हूँ, धन्यवाद! आप कैसे हैं?",
        "thx": "आपका स्वागत है! 😊",
        "bye": "अलविदा! सुरक्षित ड्राइव करें 🚗",
        "greet": "नमस्ते! 👋 मैं V-Bot हूँ — कुछ भी पूछें, वाहन या और भी कुछ!",
        "buy": "PakWheels पर खरीदें",
        "inBudget": "आपके बजट में ये बेहतरीन विकल्प हैं",
        "found": "आपने जो पूछा, ये रहा",
        "cheapest": "सबसे सस्ता विकल्प यह है",
        "expensive": "सबसे महंगा वाहन यह है",
        "fastest": "सबसे तेज़ वाहन यह है",
        "family": "परिवार के लिए बेहतरीन 7-सीटर",
        "def": "आजकल यह विकल्प सबसे लोकप्रिय है",
        "askBudget": "अपना बजट बताएं (जैसे \"5 लाख\" या \"1 करोड़\") तो मैं बेस्ट विकल्प दिखाऊं!",
        "notFound": "यह वाहन नहीं मिला। लोकप्रिय विकल्प:",
    },
    "ar": {
        "how": "بخير، شكراً! وكيف حالك؟",
        "thx": "على الرحب والسعة! 😊",
        "bye": "إلى اللقاء! قُد بحذر 🚗",
        "greet": "أهلاً! 👋 أنا فـ-بوت — اسألني أي شيء، مركبات أو غير ذلك!",
        "buy": "اشترِ على PakWheels",
        "inBudget": "أفضل الخيارات ضمن ميزانية",
        "found": "إليك ما وجدته لك",
        "cheapest": "الخيار الأرخص حالياً",
        "expensive": "أغلى مركبة في القائمة",
        "fastest": "أسرع مركبة في القائمة",
        "family": "أفضل مركبات 7 مقاعد للعائلة",
        "def": "هذا الخيار من الأكثر رواجاً هذه الأيام",
        "askBudget": "أخبرني بميزانيتك (مثل \"5 لاكھ\" أو \"1 كرور\") لأعرض لك أفضل الخيارات!",
        "notFound": "لم أجد هذه المركبة. خيارات شائعة:",
    },
}

GENERIC = {"used", "import", "imported", "class"}


def detect_lang(text: str) -> str:
    """en / ur (Roman Urdu + Urdu script) / hi (Devanagari) / ar (Arabic)."""
    t = text or ""
    if re.search(r"[\u0900-\u097F]", t):
        return "hi"
    if URDU_EXTRA.search(t):
        return "ur"
    if re.search(r"[\u0600-\u06FF]", t):
        return "ar"
    if ROMAN_URDU.search(t):
        return "ur"
    return "en"


def _norm(s: str) -> str:
    # keep letters, digits, spaces, dots (so "2.5 lakh" keeps its decimal point)
    return re.sub(r"\s+", " ", re.sub(r"[^\w\u0600-\u06FF\u0900-\u097F .]+", " ", (s or "").lower())).strip()


def _aliases(name: str):
    return [
        w
        for w in re.split(r"[\s()]+", (name or "").lower())
        if len(w) > 1 and w not in GENERIC and not w.startswith("(")
    ]


def parse_budget(text: str) -> int:
    """'5 lakh' / '1 crore' / '12,50,000' / '200000' -> PKR (0 if none)."""
    t = _norm(text)
    t = re.sub(r"[,.](?=\d{3})", "", t)
    m = re.search(r"(\d+(?:\.\d+)?)\s*(crore|karor|كرور|करोड़)", t)
    if m:
        return round(float(m.group(1)) * 10_000_000)
    m = re.search(r"(\d+(?:\.\d+)?)\s*(lakh|lac|لاک|लाख)", t)
    if m:
        return round(float(m.group(1)) * 100_000)
    m = re.search(r"(\d{4,12})", t)
    if m:
        return int(m.group(1))
    return 0


def find_vehicle(df: pd.DataFrame, text: str):
    """DataFrame row of the best-matching vehicle, or None."""
    n = _norm(text)
    for _, r in df.iterrows():
        if _norm(r["name"]) in n:
            return r
    best, best_score = None, 0
    for _, r in df.iterrows():
        score = 0
        for a in _aliases(r["name"]):
            if a in n:
                score += len(a)
        if score > best_score:
            best_score, best = score, r
    return best


def _cat_wish(n: str):
    """User's category wish from the wording ('sab se sasti BIKE' -> bikes only)."""
    if re.search(r"bicycle|\bcycle\b", n):
        return ["Cycle"]
    if re.search(r"bike|motorcycle", n):
        return ["Petrol Bike", "Heavy Bike", "Electric Bike", "Scooter"]
    if re.search(r"\bcar\b|gaari|gari|سيارة|कार", n):
        return ["Car"]
    return None


def _card(r, lang: str) -> str:
    """Compact markdown card for one vehicle row (pandas Series)."""
    l = L[lang]
    pros = ml.split_list(r.get("features_good"))
    cons = ml.split_list(r.get("features_bad"))
    extra = ""
    if pros:
        extra += f"\n✔ {pros[0]}"
    if cons:
        extra += f" · ✖ {cons[0]}"
    return (
        f"**{r['name']}** — *{ml.money(r['price_pkr'])}*"
        f"\n{r['category']} · {r['fuel_type']} · {int(r['seats'])} seats · {int(r['top_speed_kmh'])} km/h{extra}"
        f"\n[{l.get('buy', 'Buy on PakWheels')}]({r['pakwheels_url']})"
    )


def _cards(rows, lang: str) -> str:
    return "\n\n".join(_card(r, lang) for _, r in rows.iterrows())


def fallback_answer(question: str, df: pd.DataFrame) -> str:
    """Rule-based answer with smalltalk + a real vehicle suggestion, or None."""
    lang = detect_lang(question)
    l = L[lang]
    n = _norm(question)
    small = ""

    if re.search(r"\b(salam|assalam|asalam|asslam|salaam|hello|hi|hey)\b", n) or re.search(r"سلام|नमस्ते|مرحبا|السلام", n):
        small = l["greet"]
    elif re.search(r"\b(how are you|kaise ho|kaise hain|kya haal|haal)\b", n) or re.search(r"كيف حالك|कैसे हो|कैसे हैं", n):
        small = l["how"]
    elif re.search(r"\b(thanks|thank you|shukriya|shukria)\b", n) or re.search(r"شكرا|धन्यवाद", n):
        small = l["thx"]
    elif re.search(r"\b(bye|goodbye|khuda hafiz|alvida)\b", n) or re.search(r"الوداع|अलविदा|خدا حافظ", n):
        return l["bye"]  # no vehicle push after goodbye

    bud = parse_budget(question)
    if bud >= 50_000:
        pool = df[df["price_pkr"] <= bud].sort_values("price_pkr", ascending=False)
        if len(pool):
            veh = f"{l['inBudget']} **{ml.money(bud)}**:\n\n" + _cards(pool.head(3), lang)
        else:
            veh = l["askBudget"] + "\n\n" + l["cheapest"] + ":\n\n" + _cards(df.nsmallest(2, "price_pkr"), lang)
    elif re.search(r"sab se sasta|sab se sasti|cheapest|सबसे सस्त|أرخص|سستی", n):
        wish = _cat_wish(n)
        pool = df[df["category"].isin(wish)] if wish else df
        veh = l["cheapest"] + ":\n\n" + _card(pool.loc[pool["price_pkr"].idxmin()], lang)
    elif re.search(r"mehnga|mehngi|expensive|सबसे महंग|أغلى", n):
        wish = _cat_wish(n)
        pool = df[df["category"].isin(wish)] if wish else df
        veh = l["expensive"] + ":\n\n" + _card(pool.loc[pool["price_pkr"].idxmax()], lang)
    elif re.search(r"fast|tez|speed|तेज|أسرع", n):
        wish = _cat_wish(n)
        pool = df[df["category"].isin(wish)] if wish else df
        veh = l["fastest"] + ":\n\n" + _card(pool.loc[pool["top_speed_kmh"].idxmax()], lang)
    elif re.search(r"family|7 seat|parivar|عائلة", n):
        pool = df[df["seats"] >= 7].sort_values("price_pkr")
        veh = l["family"] + ":\n\n" + _cards(pool.head(3), lang)
    else:
        r = find_vehicle(df, question)
        if r is not None:
            veh = l["found"] + ":\n\n" + _card(r, lang)
        else:
            pop = df[df["name"].str.contains("Alto|Swift|CD 70 Dream|Sportage", regex=True)].head(3)
            veh = l["notFound"] + "\n\n" + _cards(pop, lang) + "\n\n💬 " + l["askBudget"]

    return (small + "\n\n" + veh).strip()


# ================================================================ chat UI
def _reply(question: str, df: pd.DataFrame) -> str:
    """ChatGPT first, built-in engine as guaranteed fallback (never raises)."""
    ans = ask_openai(question, df)
    if ans:
        return ans
    try:
        return fallback_answer(question, df)
    except Exception:
        return "Maaf kijiye, thori technical masla hua — dobara likhein? 🙂"


def render_chat(df: pd.DataFrame):
    """Native Streamlit chat (ChatGPT-powered). Call once at the end of app.py."""
    ss = st.session_state
    ss.setdefault("chat_hist", [])

    st.markdown(
        "<div class='stepchip'>[ <b>V-BOT</b> ] &middot; ChatGPT se juda hua &middot; har sawal ka jawab"
        " (English &middot; Roman Urdu &middot; हिंदी &middot; عربي)</div>",
        unsafe_allow_html=True,
    )

    with st.container():
        for m in ss.chat_hist:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

    q = st.chat_input("Sawal likhein... (jaise: 15 lakh ki best car?)")
    if q and q.strip():
        ss.chat_hist.append({"role": "user", "content": q.strip()})
        with st.chat_message("user"):
            st.markdown(q.strip())
        with st.chat_message("assistant"):
            with st.spinner("V-Bot soch raha hai..."):
                ans = _reply(q.strip(), df)
            st.markdown(ans)
        ss.chat_hist.append({"role": "assistant", "content": ans})
        st.rerun()
