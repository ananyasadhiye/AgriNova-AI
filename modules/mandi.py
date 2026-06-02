import requests
import streamlit as st

def get_prices(crop):

    API_KEY = st.secrets["MANDI_API"]

    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 1500
    }

    # ADD HEADERS HERE
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        # REQUEST WITH HEADERS
        r = requests.get(url, params=params, headers=headers, timeout=10)

        if r.status_code != 200:
            st.error("Mandi API not responding")
            return []

        try:
            data = r.json()
        except:
            st.error("Invalid response from API")
            return []

        result = []

        if "records" not in data:
            return []

        for item in data["records"]:

            commodity = item.get("commodity", "")
            state = item.get("state", "")
            market = item.get("market", "")
            price = item.get("modal_price", "")

            # BETTER SEARCH MATCH
            if crop.lower() not in commodity.lower() and commodity.lower() not in crop.lower():
                continue

            if price == "":
                continue

            result.append({
                "Crop": commodity,
                "State": state,
                "Market": market,
                "Price": float(price),
                "Latitude": item.get("latitude", 20),
                "Longitude": item.get("longitude", 78)
            })

        return result

    except Exception as e:
        st.error(f"API Error: {e}")
        return []