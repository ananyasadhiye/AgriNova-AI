import streamlit as st
import requests

def _ask_openrouter(messages, api_key):
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "meta-llama/llama-3-8b-instruct", "messages": messages},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

SYSTEM_PROMPT = (
    "You are AgriNova, an expert Indian agriculture assistant. "
    "Help farmers with crops, soil, diseases, fertilizers, irrigation, pests, "
    "and market prices. Give practical, actionable advice in simple language. "
    "When relevant, mention specific product names, dosages, and timing."
)

SUGGESTIONS = [
    "What is the best crop for black soil in Maharashtra?",
    "How do I treat early blight in tomatoes?",
    "What NPK ratio should I use for wheat?",
    "When should I irrigate sugarcane?",
    "How do I protect crops from heavy rain?",
]

def run():
    st.markdown("### ⊹ AI Chat — Farm Advisor")
    st.markdown("Ask anything about farming — crops, soil, disease, markets, weather.")

    # API key
    api_key = st.secrets.get("OPENROUTER_API_KEY", "")
    if not api_key:
        api_key = st.text_input("🔑 Enter OpenRouter API Key",
                                type="password",
                                help="Get free key at openrouter.ai/keys")
        if not api_key:
            st.warning("Enter your OpenRouter API key above to enable AI chat.")
            st.markdown("[Get a free API key →](https://openrouter.ai/keys)")
            return

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Suggestions
    st.markdown("**Quick questions:**")
    cols = st.columns(3)
    for i, s in enumerate(SUGGESTIONS[:3]):
        with cols[i % 3]:
            if st.button(s, key=f"sug_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": s})
                with st.spinner("Thinking..."):
                    try:
                        msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.chat_history
                        reply = _ask_openrouter(msgs, api_key)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    except Exception as e:
                        st.error(f"Error: {e}")
                st.rerun()

    # Display history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("Ask a farming question...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.chat_history
                    reply = _ask_openrouter(msgs, api_key)
                    st.markdown(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                except requests.exceptions.ConnectionError:
                    st.error("No internet connection.")
                except Exception as e:
                    st.error(f"AI error: {e}")

    # Clear button
    if st.session_state.chat_history:
        if st.button("🗑 Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
