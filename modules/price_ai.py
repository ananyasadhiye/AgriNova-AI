import streamlit as st
import numpy as np

def _predict(prices):
    if len(prices) < 2:
        return prices[-1]
    from sklearn.linear_model import LinearRegression
    X = np.arange(len(prices)).reshape(-1, 1)
    y = np.array(prices)
    m = LinearRegression()
    m.fit(X, y)
    return round(float(m.predict([[len(prices)]])[0]), 2)

SAMPLE_PRICES = {
    "Rice":   [2200, 2300, 2250, 2400, 2350, 2500],
    "Wheat":  [1900, 1950, 2000, 1980, 2050, 2100],
    "Tomato": [1500, 1800, 2200, 1600, 1900, 2400],
    "Onion":  [1200, 1400, 1100, 1600, 1300, 1700],
    "Cotton": [5500, 5700, 5900, 6100, 5800, 6200],
}

def run():
    st.markdown("### ⟁ Price AI — Mandi Price Predictor")
    st.markdown("Enter historical prices to predict tomorrow's mandi rate.")

    tab1, tab2 = st.tabs(["📊 Manual Entry", "🌾 Quick Demo"])

    with tab1:
        st.markdown("Enter last 6 days' prices (₹/Qtl):")
        cols = st.columns(6)
        prices = []
        for i, col in enumerate(cols):
            with col:
                val = st.number_input(f"Day {i+1}", min_value=0, max_value=50000,
                                      value=2000 + i*50, key=f"price_{i}")
                prices.append(val)

        if st.button("🔮 Predict Tomorrow's Price", use_container_width=True, key="manual_predict"):
            pred = _predict(prices)
            trend = "📈" if pred > prices[-1] else "📉"
            st.success(f"{trend} **Predicted Price: ₹{pred:,.2f} / Qtl**")
            diff = pred - prices[-1]
            st.info(f"Expected change from today: **{'+' if diff >= 0 else ''}{diff:.2f} ₹**")
            _show_chart(prices, pred)

    with tab2:
        crop = st.selectbox("Select crop", list(SAMPLE_PRICES.keys()))
        prices = SAMPLE_PRICES[crop]
        st.markdown(f"Last 6 days prices for **{crop}** (₹/Qtl):")
        st.write(prices)
        if st.button("🔮 Predict", use_container_width=True, key="demo_predict"):
            pred = _predict(prices)
            trend = "📈" if pred > prices[-1] else "📉"
            st.success(f"{trend} **Predicted Price: ₹{pred:,.2f} / Qtl**")
            _show_chart(prices, pred)

def _show_chart(prices, pred):
    try:
        import pandas as pd
        days = [f"Day {i+1}" for i in range(len(prices))] + ["Tomorrow"]
        vals = prices + [pred]
        df   = pd.DataFrame({"Day": days, "Price": vals})
        st.line_chart(df.set_index("Day"))
    except Exception:
        pass
