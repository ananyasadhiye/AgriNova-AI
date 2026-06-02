import streamlit as st
import importlib
import traceback
from pathlib import Path

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AgriNova AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load CSS ──────────────────────────────────────────────────
css_path = Path("assets/background.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
  #MainMenu, footer, header { visibility: hidden; }
  [data-testid="stSidebar"]        { display: none !important; }
  [data-testid="collapsedControl"] { display: none !important; }
  .block-container {
    padding-top: 0 !important;
    max-width: 1320px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Feature registry ─────────────────────────────────────────
FEATURES = [
    {"key": "home",     "label": "Home",          "num": "—",  "icon": "⌂",  "module": None,
     "desc": "Overview & all tools"},
    {"key": "weather",  "label": "Weather",        "num": "01", "icon": "☁",  "module": "weather",
     "desc": "Hyper-local forecasts"},
    {"key": "mandi",    "label": "Mandi Prices",   "num": "02", "icon": "₹",  "module": "mandi",
     "desc": "Live crop market rates"},
    {"key": "disease",  "label": "Disease Scan",   "num": "03", "icon": "🍃", "module": "disease_ai",
     "desc": "Leaf photo diagnosis"},
    {"key": "soil",     "label": "Soil AI",        "num": "04", "icon": "◈",  "module": "soil_ai",
     "desc": "Nutrient-based crop match"},
    {"key": "crop",     "label": "Crop Match",     "num": "05", "icon": "✿",  "module": "crop_ai",
     "desc": "ML-powered recommendation"},
    {"key": "yield",    "label": "Yield Forecast", "num": "06", "icon": "▲",  "module": "yield_ai",
     "desc": "Harvest output prediction"},
    {"key": "price",    "label": "Price AI",       "num": "07", "icon": "⟁",  "module": "price_ai",
     "desc": "Tomorrow's mandi rate"},
    {"key": "voice",    "label": "Voice Out",      "num": "08", "icon": "♪",  "module": "voice",
     "desc": "Listen to AI answers"},
    {"key": "vsearch",  "label": "Voice Search",   "num": "09", "icon": "◉",  "module": "voice_search",
     "desc": "Speak your question"},
    {"key": "chat",     "label": "AI Chat",        "num": "10", "icon": "⊹",  "module": "ai_chat",
     "desc": "Farm advisor chat"},
    {"key": "language", "label": "Language",       "num": "11", "icon": "✱",  "module": "language",
     "desc": "Switch interface language"},
]

if "active" not in st.session_state:
    st.session_state.active = "home"

# ── NAVBAR ────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="nav-brand">
    <div class="nav-logo">A</div>
    <div>
      <div class="nav-title">AgriNova AI</div>
      <div class="nav-tagline">Field Intelligence Platform</div>
    </div>
  </div>
  <div class="nav-pill">Kharif 2026 · Live</div>
</div>
""", unsafe_allow_html=True)

# ── TAB NAV ───────────────────────────────────────────────────
tab_cols = st.columns(len(FEATURES))
for i, f in enumerate(FEATURES):
    with tab_cols[i]:
        is_active = st.session_state.active == f["key"]
        if st.button(f["label"], key=f"tab_{f['key']}",
                     use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.active = f["key"]
            st.rerun()

st.markdown('<div style="height:1px;background:rgba(255,220,160,0.07);margin:0 0 32px"></div>',
            unsafe_allow_html=True)

# ── SAFE MODULE LOADER ────────────────────────────────────────
def load_module(module_name: str):
    try:
        mod = importlib.import_module(f"modules.{module_name}")
        importlib.reload(mod)
        if hasattr(mod, "run") and callable(mod.run):
            mod.run()
        else:
            st.error(f"Module **{module_name}** has no `run()` function.")
    except ModuleNotFoundError as e:
        if module_name not in str(e):
            st.error(f"Missing package in **{module_name}**: `{e}`")
            pkg = str(e).split("'")[1]
            st.code(f"pip install {pkg}", language="bash")
        else:
            st.error(f"Module file not found: `modules/{module_name}.py`")
    except Exception:
        st.error(f"Error in module **{module_name}**:")
        st.code(traceback.format_exc(), language="python")

def render_module(feat):
    st.markdown(f"""
    <div class="mod-header">
      <div>
        <div class="mod-eyebrow">Module {feat['num']}</div>
        <div class="mod-title">{feat['label']}</div>
        <div class="mod-sub" style="margin-top:10px">{feat['desc']}</div>
      </div>
      <div class="mod-num">{feat['num']}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    load_module(feat["module"])
    st.markdown('</div>', unsafe_allow_html=True)

# ── HOME PAGE ─────────────────────────────────────────────────
def render_home():
    st.markdown("""
    <div class="hero">
      <div>
        <div class="hero-kicker">Season 2026 · Kharif Intelligence</div>
        <h1 class="hero-h1">
          Grow with<br/>
          <em>data,</em> not <span class="glow">guesswork.</span>
        </h1>
        <p class="hero-body">
          Eleven precision tools — disease detection, soil analysis, live mandi prices,
          yield forecasting, and voice assistance — unified in one workspace built
          for the working farmer.
        </p>
      </div>
      <div class="hero-stats">
        <div class="hero-stat"><div class="hs-num">11</div><div class="hs-label">AI Modules</div></div>
        <div class="hero-stat"><div class="hs-num">24/7</div><div class="hs-label">Live Data</div></div>
        <div class="hero-stat"><div class="hs-num">99%</div><div class="hs-label">Disease Acc.</div></div>
        <div class="hero-stat"><div class="hs-num">6+</div><div class="hs-label">Languages</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tools = [f for f in FEATURES if f["key"] != "home"]
    st.markdown('<div class="grid-label">All Modules — 11 Tools</div>', unsafe_allow_html=True)

    rows = [tools[i:i+4] for i in range(0, len(tools), 4)]
    for row in rows:
        cols = st.columns(4)
        for col, feat in zip(cols, row):
            with col:
                st.markdown(f"""
                <div class="fcard">
                  <div class="fcard-top">
                    <span class="fcard-num">{feat['num']}</span>
                    <span class="fcard-ico">{feat['icon']}</span>
                  </div>
                  <div class="fcard-name">{feat['label']}</div>
                  <div class="fcard-desc">{feat['desc']}</div>
                  <div class="fcard-arrow">Open →</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Open {feat['label']}", key=f"open_{feat['key']}",
                             use_container_width=True):
                    st.session_state.active = feat["key"]
                    st.rerun()

# ── ROUTER ────────────────────────────────────────────────────
active = st.session_state.active
if active == "home":
    render_home()
else:
    feat = next((f for f in FEATURES if f["key"] == active), None)
    if feat and feat["module"]:
        render_module(feat)

# ── FOOTER ────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <span>AgriNova AI · Field Intelligence Platform</span>
  <div class="footer-dot"></div>
  <span>Built for India's Farmers · 2026</span>
  <div class="footer-dot"></div>
  <span>v3.0 · Terra Moderna</span>
</div>
""", unsafe_allow_html=True)
