import streamlit as st
import requests

def run():
    st.markdown("### ☁ Weather Forecast")
    st.markdown("Get real-time weather for any city.")

    city = st.text_input("Enter city name", placeholder="e.g. Bengaluru, Mysuru, Hubli")

    if st.button("Get Weather", use_container_width=True):
        if not city.strip():
            st.warning("Please enter a city name.")
            return

        try:
            key = st.secrets.get("WEATHER_API", "")
            if not key:
                st.error("⚠ WEATHER_API key not set in secrets.toml")
                return

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
            r = requests.get(url, timeout=8).json()

            if "main" not in r:
                st.error(f"City not found: {r.get('message', 'Unknown error')}")
                return

            temp    = r["main"]["temp"]
            feels   = r["main"]["feels_like"]
            humidity= r["main"]["humidity"]
            desc    = r["weather"][0]["description"].title()
            wind    = r["wind"]["speed"]
            country = r["sys"]["country"]

            st.success(f"Weather in **{city.title()}, {country}**")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🌡 Temperature", f"{temp}°C")
            c2.metric("🤔 Feels Like",  f"{feels}°C")
            c3.metric("💧 Humidity",    f"{humidity}%")
            c4.metric("💨 Wind",        f"{wind} m/s")
            st.info(f"**Condition:** {desc}")

        except requests.exceptions.ConnectionError:
            st.error("No internet connection.")
        except Exception as e:
            st.error(f"Error: {e}")
