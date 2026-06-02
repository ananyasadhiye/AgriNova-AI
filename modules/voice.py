import streamlit as st
import io

def run():
    st.markdown("### ♪ Voice Out — Text to Speech")
    st.markdown("Type any farming advice or information and listen to it spoken aloud.")

    PRESETS = {
        "Crop Tips":     "Apply fertilizer in the early morning for best absorption. Ensure adequate irrigation before and after application.",
        "Weather Alert": "Heavy rainfall expected in the next 48 hours. Protect your crops by ensuring proper drainage and covering sensitive plants.",
        "Market Update": "Today's rice price is 2400 rupees per quintal in local mandis. Wheat is trading at 2050 rupees per quintal.",
        "Disease Alert":  "Early blight symptoms detected in nearby farms. Spray Mancozeb every 7 days as a precaution.",
    }

    preset = st.selectbox("Quick presets", ["Custom"] + list(PRESETS.keys()))
    default_text = PRESETS.get(preset, "") if preset != "Custom" else ""
    text = st.text_area("Enter text to speak", value=default_text, height=120,
                        placeholder="Type farming advice, alerts, or any text here...")

    lang = st.selectbox("Language", ["English (en)", "Hindi (hi)", "Kannada (kn)",
                                      "Telugu (te)", "Tamil (ta)", "Marathi (mr)"])
    lang_code = lang.split("(")[1].rstrip(")")

    if st.button("🔊 Speak Text", use_container_width=True):
        if not text.strip():
            st.warning("Please enter some text to speak.")
            return
        try:
            from gtts import gTTS
            tts   = gTTS(text=text, lang=lang_code, slow=False)
            audio = io.BytesIO()
            tts.write_to_fp(audio)
            audio.seek(0)
            st.audio(audio, format="audio/mp3")
            st.success("✅ Audio ready — press play above!")
        except ImportError:
            st.error("gTTS not installed. Run: `pip install gTTS`")
        except Exception as e:
            st.error(f"TTS error: {e}")
            st.info("Tip: Check your internet connection. gTTS requires internet to generate audio.")
