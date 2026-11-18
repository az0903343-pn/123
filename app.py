"""
Vehicle Budget Advisor - wizard style Streamlit app.

Flow: Step 1 choose vehicle type (photo cards) -> Step 2 set budget ->
Step 3 see matching vehicles (photo cards) -> click a card for full details
(price, modifications, pros/cons) with a direct Buy-on-PakWheels link.
"""
import pandas as pd
import plotly.express as px
import streamlit as st

import urllib.parse

import ai
import images
import ml

st.set_page_config(page_title="Vehicle Budget Advisor", page_icon="🚗", layout="wide")

# ---------------------------------------------------------------- data
@st.cache_data
def load_df():
    df = pd.read_csv("vehicles.csv")
    df["price_pkr"] = df["price_pkr"].astype(float)
    df["seats"] = df["seats"].astype(int)
    df["top_speed_kmh"] = df["top_speed_kmh"].astype(int)
    return df


@st.cache_resource
def get_model():
    """Train once per session (uses model.joblib if present, else trains from CSV)."""
    return ml.ensure_model(DF)


DF = load_df()
MODEL = get_model()

CATEGORIES = [
    "Car", "Van", "Bus/Truck", "Tractor", "Rickshaw", "Petrol Bike",
    "Scooter", "Electric Bike", "Cycle", "Heavy Bike", "Boat",
    "Helicopter", "Aircraft", "Jet",
]
EMOJI = {
    "Car": "🚗", "Van": "🚐", "Bus/Truck": "🚌", "Tractor": "🚜", "Rickshaw": "🛺",
    "Petrol Bike": "🏍️", "Heavy Bike": "🏍️", "Scooter": "🛵", "Electric Bike": "⚡",
    "Cycle": "🚲", "Boat": "🚤", "Helicopter": "🚁", "Aircraft": "✈️", "Jet": "🛩️",
}
TAGLINE = {
    "Car": "Family & style", "Van": "Business & travel", "Bus/Truck": "Karobar",
    "Tractor": "Kheti ka kaam", "Rickshaw": "Roz ki kamai", "Petrol Bike": "Roz ka sath",
    "Scooter": "Asaan ride", "Electric Bike": "Petrol zero", "Cycle": "Fitness & fun",
    "Heavy Bike": "Speed & style", "Boat": "Paani par masti", "Helicopter": "Aasman ka safar",
    "Aircraft": "Udne ka maza", "Jet": "Luxury ka king",
}
PRESETS = [
    ("5 Lakh", 500_000), ("10 Lakh", 1_000_000), ("25 Lakh", 2_500_000),
    ("50 Lakh", 5_000_000), ("1 Crore", 10_000_000), ("2 Crore", 20_000_000),
    ("5 Crore", 50_000_000), ("10 Crore", 100_000_000),
]

# ---------------------------------------------------------------- CSS
st.markdown(
    """
    <style>
    :root { --g:#22c55e; --gl:#4ade80; --pale:#86efac; --mut:#9db2a4; }
    html, body, [data-testid="stAppViewContainer"] {
        background: #030503 !important;
        color: #eef5ee;
    }
    [data-testid="stAppViewContainer"]::before {
        content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
        background:
            radial-gradient(900px 430px at 50% -6%, rgba(34,197,94,.17), transparent 65%),
            radial-gradient(700px 400px at 88% 18%, rgba(34,197,94,.07), transparent 60%),
            radial-gradient(620px 380px at 8% 32%, rgba(34,197,94,.05), transparent 60%);
    }
    [data-testid="stAppViewContainer"]::after {
        content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0; opacity: .55;
        background-image:
            linear-gradient(rgba(134,239,172,.045) 1px, transparent 1px),
            linear-gradient(90deg, rgba(134,239,172,.045) 1px, transparent 1px);
        background-size: 58px 58px;
        -webkit-mask-image: radial-gradient(ellipse at 50% 0%, #000 0%, transparent 72%);
        mask-image: radial-gradient(ellipse at 50% 0%, #000 0%, transparent 72%);
    }
    section[data-testid="stSidebar"] { display: none; }
    div.block-container { padding-top: 1.2rem; max-width: 1150px; position: relative; z-index: 1;
        padding-bottom: 560px; }

    /* ---- navbar ---- */
    .nav { display: flex; align-items: center; gap: 6px; background: rgba(9,12,9,.85);
        border: 1px solid rgba(255,255,255,.09); border-radius: 16px; padding: 9px 14px;
        margin: 2px auto 8px; backdrop-filter: blur(12px); width: fit-content;
        max-width: 100%; box-shadow: 0 10px 40px rgba(0,0,0,.5); }
    .nav .logo { font-weight: 800; font-size: 1.05rem; color: #fff; letter-spacing: -.3px; margin-right: 10px; }
    .nav .logo b { color: var(--gl); }
    .nav .lk { color: #9db2a4; font-size: .78rem; padding: 6px 11px; border-radius: 999px; font-weight: 600; }
    .nav .lk.on { color: #fff; background: rgba(34,197,94,.16); }
    .nav .sp { flex: 0 0 12px; }
    .nav .cta { background: #fff; color: #04180a; font-weight: 700; font-size: .78rem;
        padding: 7px 14px; border-radius: 999px; }
    .nav .gh { border: 1px solid rgba(255,255,255,.22); color: #fff; font-weight: 600;
        font-size: .78rem; padding: 7px 14px; border-radius: 999px; }

    /* ---- hero ---- */
    .hero { text-align: center; padding: 34px 0 10px; }
    .hero .kicker { color: #9db2a4; font-size: .8rem; letter-spacing: .8px; margin-bottom: 16px; }
    .hero .kicker b { color: var(--gl); font-weight: 600; }
    .hero h1 { font-size: clamp(2.2rem, 5vw, 3.5rem); font-weight: 800; line-height: 1.08;
        letter-spacing: -1px; color: #fff; margin: 0; }
    .hero h1 .gg { background: linear-gradient(90deg, #a7f3c0, #22c55e);
        -webkit-background-clip: text; background-clip: text; color: transparent; }
    .hero .sub { color: #9db2a4; margin-top: 14px; font-size: .95rem; }
    .hero .cta-row { display: flex; gap: 10px; justify-content: center; margin-top: 24px; flex-wrap: wrap; }
    .btn-white { display: inline-block; background: #fff; color: #04180a; font-weight: 700;
        font-size: .85rem; padding: 10px 22px; border-radius: 999px; }
    .btn-ghost { display: inline-block; border: 1px solid rgba(255,255,255,.22); color: #fff;
        font-weight: 600; font-size: .85rem; padding: 10px 22px; border-radius: 999px; }

    /* ---- step label (bracket style) ---- */
    .stepchip { font-family: ui-monospace, "Cascadia Mono", monospace; color: #9db2a4;
        font-size: .8rem; letter-spacing: .8px; margin-bottom: 16px; }
    .stepchip b { color: var(--gl); font-weight: 600; }

    .cat-card, .veh-card { background: rgba(255,255,255,.035);
        border: 1px solid rgba(255,255,255,.08); border-radius: 16px;
        overflow: hidden; backdrop-filter: blur(10px); height: 100%;
        transition: transform .3s ease, border-color .3s ease, box-shadow .3s ease; }
    .cat-card:hover, .veh-card:hover { transform: translateY(-6px);
        border-color: rgba(134,239,172,.45);
        box-shadow: 0 0 0 1px rgba(34,197,94,.22), 0 20px 55px rgba(34,197,94,.12), 0 20px 55px rgba(0,0,0,.6); }
    .pimg { position: relative; height: 150px; overflow: hidden; background: rgba(255,255,255,.04); }
    .veh-card .pimg { height: 140px; }
    .pimg img { width: 100%; height: 100%; object-fit: cover; transition: transform .5s ease;
        filter: saturate(.92); }
    .cat-card:hover .pimg img, .veh-card:hover .pimg img { transform: scale(1.09); filter: saturate(1.05); }
    .pimg .tag { position: absolute; left: 10px; bottom: 9px; font-weight: 700; color: #fff;
        font-size: .95rem; text-shadow: 0 2px 8px rgba(0,0,0,.95); }
    .pimg .ic { position: absolute; top: 9px; right: 9px; width: 34px; height: 34px;
        display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
        background: rgba(3,5,3,.72); border: 1px solid rgba(134,239,172,.25); border-radius: 50%;
        backdrop-filter: blur(4px); }
    .cat-card .csub { padding: 10px 13px 4px; color: #9db2a4; font-size: .78rem; text-align: center; }
    .veh-card .vname { padding: 9px 13px 0; font-weight: 700; color: #fff; font-size: .95rem; line-height: 1.3; }
    .veh-card .vprice { padding: 4px 13px 0; font-size: 1.02rem; font-weight: 800; color: var(--pale); }
    .veh-card .vmeta { padding: 2px 13px 9px; color: #9db2a4; font-size: .74rem; line-height: 1.55; }
    .vbtn { padding: 0 10px 11px; }

    .detail { background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.09);
        border-radius: 18px; padding: 18px 20px; backdrop-filter: blur(10px); }
    .detail.glow { border-color: rgba(134,239,172,.28);
        box-shadow: 0 0 60px rgba(34,197,94,.10) inset, 0 18px 50px rgba(0,0,0,.5); }
    .detail .dprice { font-size: 1.9rem; font-weight: 800; color: var(--pale); }
    .pill { display: inline-block; font-family: ui-monospace, monospace; font-size: .68rem;
        padding: 3px 11px; border-radius: 999px; background: rgba(34,197,94,.10);
        border: 1px solid rgba(134,239,172,.28); color: #b9e6c4; margin: 2px 4px 2px 0;
        letter-spacing: .4px; }
    .sect { font-weight: 700; margin: 14px 0 6px; font-size: 1.0rem; color: #fff; }
    .sect .mono { font-family: ui-monospace, monospace; font-size: .68rem; color: #9db2a4; letter-spacing: .6px; }
    .li { display: flex; gap: 8px; padding: 5px 0; line-height: 1.5; font-size: .92rem; color: #cfe0d2; }
    .hintbox { background: rgba(34,197,94,.08); border: 1px solid rgba(134,239,172,.3);
        color: #cde9d4; border-radius: 14px; padding: 12px 16px; font-size: .9rem; }
    a[data-testid="stLinkButton"], a[data-testid="stLinkButton"] p { font-weight: 800 !important; }
    div[data-testid="stButton"] > button { border-radius: 999px; font-weight: 700;
        background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.15); color: #fff; }
    div[data-testid="stButton"] > button:hover { border-color: rgba(134,239,172,.45); }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: #fff !important; border: none !important;
        box-shadow: 0 8px 30px rgba(255,255,255,.12); }
    div[data-testid="stButton"] > button[kind="primary"] * { color: #04180a !important; }
    a[data-testid="stLinkButton"] { background: #fff !important; border: none !important; }
    a[data-testid="stLinkButton"] * { color: #04180a !important; }
    div[data-testid="stAlert"] { background: rgba(34,197,94,.08) !important;
        border: 1px solid rgba(134,239,172,.28) !important; color: #d7f0dd !important; border-radius: 12px; }
    .stExpander { border: 1px solid rgba(255,255,255,.09) !important; border-radius: 14px !important; }

    /* ---- multi-platform links ---- */
    .plat { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
    .plat a { display: inline-block; font-size: .76rem; font-weight: 700; text-decoration: none;
        padding: 8px 15px; border-radius: 999px; border: 1px solid rgba(134,239,172,.35);
        color: #d7f0dd; background: rgba(34,197,94,.07); transition: all .25s ease; }
    .plat a:hover { background: rgba(34,197,94,.22); border-color: rgba(134,239,172,.7);
        color: #fff; transform: translateY(-2px); }
    .plat a.pw { background: #fff; border-color: #fff; color: #04180a; }
    .plat a.pw:hover { background: var(--pale); border-color: var(--pale); color: #04180a; }
    .plat .cap { width: 100%; font-family: ui-monospace, monospace; font-size: .68rem;
        color: #9db2a4; letter-spacing: .6px; margin-bottom: 2px; }

    /* ---- AI chat (ChatGPT) ---- */
    [data-testid="stChatMessage"] { background: rgba(255,255,255,.035) !important;
        border: 1px solid rgba(255,255,255,.09) !important; border-radius: 14px !important;
        padding: 6px 8px !important; }
    [data-testid="stChatInput"] { background: rgba(255,255,255,.06) !important;
        border: 1px solid rgba(134,239,172,.3) !important; border-radius: 999px !important; }
    [data-testid="stChatInput"] textarea { color: #eef5ee !important; }
    [data-testid="stChatInput"]::placeholder { color: #6f8274 !important; }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p { font-size: .92rem; }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] a { color: #86efac !important; }
    [data-testid="stChatInputSubmitButton"] button { background: linear-gradient(135deg, #16a34a, #4ade80) !important; }

    /* ---- corner chat dock (V-Bot, bottom-right) ---- */
    div[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stChatInput"]) {
        position: fixed; bottom: 14px; right: 14px; z-index: 99999;
        width: 400px; max-width: calc(100vw - 24px);
        background: rgba(5,8,5,.97) !important;
        border: 1px solid rgba(134,239,172,.32) !important;
        border-radius: 18px !important;
        box-shadow: 0 24px 60px rgba(0,0,0,.65), 0 0 40px rgba(34,197,94,.12);
        padding: 12px 14px 12px !important;
        backdrop-filter: blur(10px);
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stChatInput"]) [data-testid="stButton"] > button {
        font-size: .68rem !important; padding: 5px 8px !important; border-radius: 999px !important;
        background: rgba(34,197,94,.12) !important; border: 1px solid rgba(134,239,172,.3) !important;
        color: #b9e6c4 !important; font-weight: 700;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stChatInput"]) [data-testid="stButton"] > button:hover {
        background: rgba(34,197,94,.28) !important; color: #fff !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stChatInput"]) [data-testid="stChatMessage"] {
        background: rgba(255,255,255,.04) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# navbar (decorative, Forology style)
st.markdown(
    """
    <div class='nav'>
      <span class='logo'>V<b>hology</b></span>
      <span class='lk on'>Home</span><span class='lk'>How It Works</span>
      <span class='lk'>Vehicles</span><span class='lk'>Support</span>
      <span class='sp'></span>
      <span class='gh'>&#127760; English &#9662;</span>
      <span class='cta'>&#128640; Start</span>
      <span class='gh'>PakWheels &#8599;</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- state
ss = st.session_state
ss.setdefault("step", "cat")
ss.setdefault("cat", None)
ss.setdefault("budget", 5_000_000)
ss.setdefault("sel", None)


def go(step):
    ss.step = step
    st.rerun()


def photo_card(html_cls, img, title, inner="", icon=""):
    if img:
        small, big = images.pair_for_url(img)
        big = big.replace("'", "%27")
        img_html = (
            f"<img src='{small}' alt='' loading='lazy' "
            f"onerror=\"this.onerror=null;this.src='{big}'\">"
        )
    else:
        img_html = ""
    return (
        f"<div class='{html_cls}'>"
        f"<div class='pimg'>{img_html}"
        f"<span class='tag'>{title}</span>"
        + (f"<span class='ic'>{icon}</span>" if icon else "")
        + "</div>" + inner + "</div>"
    )


# ================================================================= STEP 1
if ss.step == "cat":
    st.markdown(
        "<div class='hero'>"
        "<div class='kicker'>[ Our Data <b>&middot;</b> Your Success ]</div>"
        "<h1>No Budget Limit<br>Conquer the <span class='gg'>road</span></h1>"
        f"<div class='sub'>{len(DF):,} vehicles &middot; {len(CATEGORIES)} categories &middot; Pakistan ki har cheez "
        "cycles se le kar private jets tak &mdash; neeche se choose karein &#8595;</div>"
        "<div class='cta-row'><span class='btn-white'>&#128640; Start a challenge</span>"
        "<span class='btn-ghost'>Scroll to explore &#8595;</span></div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='stepchip'>[ <b>STEP 1</b> ] &middot; Vehicle type select karein</div>", unsafe_allow_html=True)

    cols_per_row = 4
    for i in range(0, len(CATEGORIES), cols_per_row):
        chunk = CATEGORIES[i : i + cols_per_row]
        cols = st.columns(cols_per_row)
        for col, cat in zip(cols, chunk):
            img = images.CATEGORY_IMAGES.get(cat, "")
            n = int((DF["category"] == cat).sum())
            inner = f"<div class='csub'>{TAGLINE[cat]} · {n} options</div>"
            with col:
                st.markdown(photo_card("cat-card", img, f"{EMOJI[cat]} {cat}", inner), unsafe_allow_html=True)
                st.markdown("<div class='vbtn'>", unsafe_allow_html=True)
                if st.button("Select ▸", key=f"cat_{cat}", use_container_width=True):
                    ss.cat = cat
                    ss.budget = 5_000_000  # reset budget for the new category
                    if "budget_slider" in ss:
                        del ss["budget_slider"]
                    go("budget")
                st.markdown("</div>", unsafe_allow_html=True)

# ================================================================= STEP 2
elif ss.step == "budget":
    cat = ss.cat
    cat_df = DF[DF["category"] == cat]
    lo = max(int(cat_df["price_pkr"].min() * 0.6) // 10_000 * 10_000, 50_000)
    hi = max(int(cat_df["price_pkr"].max() * 1.2) // 10_000 * 10_000, 1_000_000)

    st.markdown("<div class='stepchip'>[ <b>STEP 2</b> ] &middot; Budget set karein</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='hintbox'>Aap ne <b>{EMOJI[cat]} {cat}</b> select kiya hai · "
        f"{len(cat_df)} options available</div>",
        unsafe_allow_html=True,
    )
    st.write("")

    st.slider("Aap ka budget (PKR)", min_value=lo, max_value=hi,
              value=min(max(ss.budget, lo), hi),
              step=max(10_000, (hi - lo) // 600 // 10_000 * 10_000),
              format="%d", key="budget_slider")

    st.write("Ya koi preset choose karein:")
    pcols = st.columns(len(PRESETS))
    for col, (label, amount) in zip(pcols, PRESETS):
        with col:
            if st.button(label, key=f"pre_{label}", use_container_width=True):
                ss.budget = min(amount, hi)  # clamp to this category's range
                ss.budget_slider = ss.budget  # keep the slider in sync
                go("budget")
    if ss.budget_slider != ss.budget:
        ss.budget = ss.budget_slider

    st.write("")
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("↩ Wapas vehicle type", use_container_width=True):
            go("cat")
    with c2:
        if st.button("🚀 Show me my options", type="primary", use_container_width=True):
            go("results")

# ================================================================= STEP 3
elif ss.step == "results":
    cat, budget = ss.cat, ss.budget
    st.markdown(
        f"<div class='stepchip'>[ <b>STEP 3</b> ] &middot; {EMOJI[cat]} {cat} &middot; budget "
        f"<b>{ml.money(budget)}</b></div>",
        unsafe_allow_html=True,
    )

    res = DF[(DF["category"] == cat) & (DF["price_pkr"] <= budget)].sort_values("price_pkr", ascending=False)
    st.caption(f"🎯 {len(res)} vehicles aap ke budget me fit ho rahi hain")

    if res.empty:
        alt = DF[DF["category"] == cat].sort_values("price_pkr").head(3)
        st.markdown(
            "<div class='hintbox'>😕 Is budget me ye category fit nahi hoti. "
            "Budget thora barhayein ya neeche sab se sasti options dekhein 👇</div>",
            unsafe_allow_html=True,
        )
        res = alt

    shown = res.head(12)
    for i in range(0, len(shown), 3):
        chunk = shown.iloc[i : i + 3]
        cols = st.columns(3)
        for col, (_, row) in zip(cols, chunk.iterrows()):
            img = images.image_for(row["name"], row["category"])
            inner = (
                f"<div class='vname'>{row['name']}</div>"
                f"<div class='vprice'>{ml.money(row['price_pkr'])}</div>"
                f"<div class='vmeta'>⛽ {row['fuel_type']} · 🪑 {row['seats']} seats · "
                f"⚡ {row['top_speed_kmh']} km/h</div>"
            )
            with col:
                st.markdown(photo_card("veh-card", img, row["brand"], inner, icon=EMOJI[row["category"]]), unsafe_allow_html=True)
                st.markdown("<div class='vbtn'>", unsafe_allow_html=True)
                if st.button("🔍 View Details", key=f"det_{row['name']}", use_container_width=True):
                    ss.sel = row["name"]
                    go("detail")
                st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("↩ Budget change karein", use_container_width=True):
            go("budget")
    with b2:
        if st.button("🏠 Vehicle type change karein", use_container_width=True):
            go("cat")

    # budget breakdown chart
    if not res.empty and len(res) > 1:
        with st.expander("📊 Budget breakdown — kin kin par kharch ho sakta hai", expanded=False):
            top = res.head(8).copy()
            fig = px.bar(
                top, x="name", y="price_pkr", color="price_pkr",
                color_continuous_scale="Greens",
                labels={"name": "Vehicle", "price_pkr": "Price (PKR)"},
            )
            fig.add_hline(y=budget, line_dash="dot", line_color="#86efac",
                          annotation_text="Aap ka budget")
            fig.update_layout(height=380, showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)", font_color="#9db2a4",
                              xaxis_tickangle=-25)
            st.plotly_chart(fig, use_container_width=True)

# ================================================================= DETAIL
elif ss.step == "detail":
    row = DF[DF["name"] == ss.sel].iloc[0]
    img = images.image_for(row["name"], row["category"])
    pros = ml.split_list(row["features_good"])
    cons = ml.split_list(row["features_bad"])
    mods = ml.split_list(row["mods"])

    st.markdown(
        f"<div class='detail glow'>"
        f"<span class='pill'>{EMOJI[row['category']]} {row['category']}</span>"
        f"<span class='pill'>🏷 {row['brand']}</span>"
        f"<span class='pill'>⛽ {row['fuel_type']}</span>"
        f"<span class='pill'>🪑 {row['seats']} seats</span>"
        f"<span class='pill'>⚡ {row['top_speed_kmh']} km/h top speed</span>"
        f"<h1 style='margin:10px 0 4px'>{row['name']}</h1>"
        f"<div class='dprice'>{ml.money(row['price_pkr'])}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.write("")
    lc, rc = st.columns([1.1, 1])
    with lc:
        if img:
            st.image(img, use_container_width=True)
        st.write("")
        st.link_button("🛒 Buy on PakWheels — Live prices dekhein", row["pakwheels_url"], use_container_width=True)

        # multi-platform links (computed live per vehicle - har platform ka data)
        q = urllib.parse.quote_plus(row["name"])
        st.markdown(
            "<div class='plat'>"
            "<span class='cap'>[ MORE PLATFORMS ] &middot; is vehicle ko aur jagah dhoondein</span>"
            f"<a href='https://www.olx.com.pk/items/q-{q}' target='_blank'>OLX Pakistan &#8599;</a>"
            f"<a href='https://www.cardekho.com/search?q={q}' target='_blank'>CarDekho &#8599;</a>"
            f"<a href='https://www.google.com/search?q={q}+price+in+Pakistan' target='_blank'>Google Prices &#8599;</a>"
            f"<a href='https://www.google.com/search?tbm=isch&q={q}' target='_blank'>Images &#8599;</a>"
            "</div>",
            unsafe_allow_html=True,
        )
    with rc:
        st.markdown("<div class='detail'>", unsafe_allow_html=True)
        st.markdown("<div class='sect'>✅ Faide <span class='mono'>[ PROS ]</span></div>", unsafe_allow_html=True)
        for p in pros:
            st.markdown(f"<div class='li'>✔️ <span>{p}</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='sect'>❌ Nuqsan <span class='mono'>[ CONS ]</span></div>", unsafe_allow_html=True)
        for c_ in cons:
            st.markdown(f"<div class='li'>✖️ <span>{c_}</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='sect'>🛠️ Modifications <span class='mono'>[ MODS ]</span></div>", unsafe_allow_html=True)
        for m_ in mods:
            st.markdown(f"<div class='li'>🔧 <span>{m_}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # AI price estimate + similar vehicles (ML part)
    est = ml.predict_price(MODEL, row["category"], row["brand"], row["fuel_type"], row["seats"], row["top_speed_kmh"])
    sim = ml.similar(DF, row["name"], 4)
    st.write("")
    with st.expander("🤖 ML insights — price estimate & similar vehicles", expanded=False):
        diff_pct = (row["price_pkr"] - est) / est * 100
        verdict = "list price theek hai" if abs(diff_pct) < 12 else ("list price thori zyada lagti hai" if diff_pct > 0 else "ye kaafi reasonable price hai")
        st.info(f"**Random Forest estimate:** {ml.money(est)} — is list price se **{abs(diff_pct):.0f}% {'zyada' if diff_pct>0 else 'kam'}** ({verdict})")
        if not sim.empty:
            st.dataframe(sim, use_container_width=True, hide_index=True)

    st.write("")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("↩ Wapas results par", use_container_width=True):
            go("results")
    with b2:
        if st.button("🏠 Naya search shuru karein", use_container_width=True):
            go("cat")

# ---------------------------------------------------------------- AI chat (corner dock)
ai.render_chat(DF)
