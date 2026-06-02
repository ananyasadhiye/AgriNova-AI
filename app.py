import streamlit as st
import importlib
import runpy
import traceback
from pathlib import Path

# -------------------------------------------------------------------
# Page config — sidebar collapsed (we use a custom top nav instead)
# -------------------------------------------------------------------
st.set_page_config(
    page_title="AgriNova AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------------------------------------------------
# Load global CSS
# -------------------------------------------------------------------
css_path = Path("assets/background.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
      #MainMenu, footer, header {visibility: hidden;}
      [data-testid="stSidebar"] {display: none;}
      [data-testid="collapsedControl"] {display: none;}
      .block-container {padding-top: 1.2rem; max-width: 1280px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------
# Feature registry (11 modules)
# key       -> session key
# module    -> filename in modules/  (without .py)
# -------------------------------------------------------------------
FEATURES = [
    {"key": "home",     "label": "Home",       "tag": "00", "icon": "✦", "module": None},
    {"key": "weather",  "label": "Weather",    "tag": "01", "icon": "☁", "module": "weather"},
    {"key": "mandi",    "label": "Mandi",      "tag": "02", "icon": "₹", "module": "mandi"},
    {"key": "disease",  "label": "Disease",    "tag": "03", "icon": "🍃", "module": "disease_ai"},
    {"key": "soil",     "label": "Soil AI",    "tag": "04", "icon": "◐", "module": "soil_ai"},
    {"key": "crop",     "label": "Crop Match", "tag": "05", "icon": "✿", "module": "crop_ai"},
    {"key": "yield",    "label": "Yield",      "tag": "06", "icon": "▲", "module": "yield_ai"},
    {"key": "price",    "label": "Price",      "tag": "07", "icon": "$", "module": "price_ai"},
    {"key": "voice",    "label": "Voice Out",  "tag": "08", "icon": "♪", "module": "voice"},
    {"key": "vsearch",  "label": "Voice Ask",  "tag": "09", "icon": "◉", "module": "voice_search"},
    {"key": "chat",     "label": "AI Chat",    "tag": "10", "icon": "✺", "module": "ai_chat"},
    {"key": "language", "label": "Language",   "tag": "11", "icon": "✱", "module": "language"},
]

if "active" not in st.session_state:
    st.session_state.active = "home"

# -------------------------------------------------------------------
# Top nav bar
# -------------------------------------------------------------------
st.markdown(
    """
    <div class="topbar">
      <div class="brand">
        <div class="brand-mark">◈</div>
        <div class="brand-text">
          <div class="brand-name">AgriNova</div>
          <div class="brand-sub">AI · FIELD INTELLIGENCE</div>
        </div>
      </div>
      <div class="brand-meta">v2.0 — DARK ORGANIC</div>
    </div>
    """,
    unsafe_allow_html=True,
)

nav_cols = st.columns(len(FEATURES))
for i, f in enumerate(FEATURES):
    with nav_cols[i]:
        is_active = st.session_state.active == f["key"]
        label = f"{f['icon']}  {f['label']}"
        if st.button(label, key=f"nav_{f['key']}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.active = f["key"]
            st.rerun()

st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

# -------------------------------------------------------------------
# Home
# -------------------------------------------------------------------
def render_home():
    st.markdown(
        """
        <section class="hero">
          <div class="hero-tag">SEASON 26 · KHARIF INDEX</div>
          <h1 class="hero-title">
            Grow <em>smarter</em>.<br/>
            Decide <span class="accent">in seconds</span>.
          </h1>
          <p class="hero-sub">
            Eleven AI tools — weather, soil, disease, market and voice — woven
            into one quiet workspace built for working farmers.
          </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    cards = [f for f in FEATURES if f["key"] != "home"]
    rows = [cards[i:i + 4] for i in range(0, len(cards), 4)]
    for row in rows:
        cols = st.columns(4)
        for c, f in zip(cols, row):
            with c:
                st.markdown(
                    f"""
                    <div class="feature-card">
                      <div class="fc-top">
                        <span class="fc-tag">{f['tag']}</span>
                        <span class="fc-icon">{f['icon']}</span>
                      </div>
                      <div class="fc-title">{f['label']}</div>
                      <div class="fc-desc">Open module →</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"Open {f['label']}", key=f"open_{f['key']}", use_container_width=True):
                    st.session_state.active = f["key"]
                    st.rerun()

    st.markdown(
        """
        <div class="stat-strip">
          <div class="stat"><div class="stat-num">11</div><div class="stat-lab">AI MODULES</div></div>
          <div class="stat"><div class="stat-num">24/7</div><div class="stat-lab">LIVE FORECASTS</div></div>
          <div class="stat"><div class="stat-num">99%</div><div class="stat-lab">DISEASE ACCURACY</div></div>
          <div class="stat"><div class="stat-num">12+</div><div class="stat-lab">LANGUAGES</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------------------------------------------
# Safe module loader — handles BOTH styles:
#   (a) module exposes a run() function
#   (b) module is a plain Streamlit script with top-level code
# -------------------------------------------------------------------
def load_module(module_name: str):
    """
    Try to import modules.<module_name>. If it has run(), call it.
    Otherwise execute the file as a script via runpy so its top-level
    Streamlit code renders inside the current page.
    """
    # 1) Try import + run()
    try:
        mod = importlib.import_module(f"modules.{module_name}")
        importlib.reload(mod)  # pick up edits during dev
        if hasattr(mod, "run") and callable(mod.run):
            mod.run()
            return
    except ModuleNotFoundError as e:
        # Only swallow if it's the module file itself missing
        if module_name not in str(e):
            st.error(f"Missing dependency while loading **{module_name}**: `{e}`")
            st.caption("Install the missing package and reload.")
            return
        # else fall through to script-mode
    except Exception:
        st.error(f"Error inside module **{module_name}**:")
        st.code(traceback.format_exc(), language="python")
        return

    # 2) Fallback: run as a script
    script_path = Path("modules") / f"{module_name}.py"
    if not script_path.exists():
        st.error(f"Module file not found: `{script_path}`")
        st.caption("Make sure the file exists inside the `modules/` folder.")
        return

    try:
        runpy.run_path(str(script_path), run_name="__main__")
    except Exception:
        st.error(f"Error while running **{module_name}.py**:")
        st.code(traceback.format_exc(), language="python")

# -------------------------------------------------------------------
# Section wrapper
# -------------------------------------------------------------------
def section(title, subtitle, module_name):
    st.markdown(
        f"""
        <div class="section-head">
          <div class="section-tag">MODULE</div>
          <h2 class="section-title">{title}</h2>
          <p class="section-sub">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    load_module(module_name)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------------
# Router
# -------------------------------------------------------------------
SUBTITLES = {
    "weather":  "Hyper-local forecast for any city.",
    "mandi":    "Live crop prices across markets.",
    "disease":  "Upload a leaf — diagnose in seconds.",
    "soil":     "N · P · K · pH · rainfall analysis.",
    "crop":     "Best-fit crop for your field.",
    "yield":    "Forecast your harvest output.",
    "price":    "Tomorrow's mandi rate, today.",
    "voice":    "Listen to AgriNova's answers.",
    "vsearch":  "Speak your question, get a reply.",
    "chat":     "Conversational farm advisor.",
    "language": "Switch interface language.",
}

active = st.session_state.active
if active == "home":
    render_home()
else:
    feat = next((f for f in FEATURES if f["key"] == active), None)
    if feat and feat["module"]:
        section(feat["label"], SUBTITLES.get(active, ""), feat["module"])

# -------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
      <div>AGRINOVA AI · BUILT FOR THE FIELD</div>
      <div>© 2026 · Crafted with care</div>
    </div>
    """,
    unsafe_allow_html=True,
)
