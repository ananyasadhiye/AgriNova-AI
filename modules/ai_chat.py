import streamlit as st
import requests

API_KEY = st.secrets["OPENROUTER_API_KEY"]

def ask_ai(q):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert agriculture assistant helping farmers with crops, soil, pests and fertilizers."
            },
            {
                "role": "user",
                "content": q
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    return result["choices"][0]["message"]["content"]