import streamlit as st
import numpy as np
import os

CROP_RULES = {
    "Rice":        {"n":(60,120), "p":(30,60),  "k":(30,60),  "ph":(5.5,7.0), "rain":(150,300)},
    "Wheat":       {"n":(50,100), "p":(40,80),  "k":(30,60),  "ph":(6.0,7.5), "rain":(60,150)},
    "Maize":       {"n":(70,120), "p":(40,70),  "k":(40,80),  "ph":(5.8,7.0), "rain":(80,200)},
    "Cotton":      {"n":(50,100), "p":(30,60),  "k":(40,80),  "ph":(6.0,8.0), "rain":(60,150)},
    "Sugarcane":   {"n":(80,150), "p":(30,60),  "k":(80,150), "ph":(6.0,7.5), "rain":(150,250)},
    "Soybean":     {"n":(20,50),  "p":(40,80),  "k":(40,80),  "ph":(6.0,7.0), "rain":(100,200)},
    "Groundnut":   {"n":(20,40),  "p":(30,70),  "k":(30,60),  "ph":(5.5,7.0), "rain":(60,150)},
    "Potato":      {"n":(80,120), "p":(60,100), "k":(80,120), "ph":(5.5,6.5), "rain":(100,200)},
    "Banana":      {"n":(60,100), "p":(30,60),  "k":(80,150), "ph":(6.0,7.5), "rain":(200,300)},
    "Millet":      {"n":(20,60),  "p":(20,50),  "k":(20,50),  "ph":(5.5,7.5), "rain":(40,100)},
}

def _ml_recommend(n, p, k, ph, rain):
    model_path = "models/crop_model.pkl"
    if os.path.exists(model_path):
        try:
            import joblib
            model = joblib.load(model_path)
            data  = np.array([[n, p, k, 25, 70, ph, rain]])
            return model.predict(data)[0], True
        except Exception:
            pass
    return None, False

def _score_crops(n, p, k, ph, rain):
    scores = {}
    for crop, r in CROP_RULES.items():
        s = 0
        for val, (lo, hi), w in [
            (n,    r["n"],    3),
            (p,    r["p"],    2),
            (k,    r["k"],    2),
            (ph,   r["ph"],   2),
            (rain, r["rain"], 1),
        ]:
            mid = (lo + hi) / 2
            rng = (hi - lo) / 2 or 1
            s  += w * max(0, 1 - abs(val - mid) / rng)
        scores[crop] = round(s / 10 * 100, 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def run():
    st.markdown("### ✿ Crop Match — ML Recommendation")
    st.markdown("Enter field parameters to get the best-fit crop from our trained model.")

    with st.form("crop_form"):
        c1, c2 = st.columns(2)
        with c1:
            n    = st.slider("Nitrogen (N) kg/ha",   0, 200, 80)
            p    = st.slider("Phosphorus (P) kg/ha", 0, 150, 45)
            k    = st.slider("Potassium (K) kg/ha",  0, 200, 55)
        with c2:
            ph   = st.slider("Soil pH",              4.0, 9.0, 6.5, step=0.1)
            rain = st.slider("Rainfall mm/year",     20, 400, 150)

        submitted = st.form_submit_button("🌾 Find Best Crop", use_container_width=True)

    if submitted:
        ml_crop, used_ml = _ml_recommend(n, p, k, ph, rain)
        ranked = _score_crops(n, p, k, ph, rain)

        if used_ml:
            st.success(f"🤖 **ML Model Recommends: {ml_crop}**")
        else:
            st.success(f"🌱 **Best Match: {ranked[0][0]}**")
            st.caption("_(Rule-based analysis — place crop_model.pkl in models/ for full ML)_")

        st.markdown("#### 🏆 Crop Compatibility Scores")
        for crop, pct in ranked[:6]:
            filled = int(pct / 10)
            bar    = "█" * filled + "░" * (10 - filled)
            marker = " ◀ ML Pick" if used_ml and crop == ml_crop else ""
            st.markdown(f"**{crop}** `{bar}` {pct}%{marker}")

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("N",  f"{n}")
        c2.metric("P",  f"{p}")
        c3.metric("K",  f"{k}")
        c4.metric("pH", f"{ph}")
        c5.metric("Rain", f"{rain}mm")
