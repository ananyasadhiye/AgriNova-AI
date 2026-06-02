import streamlit as st
import numpy as np
import os

# Fallback: simple regression formula derived from typical dataset ranges
def _estimate_yield(rain, temp, pesticide):
    # Approximate hg/ha from typical crop yield dataset
    base      = 28000
    rain_eff  = (rain - 1000) * 4.5
    temp_eff  = (temp - 15)   * 300
    pest_eff  = np.log1p(pesticide) * 800
    total     = base + rain_eff + temp_eff + pest_eff
    return max(500, round(total, 0))

def _ml_predict(rain, temp, pesticide):
    model_path = "models/yield_model.pkl"
    if os.path.exists(model_path):
        try:
            import pickle
            model = pickle.load(open(model_path, "rb"))
            pred  = model.predict([[rain, temp, pesticide]])
            return round(float(pred[0]), 0), True
        except Exception:
            pass
    return None, False

def run():
    st.markdown("### ▲ Yield Forecast")
    st.markdown("Predict your harvest output based on environmental and farming conditions.")

    with st.form("yield_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            rain      = st.number_input("Rainfall (mm/year)",     100,  4000, 1200, step=50)
        with c2:
            temp      = st.number_input("Avg Temperature (°C)",   5.0,  40.0, 20.0, step=0.5)
        with c3:
            pesticide = st.number_input("Pesticides (tonnes/ha)", 0.0, 500.0,  5.0, step=0.5)

        submitted = st.form_submit_button("📈 Predict Yield", use_container_width=True)

    if submitted:
        ml_val, used_ml = _ml_predict(rain, temp, pesticide)

        if used_ml:
            y_hg   = ml_val
            method = "🤖 ML Model"
        else:
            y_hg   = _estimate_yield(rain, temp, pesticide)
            method = "📐 Estimation Formula"
            st.caption("_(Place yield_model.pkl in models/ for full ML accuracy)_")

        y_kg   = round(y_hg / 100, 1)   # convert hg/ha → kg/ha (÷100)  approximate
        y_ton  = round(y_kg / 1000, 2)  # kg → tonnes

        st.success(f"**{method} Prediction**")
        c1, c2, c3 = st.columns(3)
        c1.metric("Yield (hg/ha)",      f"{y_hg:,.0f}")
        c2.metric("Approx (kg/ha)",     f"{y_kg:,.1f}")
        c3.metric("Approx (tonnes/ha)", f"{y_ton:.2f}")

        st.markdown("#### 📊 Input Summary")
        st.markdown(f"- 🌧 Rainfall: **{rain} mm/year**")
        st.markdown(f"- 🌡 Temperature: **{temp}°C**")
        st.markdown(f"- 🧪 Pesticides: **{pesticide} tonnes/ha**")
