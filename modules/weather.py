import requests
import streamlit as st

def get_weather(city):

    key = st.secrets["WEATHER_API"]

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"

    r = requests.get(url).json()

    # check API response
    if "main" not in r:
        return {"error": r.get("message", "City not found")}

    temp = r["main"]["temp"]
    desc = r["weather"][0]["description"]

    return {
        "temp": temp,
        "desc": desc
    }