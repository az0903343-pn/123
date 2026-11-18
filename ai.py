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


def ask_openai(question: str, df: pd.DataFrame, history=None):
    """Real ChatGPT answer (with prior conversation context), or None when unavailable."""
    key = _key()
    if not key:
        return None
    msgs = []
    for m in (history or []):
        if m.get("role") in ("user", "assistant") and m.get("content"):
            msgs.append({"role": m["role"], "content": m["content"]})
    msgs = msgs[-8:]  # aakhri 8 messages ka context
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
                            + "\n\nRules: ALWAYS reply in ENGLISH, no matter which "
                            "language the user writes in. Keep answers short "
                            "(max ~120 words). For vehicle suggestions give 1-3 concrete "
                            "vehicles with their price and the PakWheels link from the dataset. "
                            "Mention a pro (faida) and a con (nuqsan) when suggesting vehicles."
                        ),
                    },
                    *msgs,
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
        "general": "Interesting question! 🌟 I'm the vehicle expert here — but turn **ChatGPT mode ON** (add `OPENAI_API_KEY` in the app secrets) and I can chat about absolutely anything. Meanwhile, tell me your budget and I'll find your perfect ride!",
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
        "general": "Zabardast sawal! 🌟 **ChatGPT mode ON** karein (app secrets me `OPENAI_API_KEY` add karein) to main kisi bhi topic par poori baat kar sakta hoon. Filhal vehicles ka expert hoon — apna budget batayein, best ride dhoond deta hoon!",
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
        "general": "शानदार सवाल! 🌟 **ChatGPT मोड ON** करें (app secrets में `OPENAI_API_KEY` जोड़ें) तो मैं किसी भी विषय पर बात कर सकता हूँ। फिलहाल वाहन विशेषज्ञ हूँ — अपना बजट बताएं, बेस्ट राइड ढूंढ देता हूँ!",
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
        "general": "سؤال رائع! 🌟 شغّل **وضع ChatGPT** (أضف `OPENAI_API_KEY` في إعدادات التطبيق) لأستطيع الحديث عن أي موضوع. حالياً خبير المركبات هنا — أخبرني بميزانيتك وسأجد لك أفضل ركوب!",
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


def _vehicle_sounding(n: str) -> bool:
    """Does the text look like a vehicle/money question? (general fallback ke liye)"""
    return bool(
        re.search(
            r"car|gaari|gari|bike|cycle|vehicle|sasta|sasti|mehnga|mehngi|tez|fast|speed"
            r"|price|qeemat|kimat|kitne|kitna|budget|lakh|crore|engine|milege|mileage|suv"
            r"|jeep|scooter|rickshaw|tractor|boat|helicopter|jet\b|plane|jahaz|seat|family"
            r"|electric|diesel|petrol|hybrid|imported|model|gear",
            n,
        )
    )


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
    # English-only mode: har fallback jawab English me (user request)
    lang = "en"
    l = L[lang]
    n = _norm(question)
    small = ""

    if re.search(r"\b(salam|assalam|asalam|asslam|salaam|hello|hi|hey|good morning|good evening)\b", n) or re.search(r"سلام|नमस्ते|مرحبا|السلام", n):
        small = l["greet"]
    elif re.search(r"\b(how are you|how r u|kaise ho|kaise hain|kya haal|haal)\b", n) or re.search(r"كيف حالك|कैसे हो|कैसे हैं", n):
        small = l["how"]
    elif re.search(r"\b(thanks|thank you|shukriya|shukria)\b", n) or re.search(r"شكرا|धन्यवाद", n):
        small = l["thx"]
    elif re.search(r"\b(bye|goodbye|khuda hafiz|alvida|good night)\b", n) or re.search(r"الوداع|अलविदा|خدا حافظ", n):
        return l["bye"]  # no vehicle push after goodbye
    elif re.search(r"\b(who are you|your name|tum kaun|aap kaun|tumhara naam|apna intro|introduce)\b", n):
        small = (
            "I'm **V-Bot** 🤖 — the AI companion of Vhology! I know all 10,000+ vehicles in the "
            "dataset (prices, pros, cons, mods) and with ChatGPT ON I can chat about *anything* "
            "— studies, sports, jokes, general knowledge. Try: *\"best car under 20 lakh\"*!"
        )
    elif re.search(r"\b(what can you do|help|madad|features|how to use)\b", n):
        small = (
            "Here's what I can do 👇\n\n"
            "- 🚗 **Vehicle search** — *\"civic ka price?\"*, *\"CD 70 dikhao\"*\n"
            "- 💰 **Budget picks** — *\"best car under 15 lakh\"*, *\"1 crore ki SUV\"*\n"
            "- 🏆 **Superlatives** — *\"cheapest bike\"*, *\"fastest vehicle\"*\n"
            "- 👨‍👩‍👧 **Family picks** — *\"7 seater family car\"*\n"
            "- 💬 **General chat** — with ChatGPT ON, ask me *anything*!"
        )
    elif re.search(r"\b(joke|hasao|mazak)\b", n):
        small = "Why did the car apply for a job? 🚗 It wanted to *drive* its career forward! 😄"
    elif re.search(r"\b(ok|okay|okey|good|great|nice|cool|wow|amazing|super|acha|achha|theek|haan|haanji|han ji|yes|yep|yup|lol|hmm)\b", n):
        small = "Glad to hear that! 😊 Anything else you'd like to ask — vehicles, budget, or any topic?"

    bud = parse_budget(question)
    has_intent = bud >= 50_000 or _vehicle_sounding(n)
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
        elif _vehicle_sounding(n):
            pop = df[df["name"].str.contains("Alto|Swift|CD 70 Dream|Sportage", regex=True)].head(3)
            veh = l["notFound"] + "\n\n" + _cards(pop, lang) + "\n\n💬 " + l["askBudget"]
        else:
            # general / non-vehicle baat (ChatGPT OFF ho to friendly jawab + suggestion)
            pop = df[df["name"].str.contains("Alto|Swift|CD 70 Dream|Sportage", regex=True)].head(1)
            veh = l["general"] + "\n\n" + l["def"] + ":\n\n" + _cards(pop, lang)

    # pure smalltalk (koi vehicle/budget sawal nahi) -> sirf baat, vehicle push nahi
    if small and not has_intent:
        return small
    return (small + "\n\n" + veh).strip()


# ================================================================ chat UI
def _reply(question: str, df: pd.DataFrame, history=None) -> str:
    """ChatGPT first (full conversation context), built-in engine as fallback (never raises)."""
    ans = ask_openai(question, df, history)
    if ans:
        return ans
    try:
        return fallback_answer(question, df)
    except Exception:
        return "Sorry, something went wrong on my side — please try again 🙂"


_CHIPS = ["Hi 👋", "Best car under 15 lakh", "Cheapest bike", "Fastest vehicle"]

# cute robot avatar (gradient circle + white visor robot) - dock header ke liye
_AVATAR_SVG = (
    "<svg viewBox='0 0 64 64' width='42' height='42' xmlns='http://www.w3.org/2000/svg'>"
    "<defs>"
    "<linearGradient id='vbg' x1='0' y1='0' x2='1' y2='1'>"
    "<stop offset='0' stop-color='#a855f7'/><stop offset='.55' stop-color='#c026d3'/>"
    "<stop offset='1' stop-color='#ec4899'/></linearGradient>"
    "</defs>"
    "<circle cx='32' cy='32' r='30' fill='url(#vbg)'/>"
    "<circle cx='32' cy='32' r='30' fill='none' stroke='rgba(255,255,255,.25)' stroke-width='2'/>"
    # antenna
    "<line x1='32' y1='21' x2='32' y2='15' stroke='#fff' stroke-width='3' stroke-linecap='round'/>"
    "<circle cx='32' cy='13' r='2.8' fill='#fbbf24'/>"
    # headphone band + cups
    "<path d='M15 31 a17 17 0 0 1 34 0' stroke='#fff' stroke-width='4' fill='none'/>"
    "<rect x='10' y='29' width='7' height='13' rx='3.5' fill='#fff'/>"
    "<rect x='47' y='29' width='7' height='13' rx='3.5' fill='#fff'/>"
    # head
    "<rect x='18' y='22' width='28' height='25' rx='9' fill='#fff'/>"
    # visor
    "<rect x='22' y='27' width='20' height='13' rx='6.5' fill='#1e1b4b'/>"
    # eyes
    "<circle cx='28.5' cy='33.5' r='2.4' fill='#67e8f9'/>"
    "<circle cx='35.5' cy='33.5' r='2.4' fill='#67e8f9'/>"
    # mouth
    "<rect x='29' y='43' width='6' height='2.6' rx='1.3' fill='#c4b5fd'/>"
    "</svg>"
)


def _ask(text: str, df: pd.DataFrame):
    """User message -> answer -> history -> rerun (chat_input aur chips dono isko use karte hain)."""
    ss = st.session_state
    text = (text or "").strip()
    if not text:
        return
    hist = [dict(m) for m in ss.get("chat_hist", [])]  # context BEFORE this message
    ss.chat_hist.append({"role": "user", "content": text})
    with st.spinner("V-Bot is thinking..."):
        ans = _reply(text, df, hist)
    ss.chat_hist.append({"role": "assistant", "content": ans})
    st.rerun()


def render_chat(df: pd.DataFrame):
    """V-Bot corner dock (bottom-right, fixed panel).

    ChatGPT key ho to HAR baat ka jawab (koi bhi topic); na ho to built-in
    engine vehicles + smalltalk handle karta hai aur general sawal ka friendly
    jawab deta hai. Koi error nahi - har haal me jawab milta hai.
    Call once at the end of app.py.
    """
    ss = st.session_state
    ss.setdefault("chat_hist", [])
    gpt_on = bool(_key())

    # border=True + key: naya Streamlit container ko .st-key-vbot class deta hai
    # (CSS isi se corner me fix karta hai). Purane version par bina key fallback.
    try:
        dock = st.container(border=True, key="vbot")
    except TypeError:
        dock = st.container(border=True)
    with dock:
        hc, xc = st.columns([5, 1])
        with hc:
            status = (
                "🟢 ChatGPT ON · ask me anything, any topic"
                if gpt_on
                else "🟡 Fallback mode · vehicles + small talk"
            )
            st.markdown(
                f"<div class='vbot-head'>"
                f"<span class='vbot-badge'>{_AVATAR_SVG}</span>"
                f"<span class='vbot-info'><span class='vbot-title'>V-BOT</span>"
                f"<span class='vbot-status'>{status}</span></span>"
                f"</div>",
                unsafe_allow_html=True,
            )
        with xc:
            if st.button("🗑", key="vbot_clear", use_container_width=True):
                ss.chat_hist = []
                st.rerun()

        with st.container(height=330, border=False):
            if not ss.chat_hist:
                st.chat_message("assistant").markdown(
                    "Hello! 👋 **I'm V-Bot** — your vehicle & budget expert. "
                    "With ChatGPT ON, I can chat about *anything* — studies, jokes, "
                    "general knowledge, you name it!\n\n"
                    "Ask me below — pick a chip or just type ⬇️"
                )
            for m in ss.chat_hist:
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])

        chips = st.columns(4)
        for col, chip in zip(chips, _CHIPS):
            with col:
                if st.button(chip, key=f"chip_{chip}", use_container_width=True):
                    _ask(chip, df)

        q = st.chat_input("Type your question... (vehicles or anything else)")
        if q:
            _ask(q, df)
