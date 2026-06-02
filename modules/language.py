import streamlit as st

TRANSLATIONS = {
    "English": {
        "welcome": "Welcome to AgriNova AI",
        "subtitle": "Your intelligent farming assistant",
        "weather": "Weather", "mandi": "Mandi Prices", "disease": "Disease Scan",
        "soil": "Soil AI", "crop": "Crop Match", "yield": "Yield Forecast",
        "price": "Price AI", "voice": "Voice Out", "chat": "AI Chat",
        "tip": "Tip: Water your crops early in the morning to reduce evaporation.",
        "flag": "🇬🇧",
    },
    "ಕನ್ನಡ (Kannada)": {
        "welcome": "AgriNova AI ಗೆ ಸ್ವಾಗತ",
        "subtitle": "ನಿಮ್ಮ ಬುದ್ಧಿವಂತ ಕೃಷಿ ಸಹಾಯಕ",
        "weather": "ಹವಾಮಾನ", "mandi": "ಮಂಡಿ ಬೆಲೆಗಳು", "disease": "ರೋಗ ಪತ್ತೆ",
        "soil": "ಮಣ್ಣಿನ AI", "crop": "ಬೆಳೆ ಹೊಂದಾಣಿಕೆ", "yield": "ಇಳುವರಿ ಮುನ್ಸೂಚನೆ",
        "price": "ಬೆಲೆ AI", "voice": "ಧ್ವನಿ", "chat": "AI ಚಾಟ್",
        "tip": "ಸಲಹೆ: ಬಾಷ್ಪೀಕರಣವನ್ನು ಕಡಿಮೆ ಮಾಡಲು ಬೆಳಿಗ್ಗೆ ಬೇಗ ಬೆಳೆಗಳಿಗೆ ನೀರು ಹಾಕಿ.",
        "flag": "🇮🇳",
    },
    "हिंदी (Hindi)": {
        "welcome": "AgriNova AI में आपका स्वागत है",
        "subtitle": "आपका स्मार्ट खेती सहायक",
        "weather": "मौसम", "mandi": "मंडी भाव", "disease": "रोग स्कैन",
        "soil": "मिट्टी AI", "crop": "फसल मिलान", "yield": "उपज अनुमान",
        "price": "मूल्य AI", "voice": "आवाज़", "chat": "AI चैट",
        "tip": "सुझाव: वाष्पीकरण कम करने के लिए सुबह जल्दी फसलों को पानी दें।",
        "flag": "🇮🇳",
    },
    "తెలుగు (Telugu)": {
        "welcome": "AgriNova AI కి స్వాగతం",
        "subtitle": "మీ స్మార్ట్ వ్యవసాయ సహాయకుడు",
        "weather": "వాతావరణం", "mandi": "మండి ధరలు", "disease": "వ్యాధి స్కాన్",
        "soil": "నేల AI", "crop": "పంట మ్యాచ్", "yield": "దిగుబడి అంచనా",
        "price": "ధర AI", "voice": "వాయిస్", "chat": "AI చాట్",
        "tip": "చిట్కా: బాష్పీభవనాన్ని తగ్గించడానికి తెల్లవారుజామున పంటలకు నీరు పెట్టండి.",
        "flag": "🇮🇳",
    },
    "தமிழ் (Tamil)": {
        "welcome": "AgriNova AI க்கு வரவேற்கிறோம்",
        "subtitle": "உங்கள் புத்திசாலி வேளாண் உதவியாளர்",
        "weather": "வானிலை", "mandi": "மண்டி விலைகள்", "disease": "நோய் ஸ்கேன்",
        "soil": "மண் AI", "crop": "பயிர் பொருத்தம்", "yield": "மகசூல் முன்னறிவிப்பு",
        "price": "விலை AI", "voice": "குரல்", "chat": "AI அரட்டை",
        "tip": "குறிப்பு: ஆவியாதலை குறைக்க காலையில் பயிர்களுக்கு தண்ணீர் பாய்ச்சுங்கள்.",
        "flag": "🇮🇳",
    },
    "मराठी (Marathi)": {
        "welcome": "AgriNova AI मध्ये आपले स्वागत आहे",
        "subtitle": "तुमचा हुशार शेती सहाय्यक",
        "weather": "हवामान", "mandi": "मंडी भाव", "disease": "रोग स्कॅन",
        "soil": "माती AI", "crop": "पीक जुळणी", "yield": "उत्पन्न अंदाज",
        "price": "किंमत AI", "voice": "आवाज", "chat": "AI चॅट",
        "tip": "टिप: बाष्पीभवन कमी करण्यासाठी सकाळी लवकर पिकांना पाणी द्या.",
        "flag": "🇮🇳",
    },
}

def run():
    st.markdown("### ✱ Language Settings")
    st.markdown("Choose your preferred language for the interface.")

    if "app_lang" not in st.session_state:
        st.session_state.app_lang = "English"

    cols = st.columns(3)
    for i, lang in enumerate(TRANSLATIONS.keys()):
        with cols[i % 3]:
            t = TRANSLATIONS[lang]
            active = st.session_state.app_lang == lang
            label  = f"{t['flag']} {lang}"
            if st.button(label, key=f"lang_{i}", use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.app_lang = lang
                st.rerun()

    st.markdown("---")
    lang = st.session_state.app_lang
    t    = TRANSLATIONS[lang]

    st.markdown(f"#### {t['flag']} {lang} — Preview")
    st.success(f"**{t['welcome']}**")
    st.info(t['subtitle'])
    st.markdown(f"💡 {t['tip']}")

    st.markdown("#### Module Names in This Language")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"☁ {t['weather']}")
        st.markdown(f"₹ {t['mandi']}")
        st.markdown(f"🍃 {t['disease']}")
    with c2:
        st.markdown(f"◈ {t['soil']}")
        st.markdown(f"✿ {t['crop']}")
        st.markdown(f"▲ {t['yield']}")
    with c3:
        st.markdown(f"⟁ {t['price']}")
        st.markdown(f"♪ {t['voice']}")
        st.markdown(f"⊹ {t['chat']}")
