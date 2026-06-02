import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from modules.price_ai import predict_price
from modules.ai_chat import ask_ai
from modules.weather import get_weather
from modules.mandi import get_prices
from modules.yield_ai import predict_yield
from modules.disease_ai import detect_disease
from modules.voice import speak
from modules.crop_ai import recommend_crop


st.set_page_config(page_title="AgriNova AI", layout="wide")

# LOAD CSS
def load_css():
    with open("assets/background.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ⭐ Shooting stars
st.markdown("""
<div class="stars"></div>
""", unsafe_allow_html=True)

# 🌫 Floating Orbs
st.markdown("""
<div class="orb" style="left:20%"></div>
<div class="orb" style="left:60%"></div>
<div class="orb" style="left:80%"></div>
""", unsafe_allow_html=True)

# 📊 Floating Data Icons
st.markdown("""
<div class="data-point" style="left:10%">📊</div>
<div class="data-point" style="left:40%">📈</div>
<div class="data-point" style="left:70%">📉</div>
""", unsafe_allow_html=True)


# 🌐 Neural Network Background
components.html("""
<canvas id="network"></canvas>

<style>
#network{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
z-index:-2;
}
</style>

<script>

const canvas=document.getElementById("network")
const ctx=canvas.getContext("2d")

canvas.width=window.innerWidth
canvas.height=window.innerHeight

let nodes=[]

for(let i=0;i<60;i++){
nodes.push({
x:Math.random()*canvas.width,
y:Math.random()*canvas.height,
vx:(Math.random()-0.5),
vy:(Math.random()-0.5)
})
}

function draw(){

ctx.clearRect(0,0,canvas.width,canvas.height)

for(let i=0;i<nodes.length;i++){

let n=nodes[i]

n.x+=n.vx
n.y+=n.vy

if(n.x<0||n.x>canvas.width) n.vx*=-1
if(n.y<0||n.y>canvas.height) n.vy*=-1

ctx.beginPath()
ctx.arc(n.x,n.y,2,0,Math.PI*2)
ctx.fillStyle="#38bdf8"
ctx.fill()

for(let j=i;j<nodes.length;j++){

let dx=n.x-nodes[j].x
let dy=n.y-nodes[j].y
let dist=Math.sqrt(dx*dx+dy*dy)

if(dist<120){

ctx.beginPath()
ctx.moveTo(n.x,n.y)
ctx.lineTo(nodes[j].x,nodes[j].y)
ctx.strokeStyle="rgba(56,189,248,0.2)"
ctx.stroke()

}

}

}

requestAnimationFrame(draw)

}

draw()

</script>
""", height=0)

# 🌟 HERO TITLE
st.markdown("""
<div class="hero-title">AgriNova AI</div>
<div class="hero-sub">AI Intelligence for Smart Farming</div>
""", unsafe_allow_html=True)

# 🤖 Rotating AI Ring
components.html("""
<style>

.ai-ring{
position:absolute;
left:50%;
top:120px;
width:300px;
height:300px;
border-radius:50%;
border:2px solid rgba(56,189,248,0.3);
animation:spin 20s linear infinite;
}

@keyframes spin{
0%{transform:translateX(-50%) rotate(0deg)}
100%{transform:translateX(-50%) rotate(360deg)}
}

</style>

<div class="ai-ring"></div>

""", height=0)


# SIDEBAR
menu = st.sidebar.selectbox("Navigation",[
"Dashboard",
"Weather",
"Mandi Prices",
"Disease Detection",
"Soil AI",
"Yield Prediction",
"Voice Assistant",
"AI Chat"
])


# DASHBOARD
if menu == "Dashboard":

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="glass-card">
        <div class="icon">🌦</div>
        <h3>Weather AI</h3>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
        <div class="icon">🌾</div>
        <h3>Crop Advisor</h3>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="glass-card">
        <div class="icon">🦠</div>
        <h3>Disease Detection</h3>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="glass-card">
        <div class="icon">📈</div>
        <h3>Market AI</h3>
        </div>
        """, unsafe_allow_html=True)


# WEATHER
elif menu == "Weather":

    city = st.text_input("Enter City")

    if st.button("Get Weather"):

        w = get_weather(city)

        if "error" in w:
            st.error(w["error"])
        else:
            st.success(f"{w['temp']}°C | {w['desc']}")


# VOICE
elif menu == "Voice Assistant":

    st.markdown("""
    <div class="wave">
    <span></span><span></span><span></span><span></span>
    </div>
    """, unsafe_allow_html=True)

    q = st.text_input("Ask AI")

    if st.button("Ask"):
        ans = ask_ai(q)
        st.write(ans)
        speak(ans)


# CHAT
elif menu == "AI Chat":

    q = st.chat_input("Ask question")

    if q:
        st.chat_message("user").write(q)
        ans = ask_ai(q)
        st.chat_message("assistant").write(ans)