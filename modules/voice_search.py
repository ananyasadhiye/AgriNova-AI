import streamlit as st

def run():
    st.markdown("### ◉ Voice Search — Ask by Speaking")
    st.markdown("Use your microphone to ask farming questions.")

    st.info("""
    **How to use Voice Search:**
    1. Click the button below to start listening
    2. Speak your farming question clearly
    3. The AI will transcribe and answer it
    
    > ⚠ Requires microphone access and works best on desktop Chrome/Edge.
    """)

    # Browser-based speech recognition using Web Speech API
    st.components.v1.html("""
    <style>
      body { font-family: system-ui; background: transparent; }
      button {
        padding: 12px 28px; font-size: 15px; font-weight: 600;
        background: #f5a623; color: #1a0f00; border: none;
        border-radius: 10px; cursor: pointer; margin: 8px 0;
        transition: all .2s;
      }
      button:hover { background: #e09010; transform: translateY(-1px); }
      button:disabled { background: #888; cursor: not-allowed; }
      #status { color: #7a6f5e; font-size: 13px; margin: 8px 0; }
      #result-box {
        background: #1c1814; color: #f0e8d8;
        border: 1px solid rgba(255,220,160,0.15);
        border-radius: 10px; padding: 14px 18px;
        font-size: 14px; margin-top: 12px; min-height: 60px;
        display: none;
      }
    </style>
    <button id="startBtn" onclick="startListening()">🎙 Start Listening</button>
    <div id="status">Ready to listen...</div>
    <div id="result-box" id="result"></div>

    <script>
    let recognition;
    function startListening() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        document.getElementById('status').innerText = '❌ Speech Recognition not supported in this browser. Use Chrome or Edge.';
        return;
      }
      recognition = new SpeechRecognition();
      recognition.lang = 'en-IN';
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      document.getElementById('startBtn').disabled = true;
      document.getElementById('status').innerText  = '🎙 Listening... speak now';

      recognition.onresult = function(e) {
        const transcript = e.results[0][0].transcript;
        const box = document.getElementById('result-box');
        box.style.display = 'block';
        box.innerHTML = '<strong>You said:</strong> ' + transcript;
        document.getElementById('status').innerText = '✅ Got it! Copy the text above to the AI Chat tab.';
        document.getElementById('startBtn').disabled = false;
      };

      recognition.onerror = function(e) {
        document.getElementById('status').innerText = '❌ Error: ' + e.error + '. Try again.';
        document.getElementById('startBtn').disabled = false;
      };

      recognition.onend = function() {
        document.getElementById('startBtn').disabled = false;
      };

      recognition.start();
    }
    </script>
    """, height=200)

    st.markdown("---")
    st.markdown("#### 💬 Or Type Your Question")
    question = st.text_input("Type a farming question", placeholder="e.g. What fertilizer is best for rice?")
    if st.button("🔍 Get Answer", use_container_width=True):
        if question.strip():
            _answer_question(question)

def _answer_question(q):
    q_lower = q.lower()
    if any(w in q_lower for w in ["fertilizer","fertiliser","npk","nitrogen"]):
        st.info("**Fertilizer Advice:** Apply NPK 17:17:17 at 2 bags/acre at sowing. Top-dress with urea at 1 bag/acre after 30 days. Avoid over-application — it burns roots.")
    elif any(w in q_lower for w in ["disease","blight","spot","mold","fungus"]):
        st.info("**Disease Control:** Spray Mancozeb 2g/L or Copper Oxychloride 3g/L every 10 days. Remove and destroy infected plant material. Improve drainage to reduce humidity.")
    elif any(w in q_lower for w in ["irrigation","water","rain"]):
        st.info("**Irrigation Tips:** Rice needs 5–7 cm standing water. Wheat needs irrigation at crown root stage (21 days), jointing (45 days), and grain filling (75 days). Avoid waterlogging.")
    elif any(w in q_lower for w in ["pest","insect","aphid","worm"]):
        st.info("**Pest Management:** Use Imidacloprid 0.3ml/L for sucking pests. For bollworms, spray Chlorpyrifos 2ml/L. Consider neem oil 5ml/L as an organic option.")
    elif any(w in q_lower for w in ["price","mandi","market","rate"]):
        st.info("**Market Advice:** Check the Mandi Prices tab for live rates. Generally sell when stock is low (post-monsoon dip ends). Avoid selling immediately after harvest when supply is high.")
    else:
        st.info(f"**General Advice for:** _{q}_\n\nFor detailed AI responses, paste this question into the **AI Chat** tab where our LLM assistant will answer with full context.")
