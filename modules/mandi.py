import streamlit as st
import requests

def run():
    st.markdown("### ₹ Live Mandi Prices")
    st.markdown("Search live crop prices from India's data.gov.in market API.")

    crop = st.text_input("Enter crop name", placeholder="e.g. Rice, Wheat, Tomato, Onion")

    if st.button("Search Prices", use_container_width=True):
        if not crop.strip():
            st.warning("Please enter a crop name.")
            return

        try:
            key = st.secrets.get("MANDI_API", "")
            if not key:
                st.error("⚠ MANDI_API key not set in secrets.toml")
                return

            url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
            params = {"api-key": key, "format": "json", "limit": 2000}
            headers = {"User-Agent": "Mozilla/5.0"}

            with st.spinner("Fetching prices..."):
                r = requests.get(url, params=params, headers=headers, timeout=12)

            if r.status_code != 200:
                st.error(f"API error: status {r.status_code}")
                return

            data = r.json()
            records = data.get("records", [])

            results = []
            for item in records:
                commodity = item.get("commodity", "")
                price     = item.get("modal_price", "")
                if crop.lower() in commodity.lower() and price:
                    results.append({
                        "Crop":    commodity,
                        "State":   item.get("state", ""),
                        "Market":  item.get("market", ""),
                        "Price (₹/Qtl)": float(price),
                    })

            if not results:
                st.warning(f"No results found for **{crop}**. Try a different spelling.")
                return

            st.success(f"Found **{len(results)}** records for '{crop}'")

            import pandas as pd
            df = pd.DataFrame(results).sort_values("Price (₹/Qtl)", ascending=False)
            st.dataframe(df, use_container_width=True)

            avg = df["Price (₹/Qtl)"].mean()
            mn  = df["Price (₹/Qtl)"].min()
            mx  = df["Price (₹/Qtl)"].max()
            c1, c2, c3 = st.columns(3)
            c1.metric("📊 Avg Price",  f"₹{avg:,.0f}")
            c2.metric("⬇ Min Price",   f"₹{mn:,.0f}")
            c3.metric("⬆ Max Price",   f"₹{mx:,.0f}")

        except requests.exceptions.ConnectionError:
            st.error("No internet connection.")
        except Exception as e:
            st.error(f"Error: {e}")
