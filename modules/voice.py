from gtts import gTTS
import streamlit as st
import io

def speak(text):

    tts=gTTS(text)

    audio=io.BytesIO()

    tts.write_to_fp(audio)

    st.audio(audio)