import streamlit as st

# Rule-based crop recommendation (no model file needed)
def _rule_recommend(n, p, k, ph, rain):
    score = {}

    def add(crop, pts):
        score[crop] = score.get(crop, 0) + pts

    # Nitrogen preferences
    if n > 80:
        add("Maize", 3); add("Sugarcane", 2); add("Cotton", 1)
    elif n > 50:
        add("Wheat", 3); add("Rice", 2)
    else:
        add("Groundnut", 2); add("Soybean", 2); add("Millet", 1)

    # Phosphorus
    if p > 60:
        add("Wheat", 2); add("Maize", 2); add("Potato", 3)
    elif p > 30:
        add("Rice", 2); add("Soybean", 2)
    else:
        add("Millet", 2); add("Groundnut", 1)

    # Potassium
    if k > 80:
        add("Banana", 3); add("Potato", 2); add("Sugarcane", 2)
    elif k > 40:
        add("Cotton", 2); add("Wheat", 1)
    else:
        add("Rice", 2); add("Groundnut", 1)

    # pH
    if 5.5 <= ph <= 6.5:
        add("Rice", 2); add("Maize", 2); add("Soybean", 2)
    elif 6.5 < ph <= 7.5:
        add("Wheat", 3); add("Cotton", 2); add("Sugarcane", 1)
    elif ph > 7.5:
        add("Barley", 2); add("Wheat", 1)
    else:
        add("Blueberry", 1); add("Tea", 1)

    # Rainfall
    if rain > 200:
        add("Rice", 3); add("Sugarcane", 2); add("Banana", 2)
    elif rain > 100:
        add("Maize", 2); add("Cotton", 2); add("Soybean", 1)
    else:
        add("Wheat", 2); add("Millet", 3); add("Groundnut", 2)

    return sorted(score.items(), key=lambda x: x[1], reverse=True)

def run():
    st.markdown("### ◈ Soil AI — Crop Recommendation")
    st.markdown("Enter your soil nutrients and conditions to get the best crop matches.")

    with st.form("soil_form"):
        c1, c2 = st.columns(2)
        with c1:
            n    = st.number_input("Nitrogen (N) kg/ha",   min_value=0,   max_value=300,  value=60)
            p    = st.number_input("Phosphorus (P) kg/ha", min_value=0,   max_value=200,  value=40)
            k    = st.number_input("Potassium (K) kg/ha",  min_value=0,   max_value=200,  value=50)
        with c2:
            ph   = st.number_input("Soil pH",              min_value=0.0, max_value=14.0, value=6.5, step=0.1)
            rain = st.number_input("Rainfall (mm/year)",   min_value=0,   max_value=500,  value=150)
        submitted = st.form_submit_button("🌱 Recommend Crops", use_container_width=True)

    if submitted:
        ranked = _rule_recommend(n, p, k, ph, rain)
        top    = ranked[0][0] if ranked else "Wheat"

        st.success(f"**Best Crop for Your Soil: {top}**")

        st.markdown("#### 🏆 Top Recommendations")
        for i, (crop, pts) in enumerate(ranked[:5], 1):
            pct = min(int((pts / ranked[0][1]) * 100), 100)
            bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
            st.markdown(f"`{i}.` **{crop}** — {bar} {pct}% match")

        st.markdown("#### 📊 Your Soil Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("N", f"{n} kg/ha")
        c2.metric("P", f"{p} kg/ha")
        c3.metric("K", f"{k} kg/ha")
        c4, c5 = st.columns(2)
        c4.metric("pH",      f"{ph}")
        c5.metric("Rainfall",f"{rain} mm")
