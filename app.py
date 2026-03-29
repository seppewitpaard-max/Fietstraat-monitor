import streamlit as st
import pandas as pd
import datetime
import random
import time
import base64
from pathlib import Path
import importlib
import textwrap
import numpy as np
from PIL import Image
import hashlib

st.set_page_config(
    page_title="Savanne Bewakingssysteem — Cheeta Bescherming",
    page_icon="🐆",
    layout="wide",
)

# ─────────────────────────────────────────────
# THEMA INIT
# ─────────────────────────────────────────────
if "thema" not in st.session_state:
    st.session_state.thema = "licht"

THEMA_KLEUREN = {
    "licht": {
        "bg": "#FFF8F2",
        "card": "#ffffff",
        "tekst": "#1a1a1a",
        "subtekst": "#666",
        "rand": "#e8e0d8",
        "oranje": "#E84E0F",
        "groen": "#2D8A4B",
    },
    "donker": {
        "bg": "#1a1208",
        "card": "#2a1f0e",
        "tekst": "#f0e6d3",
        "subtekst": "#b09070",
        "rand": "#3a2d1a",
        "oranje": "#E84E0F",
        "groen": "#41B96A",
    },
}

thema = st.session_state.thema
BG = THEMA_KLEUREN[thema]["bg"]
CARD = THEMA_KLEUREN[thema]["card"]
TEKST = THEMA_KLEUREN[thema]["tekst"]
SUBTEKST = THEMA_KLEUREN[thema]["subtekst"]
RAND = THEMA_KLEUREN[thema]["rand"]
ACCENT_ORANJE = THEMA_KLEUREN[thema]["oranje"]
ACCENT_GROEN = THEMA_KLEUREN[thema]["groen"]

BASE_DIR = Path(__file__).resolve().parent
THOMAS_MORE_LOGO_URL = str(BASE_DIR / "tm_logo.svg")
CAMPUS_LOGO_URL = str(BASE_DIR / "campus_logo.svg")
CHEETAH_IMAGE_URL = str(BASE_DIR / "cheetah_image.svg")
LIVE_FEED_URL = "https://www.youtube.com/watch?v=ydYDqZQpim8"


def svg_data_uri(svg_path: str) -> str:
    """Zet een lokale svg om naar een data-URI zodat Streamlit Cloud ze altijd kan tonen."""
    data = Path(svg_path).read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"


def svg_img_tag(svg_path: str, style: str) -> str:
    uri = svg_data_uri(svg_path)
    return f'<img src="{uri}" style="{style}" />'

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}

.stApp {{
    background-color: {BG};
    background-image:
        radial-gradient(ellipse at 20% 10%, rgba(232,78,15,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 90%, rgba(210,140,50,0.08) 0%, transparent 50%);
}}

.savanna-header {{
    background: linear-gradient(135deg, {ACCENT_ORANJE} 0%, #D4890A 55%, {ACCENT_GROEN} 100%);
    padding: 22px 32px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(232,78,15,0.25);
    position: relative;
    overflow: hidden;
}}
.savanna-header::before {{
    content: "🌾";
    position: absolute;
    right: 24px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 80px;
    opacity: 0.15;
}}
.savanna-header h1 {{
    color: white;
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 900;
    margin: 0;
    line-height: 1.2;
    text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}}
.savanna-header p {{
    color: rgba(255,255,255,0.82);
    font-size: 13px;
    margin: 5px 0 0;
    font-weight: 500;
}}

.logo-card {{
    background: {CARD};
    border: 1.5px solid {RAND};
    border-radius: 14px;
    padding: 10px;
    margin-bottom: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}

[data-testid="stMetric"] {{
    background: {CARD};
    border-radius: 16px;
    padding: 18px 22px !important;
    border: 1.5px solid {RAND};
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    transition: transform 0.2s;
}}
[data-testid="stMetric"]:hover {{ transform: translateY(-2px); }}
[data-testid="stMetricValue"] {{ color: {ACCENT_ORANJE} !important; font-size: 28px !important; font-weight: 800 !important; font-family:'Playfair Display',serif !important; }}
[data-testid="stMetricLabel"] {{ color: {SUBTEKST} !important; font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.8px; }}

.stButton > button {{
    background: linear-gradient(135deg, {ACCENT_ORANJE}, {ACCENT_GROEN}) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    width: 100%;
    padding: 10px 0 !important;
    font-size: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 12px rgba(45,138,75,0.28) !important;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, #c43d08, #23733d) !important;
    box-shadow: 0 6px 20px rgba(45,138,75,0.36) !important;
    transform: translateY(-1px) !important;
}}

.info-btn > button {{
    background: linear-gradient(135deg, #2d6a2d, #4a9a4a) !important;
    font-size: 16px !important;
    padding: 14px 0 !important;
    border-radius: 14px !important;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 20px rgba(45,106,45,0.4) !important;
    animation: pulse-green 2.5s infinite;
}}
@keyframes pulse-green {{ 0%,100%{{transform:scale(1)}} 50%{{transform:scale(1.03)}} }}

section[data-testid="stSidebar"] {{
    background: {CARD} !important;
    border-right: 3px solid {ACCENT_ORANJE};
}}
section[data-testid="stSidebar"] * {{ color: {TEKST} !important; }}

.savanna-card {{
    background: {CARD};
    border-radius: 18px;
    padding: 24px;
    border: 1.5px solid {RAND};
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    color: {TEKST};
}}
.savanna-card h3 {{
    font-family: 'Playfair Display', serif;
    font-size: 16px;
    font-weight: 700;
    color: {TEKST};
    margin: 0 0 16px;
}}

.live-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(232,78,15,0.08);
    border: 1.5px solid {ACCENT_ORANJE};
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 700;
    color: {ACCENT_ORANJE};
    float: right;
}}

.dier-card {{
    background: {CARD};
    border-radius: 18px;
    padding: 22px;
    border: 1.5px solid {RAND};
    box-shadow: 0 4px 16px rgba(0,0,0,0.07);
    text-align: center;
    transition: transform 0.22s, box-shadow 0.22s;
    color: {TEKST};
}}
.dier-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 32px rgba(45,138,75,0.24);
    border-color: {ACCENT_GROEN};
}}

.dier-observatie-rij {{
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 8px;
    background: {CARD};
    border: 1px solid {RAND};
    font-size: 14px;
}}
.dier-observatie-rij:hover {{ border-color: {ACCENT_GROEN}; background: rgba(45,138,75,0.08); }}

.credits-card {{
    background: {CARD};
    border-radius: 20px;
    padding: 40px;
    border: 2px solid {RAND};
    text-align: center;
    box-shadow: 0 8px 40px rgba(0,0,0,0.1);
    color: {TEKST};
}}

hr {{ border-color: {RAND}; margin: 16px 0; }}
p, li, span, label {{ color: {TEKST} !important; }}
h1,h2,h3,h4,h5,h6 {{ color: {TEKST} !important; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TEACHABLE MACHINE MODEL
# ─────────────────────────────────────────────
TM_NAAR_DIER = {
    "zebra": "Zebra 🦓", "cheetah": "Cheeta 🐆", "cheeta": "Cheeta 🐆",
    "gier": "Gier 🦅", "vulture": "Gier 🦅",
    "giraf": "Giraf 🦒", "giraffe": "Giraf 🦒",
    "jakhals": "Jakhals 🦊", "jackal": "Jakhals 🦊",
    "olifant": "Olifant 🐘", "elephant": "Olifant 🐘",
    "leeuw": "Leeuw 🦁", "lion": "Leeuw 🦁",
    "nijlpaard": "Nijlpaard 🦛", "hippo": "Nijlpaard 🦛",
}

@st.cache_resource
def laad_tm_model():
    """Laad het Teachable Machine Keras model (keras_model.h5 + labels.txt)."""
    model_pad = BASE_DIR / "keras_model.h5"
    labels_pad = BASE_DIR / "labels.txt"
    if not model_pad.exists() or not labels_pad.exists():
        return None, None
    try:
        keras_models = importlib.import_module("tensorflow.keras.models")
        load_model = keras_models.load_model
        model = load_model(str(model_pad), compile=False)
        labels = []
        with open(labels_pad, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(" ", 1)
                if len(parts) >= 2:
                    labels.append(parts[1].strip())
                elif parts[0]:
                    labels.append(parts[0].strip())
        return model, labels
    except Exception:
        return None, None

def classificeer_afbeelding(model, labels, afbeelding):
    """Classificeer een PIL afbeelding met het Teachable Machine model."""
    img = afbeelding.convert("RGB").resize((224, 224))
    img_array = np.asarray(img)
    normalized = (img_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized
    prediction = model.predict(data, verbose=0)
    index = int(np.argmax(prediction))
    class_name = labels[index] if index < len(labels) else "Onbekend"
    confidence = float(prediction[0][index])
    return class_name, confidence

# ─────────────────────────────────────────────
# ANIMATED SAVANNE FEED
# ─────────────────────────────────────────────
SAVANNE_FEED_HTML = """
<div style="position:relative;border-radius:14px;overflow:hidden;border:2px solid #E84E0F;box-shadow:0 8px 32px rgba(0,0,0,0.3);">
<canvas id="sf" width="700" height="380"></canvas>
</div>
<script>
const cv=document.getElementById('sf'),cx=cv.getContext('2d');
const W=cv.width,H=cv.height,GY=310;
const DIEREN=[
  {e:'🦓',n:'Zebra',s:1.2,sz:44},{e:'🐆',n:'Cheeta',s:2.0,sz:40},
  {e:'🦅',n:'Gier',s:1.5,sz:36,fly:1},{e:'🦒',n:'Giraf',s:0.7,sz:52},
  {e:'🦊',n:'Jakhals',s:1.4,sz:34},{e:'🐘',n:'Olifant',s:0.5,sz:50},
  {e:'🦁',n:'Leeuw',s:0.9,sz:44},{e:'🦛',n:'Nijlpaard',s:0.4,sz:42}
];
let ad=[],f=0,ls=0;
function spawn(){
  const d=DIEREN[Math.floor(Math.random()*DIEREN.length)];
  const dir=Math.random()>0.5?1:-1;
  ad.push({...d,x:dir>0?-60:W+60,y:d.fly?80+Math.random()*60:GY-d.sz+Math.random()*15,dir,det:false,df:0});
}
function bg(){
  let g=cx.createLinearGradient(0,0,0,GY);
  g.addColorStop(0,'#5fa8d3');g.addColorStop(0.6,'#f7dc6f');g.addColorStop(1,'#f0c27f');
  cx.fillStyle=g;cx.fillRect(0,0,W,GY);
  cx.beginPath();cx.arc(W-80,60,30,0,Math.PI*2);cx.fillStyle='#FFD700';cx.fill();
  cx.beginPath();cx.arc(W-80,60,22,0,Math.PI*2);cx.fillStyle='#FFF176';cx.fill();
  cx.fillStyle='rgba(139,115,85,0.3)';
  [[100,120],[350,80],[550,100]].forEach(([x,r])=>{
    cx.beginPath();cx.ellipse(x,GY,r,r*0.4,0,Math.PI,0);cx.fill();
  });
  [[150,GY],[420,GY],[620,GY]].forEach(([x,y])=>{
    cx.fillStyle='#4a3728';cx.fillRect(x-3,y-60,6,60);
    cx.fillStyle='rgba(85,107,47,0.7)';
    cx.beginPath();cx.ellipse(x,y-60,35,18,0,0,Math.PI*2);cx.fill();
    cx.beginPath();cx.ellipse(x-15,y-50,20,12,0.3,0,Math.PI*2);cx.fill();
    cx.beginPath();cx.ellipse(x+18,y-48,22,14,-0.2,0,Math.PI*2);cx.fill();
  });
  g=cx.createLinearGradient(0,GY,0,H);
  g.addColorStop(0,'#C4A35A');g.addColorStop(0.5,'#A08040');g.addColorStop(1,'#7A5A28');
  cx.fillStyle=g;cx.fillRect(0,GY,W,H-GY);
  cx.strokeStyle='#8B7D3C';cx.lineWidth=1.5;
  for(let i=0;i<W;i+=25){
    let o=(f*0.3+i)%W;
    cx.beginPath();cx.moveTo(o,GY);cx.lineTo(o-2,GY-7);cx.stroke();
    cx.beginPath();cx.moveTo(o+8,GY);cx.lineTo(o+10,GY-5);cx.stroke();
  }
}
function hud(){
  cx.fillStyle='rgba(0,0,0,0.65)';cx.fillRect(0,0,W,28);
  cx.fillStyle=f%60<30?'#ff3333':'#990000';cx.font='bold 11px monospace';
  cx.textAlign='left';cx.fillText('● REC',8,18);
  cx.fillStyle='white';cx.fillText('CAM SAV-001 | AI DETECTIE | SERENGETI N.P.',70,18);
  cx.textAlign='right';cx.fillText(new Date().toLocaleTimeString('nl-BE'),W-10,18);
  cx.textAlign='left';
  const sy=(f*2)%H;
  cx.strokeStyle='rgba(0,255,100,0.06)';cx.lineWidth=2;
  cx.beginPath();cx.moveTo(0,sy);cx.lineTo(W,sy);cx.stroke();
  cx.fillStyle='rgba(0,0,0,0.5)';cx.fillRect(0,H-24,W,24);
  cx.fillStyle='#00ff66';cx.font='bold 11px monospace';cx.textAlign='left';
  const det=ad.filter(a=>a.det);
  const msg=det.length>0?'DIER GEDETECTEERD: '+det[det.length-1].n.toUpperCase():'Scanning voor wildlife...';
  cx.fillText(det.length>0?'\uD83D\uDFE2 '+msg:'\uD83D\uDD0D '+msg,10,H-8);
  cx.textAlign='right';cx.fillStyle='#aaa';cx.fillText('Teachable Machine v2.0',W-10,H-8);
}
function loop(){
  f++;
  if(f-ls>200+Math.random()*300){spawn();ls=f;}
  bg();
  ad.forEach(a=>{
    a.x+=a.s*a.dir;
    if(a.fly)a.y+=Math.sin(f*0.03)*0.5;
    cx.font=a.sz+'px serif';cx.textAlign='center';cx.fillText(a.e,a.x,a.y+a.sz);
    if(a.x>150&&a.x<W-150&&!a.det){a.det=true;a.df=f;}
    if(a.det&&f-a.df<150){
      cx.strokeStyle='#00ff44';cx.lineWidth=2;cx.setLineDash([5,3]);
      cx.strokeRect(a.x-a.sz/2-8,a.y-4,a.sz+16,a.sz+12);
      cx.setLineDash([]);cx.fillStyle='rgba(0,255,68,0.08)';
      cx.fillRect(a.x-a.sz/2-8,a.y-4,a.sz+16,a.sz+12);
      cx.fillStyle='#00ff44';cx.font='bold 10px monospace';cx.textAlign='center';
      cx.fillText(a.n+' '+(85+Math.random()*13).toFixed(0)+'%',a.x,a.y-10);
    }
  });
  ad=ad.filter(a=>a.x>-80&&a.x<W+80);
  hud();requestAnimationFrame(loop);
}
spawn();loop();
</script>
"""

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
UURDATA_VANDAAG = {
    "06:00": 3, "07:00": 7, "08:00": 12, "09:00": 9,
    "10:00": 5, "11:00": 4, "12:00": 8, "13:00": 6,
    "14:00": 5, "15:00": 9, "16:00": 11, "17:00": 14,
    "18:00": 10, "19:00": 4,
}
UURDATA_GISTEREN = {
    "06:00": 2, "07:00": 5, "08:00": 10, "09:00": 7,
    "10:00": 4, "11:00": 6, "12:00": 7, "13:00": 5,
    "14:00": 7, "15:00": 8, "16:00": 9, "17:00": 11,
    "18:00": 8, "19:00": 3,
}
UURDATA_VORIGE_WEEK = {
    "06:00": 1, "07:00": 4, "08:00": 8, "09:00": 6,
    "10:00": 3, "11:00": 5, "12:00": 6, "13:00": 4,
    "14:00": 6, "15:00": 7, "16:00": 8, "17:00": 10,
    "18:00": 7, "19:00": 2,
}
UURDATA_VORIGE_MAAND = {
    "06:00": 2, "07:00": 3, "08:00": 7, "09:00": 5,
    "10:00": 3, "11:00": 4, "12:00": 5, "13:00": 3,
    "14:00": 5, "15:00": 6, "16:00": 7, "17:00": 9,
    "18:00": 6, "19:00": 2,
}

# Geobserveerde dieren op de feed (naam + emoji + aantal)
DIEREN_GISTEREN = {
    "Cheeta 🐆": 14,
    "Leeuw 🦁": 3,
    "Zebra 🦓": 22,
    "Olifant 🐘": 5,
    "Giraf 🦒": 8,
    "Nijlpaard 🦛": 2,
    "Jakhals 🦊": 6,
    "Gier 🦅": 9,
}
DIEREN_VORIGE_WEEK = {
    "Cheeta 🐆": 11,
    "Leeuw 🦁": 4,
    "Zebra 🦓": 18,
    "Olifant 🐘": 3,
    "Giraf 🦒": 7,
    "Nijlpaard 🦛": 1,
    "Jakhals 🦊": 5,
    "Gier 🦅": 7,
}
DIEREN_VORIGE_MAAND = {
    "Cheeta 🐆": 9,
    "Leeuw 🦁": 2,
    "Zebra 🦓": 15,
    "Olifant 🐘": 4,
    "Giraf 🦒": 5,
    "Nijlpaard 🦛": 2,
    "Jakhals 🦊": 4,
    "Gier 🦅": 6,
}

# Session state initialisatie
if "totaal"              not in st.session_state: st.session_state.totaal = 107
if "feed_gepauzeerd"     not in st.session_state: st.session_state.feed_gepauzeerd = False
if "detectie_gepauzeerd" not in st.session_state: st.session_state.detectie_gepauzeerd = False
if "uurdata"             not in st.session_state: st.session_state.uurdata = dict(UURDATA_VANDAAG)
if "pagina"              not in st.session_state: st.session_state.pagina = "📊 Dashboard"
if "dieren_vandaag"      not in st.session_state:
    st.session_state.dieren_vandaag = {
        "Cheeta 🐆": 18, "Leeuw 🦁": 4, "Zebra 🦓": 27,
        "Olifant 🐘": 6, "Giraf 🦒": 11, "Nijlpaard 🦛": 3,
        "Jakhals 🦊": 8, "Gier 🦅": 12,
    }
if "laatste_foto_hash"   not in st.session_state: st.session_state.laatste_foto_hash = None
if "laatste_detectie"    not in st.session_state: st.session_state.laatste_detectie = None
if "feed_huidig_dier"    not in st.session_state: st.session_state.feed_huidig_dier = None
if "feed_conf"           not in st.session_state: st.session_state.feed_conf = 0.0

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
col_logos, col_titel, col_info = st.columns([1.4, 5.6, 2])

with col_logos:
    st.markdown('<div class="logo-card">', unsafe_allow_html=True)
    st.markdown(
        svg_img_tag(THOMAS_MORE_LOGO_URL, "width:100%;height:auto;display:block;"),
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="logo-card">', unsafe_allow_html=True)
    st.markdown(
        svg_img_tag(CAMPUS_LOGO_URL, "width:100%;height:auto;display:block;"),
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_titel:
    st.markdown("""
    <div class="savanna-header">
        <div>
            <h1>🐆 Savanne Bewakingssysteem</h1>
            <p>Real-time dierenobservaties — Camera SAV-001 | Serengeti Nationaal Park</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_info:
    if st.button("🏆 CREDITS", key="credits_btn"):
        st.session_state.pagina = "🏆 Credits"
        st.rerun()
    if st.button("🎮 SPEL", key="spel_btn"):
        st.session_state.pagina = "🎮 Spel"
        st.rerun()
    st.markdown('<div class="info-btn">', unsafe_allow_html=True)
    if st.button("🦁 INFORMATIE", key="info_btn_top"):
        st.session_state.pagina = "🦁 Informatie"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🐆 Navigatie")
    st.markdown("---")
    PAGINAS = ["📊 Dashboard", "📈 Statistieken", "🦁 Informatie", "🎮 Spel", "⚙️ Instellingen", "🏆 Credits"]
    keuze = st.radio(
        "",
        PAGINAS,
        label_visibility="collapsed",
        index=PAGINAS.index(st.session_state.pagina)
            if st.session_state.pagina in PAGINAS else 0,
    )
    st.session_state.pagina = keuze
    st.markdown("---")
    st.markdown("**📍 Camera info**")
    st.write("ID: SAV-001")
    st.write("Locatie: Serengeti N.P.")
    st.write(f"{'🔴 Live' if not st.session_state.feed_gepauzeerd else '⏸️ Gepauzeerd'}")
    st.markdown("---")
    st.markdown("**🎨 Weergave**")
    thema_keuze = st.radio(
        "Thema",
        ["🌞 Licht", "🌙 Donker"],
        label_visibility="collapsed",
    )
    if "Licht" in thema_keuze:
        st.session_state.thema = "licht"
    else:
        st.session_state.thema = "donker"
    st.markdown("---")
    st.markdown(f"<small style='color:{SUBTEKST};'>Thomas More Hogeschool<br>Campus Het Spoor — Mol<br>Toegepaste Informatica</small>", unsafe_allow_html=True)

pagina = st.session_state.pagina

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
if "Dashboard" in pagina:
    # ── Detectie: Python kiest welk dier "op de feed" staat ──────────────────
    # Elk dier staat ~12s in beeld, dan rerun → teller omhoog
    FEED_DIEREN = [
        ("Zebra",     "Zebra 🦓",     "🦓"),
        ("Cheeta",    "Cheeta 🐆",    "🐆"),
        ("Gier",      "Gier 🦅",      "🦅"),
        ("Giraf",     "Giraf 🦒",     "🦒"),
        ("Jakhals",   "Jakhals 🦊",   "🦊"),
        ("Olifant",   "Olifant 🐘",   "🐘"),
        ("Leeuw",     "Leeuw 🦁",     "🦁"),
        ("Nijlpaard", "Nijlpaard 🦛", "🦛"),
    ]

    if not st.session_state.detectie_gepauzeerd:
        # Kies huidig dier op basis van de tijd (wisselt elke 12s)
        tijdslot = int(time.time() // 12)
        huidig = FEED_DIEREN[tijdslot % len(FEED_DIEREN)]
        huidig_naam, huidig_key, huidig_emoji = huidig
        conf = round(0.82 + ((tijdslot * 7919) % 100) / 588, 2)  # pseudo-random maar stabiel per slot

        # Als het tijdslot veranderd is t.o.v. vorige render → tel op
        if st.session_state.feed_huidig_dier != huidig_key:
            if st.session_state.feed_huidig_dier is not None:
                # Vorig dier was in beeld → tel op
                prev = st.session_state.feed_huidig_dier
                st.session_state.dieren_vandaag[prev] = st.session_state.dieren_vandaag.get(prev, 0) + 1
                st.session_state.totaal += 1
                st.session_state.laatste_detectie = {
                    "dier_key": prev,
                    "naam": prev.split(" ")[0],
                    "zekerheid": st.session_state.feed_conf,
                }
            st.session_state.feed_huidig_dier = huidig_key
            st.session_state.feed_conf = conf
    else:
        huidig_naam, huidig_key, huidig_emoji = ("", "", "")
        conf = 0.0

    now = datetime.datetime.now()
    totaal_gisteren = sum(DIEREN_GISTEREN.values())
    totaal_vorige_week = sum(DIEREN_VORIGE_WEEK.values())
    totaal_vorige_maand = sum(DIEREN_VORIGE_MAAND.values())
    verschil_gist = st.session_state.totaal - totaal_gisteren
    verschil_week = st.session_state.totaal - totaal_vorige_week
    verschil_maand = st.session_state.totaal - totaal_vorige_maand
    piekuur = max(st.session_state.uurdata, key=st.session_state.uurdata.get)

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("🐆 Vandaag Totaal", st.session_state.totaal)
    k2.metric("⏰ Piekuur", piekuur)
    k3.metric("📅 vs Gisteren",     f"{'+' if verschil_gist>=0 else ''}{verschil_gist}",  delta=f"{'+' if verschil_gist>=0 else ''}{verschil_gist}")
    k4.metric("📆 vs Vorige Week",  f"{'+' if verschil_week>=0 else ''}{verschil_week}",  delta=f"{'+' if verschil_week>=0 else ''}{verschil_week}")
    k5.metric("🗓️ vs Vorige Maand", f"{'+' if verschil_maand>=0 else ''}{verschil_maand}", delta=f"{'+' if verschil_maand>=0 else ''}{verschil_maand}")

    st.markdown("<br>", unsafe_allow_html=True)
    col_links, col_rechts = st.columns([1.1, 0.9], gap="large")

    # ── Canvas HTML met huidig dier groot in beeld ───────────────────────────
    with col_links:
        live_label = "⏸️ GEPAUZEERD" if st.session_state.detectie_gepauzeerd else "🔴 LIVE"
        st.markdown(f'<div class="savanna-card"><h3>📹 Live Savanne Feed <span class="live-badge">{live_label}</span></h3></div>', unsafe_allow_html=True)

        if not st.session_state.detectie_gepauzeerd:
            # Geef huidig dier door aan de canvas als JS variabele
            CANVAS_HTML = f"""
<div style="border-radius:14px;overflow:hidden;border:2px solid #E84E0F;box-shadow:0 8px 32px rgba(0,0,0,0.35);position:relative;">
<canvas id="sf" width="640" height="420" style="display:block;"></canvas>
</div>
<script>
const HUIDIG = {{e:"{huidig_emoji}", n:"{huidig_naam}", conf:{conf}}};
const cv = document.getElementById('sf');
const cx = cv.getContext('2d');
const W = cv.width, H = cv.height, GY = 310;
let frame = 0;
// Dier positie: beweegt langzaam van links naar rechts
let dx = -120, dy = GY - 110, speed = 0.55;

function drawBG() {{
  // Lucht gradient
  const sky = cx.createLinearGradient(0, 0, 0, GY);
  sky.addColorStop(0, '#4a8fc5');
  sky.addColorStop(0.55, '#9dc8e8');
  sky.addColorStop(1, '#f0d080');
  cx.fillStyle = sky; cx.fillRect(0, 0, W, GY);

  // Zon
  cx.save();
  cx.shadowColor = '#FFD700'; cx.shadowBlur = 30;
  cx.beginPath(); cx.arc(W - 80, 65, 38, 0, Math.PI * 2);
  cx.fillStyle = '#FFD700'; cx.fill();
  cx.restore();
  cx.beginPath(); cx.arc(W - 80, 65, 26, 0, Math.PI * 2);
  cx.fillStyle = '#FFF9C4'; cx.fill();

  // Wolkjes
  [[120,55],[300,40],[480,70]].forEach(([x,y]) => {{
    cx.fillStyle = 'rgba(255,255,255,0.55)';
    cx.beginPath(); cx.ellipse(x, y, 38, 16, 0, 0, Math.PI*2); cx.fill();
    cx.beginPath(); cx.ellipse(x-22, y+6, 22, 12, 0, 0, Math.PI*2); cx.fill();
    cx.beginPath(); cx.ellipse(x+24, y+4, 26, 13, 0, 0, Math.PI*2); cx.fill();
  }});

  // Verre heuvels
  cx.fillStyle = 'rgba(100,140,70,0.35)';
  [[80,130],[280,100],[500,120],[650,110]].forEach(([x,r]) => {{
    cx.beginPath(); cx.ellipse(x, GY, r, r * 0.42, 0, Math.PI, 0); cx.fill();
  }});

  // Bomen (acacia stijl)
  [[90,GY],[210,GY-8],[400,GY],[530,GY-4],[620,GY]].forEach(([tx,ty]) => {{
    // stam
    cx.fillStyle = '#5a3010';
    cx.fillRect(tx - 5, ty - 80, 10, 80);
    // kroon plat (acacia)
    cx.fillStyle = 'rgba(55,100,25,0.82)';
    cx.beginPath(); cx.ellipse(tx, ty - 80, 50, 18, 0, 0, Math.PI*2); cx.fill();
    cx.beginPath(); cx.ellipse(tx - 28, ty - 72, 26, 14, -0.2, 0, Math.PI*2); cx.fill();
    cx.beginPath(); cx.ellipse(tx + 30, ty - 70, 28, 15, 0.2, 0, Math.PI*2); cx.fill();
  }});

  // Grond
  const ground = cx.createLinearGradient(0, GY, 0, H);
  ground.addColorStop(0, '#C8A440');
  ground.addColorStop(0.3, '#A87E30');
  ground.addColorStop(1, '#6B4810');
  cx.fillStyle = ground; cx.fillRect(0, GY, W, H - GY);

  // Grasjes
  cx.strokeStyle = '#8B6914'; cx.lineWidth = 1.8;
  for (let gx = 8; gx < W; gx += 22) {{
    const o = (frame * 0.25 + gx) % W;
    cx.beginPath(); cx.moveTo(o, GY); cx.lineTo(o - 4, GY - 11); cx.stroke();
    cx.beginPath(); cx.moveTo(o + 9, GY); cx.lineTo(o + 12, GY - 8); cx.stroke();
  }}

  // Stofspoor onder dier
  if (dx > 30) {{
    const stof = cx.createRadialGradient(dx - 40, dy + 110, 5, dx - 40, dy + 110, 55);
    stof.addColorStop(0, 'rgba(180,140,60,0.35)');
    stof.addColorStop(1, 'rgba(180,140,60,0)');
    cx.fillStyle = stof; cx.fillRect(dx - 100, dy + 70, 130, 55);
  }}
}}

function drawDier() {{
  // Schaduw
  cx.fillStyle = 'rgba(0,0,0,0.18)';
  cx.beginPath(); cx.ellipse(dx, dy + 118, 68, 16, 0, 0, Math.PI*2); cx.fill();

  // Dier emoji groot
  const bob = Math.sin(frame * 0.08) * 4;
  cx.font = '110px serif';
  cx.textAlign = 'center';
  cx.fillText(HUIDIG.e, dx, dy + bob + 100);

  // Detectie box (groen) als dier in beeld
  if (dx > 80 && dx < W - 80) {{
    cx.strokeStyle = '#00ff44'; cx.lineWidth = 2.5; cx.setLineDash([7, 4]);
    cx.strokeRect(dx - 70, dy - 8, 140, 140);
    cx.setLineDash([]);
    cx.fillStyle = 'rgba(0,255,68,0.06)';
    cx.fillRect(dx - 70, dy - 8, 140, 140);

    // Label achtergrond
    const pct = Math.round(HUIDIG.conf * 100);
    const lbl = HUIDIG.n + '  ' + pct + '%';
    const tw = cx.measureText(lbl).width;
    cx.font = 'bold 13px monospace';
    const tw2 = cx.measureText(lbl).width + 20;
    cx.fillStyle = 'rgba(0,0,0,0.75)';
    cx.beginPath();
    if (cx.roundRect) cx.roundRect(dx - tw2/2, dy - 36, tw2, 26, 5);
    else cx.rect(dx - tw2/2, dy - 36, tw2, 26);
    cx.fill();
    cx.fillStyle = '#00ff44'; cx.textAlign = 'center';
    cx.fillText(lbl, dx, dy - 18);

    // Hoekmarkeringen
    const corners = [[dx-70,dy-8],[dx+70,dy-8],[dx-70,dy+132],[dx+70,dy+132]];
    cx.strokeStyle = '#00ff44'; cx.lineWidth = 3; cx.setLineDash([]);
    corners.forEach(([cx2, cy2], i) => {{
      cx.beginPath();
      const sx = i % 2 === 0 ? 1 : -1, sy = i < 2 ? 1 : -1;
      cx.moveTo(cx2, cy2 + sy * 16); cx.lineTo(cx2, cy2); cx.lineTo(cx2 + sx * 16, cy2);
      cx.stroke();
    }});
  }}
}}

function drawHUD() {{
  // Bovenste balk
  cx.fillStyle = 'rgba(0,0,0,0.68)'; cx.fillRect(0, 0, W, 30);
  cx.fillStyle = frame % 60 < 30 ? '#ff3333' : '#991111';
  cx.font = 'bold 12px monospace'; cx.textAlign = 'left';
  cx.fillText('● REC', 9, 20);
  cx.fillStyle = 'white';
  cx.fillText('CAM SAV-001  |  SERENGETI N.P.  |  AI WILDLIFE DETECTIE', 60, 20);
  cx.textAlign = 'right';
  cx.fillText(new Date().toLocaleTimeString('nl-BE'), W - 10, 20);

  // Onderste balk
  cx.fillStyle = 'rgba(0,0,0,0.62)'; cx.fillRect(0, H - 28, W, 28);
  const inZone = dx > 80 && dx < W - 80;
  cx.fillStyle = inZone ? '#00ff88' : '#aaaaaa';
  cx.font = 'bold 12px monospace'; cx.textAlign = 'left';
  const statusMsg = inZone
    ? '>> DIER GEDETECTEERD: ' + HUIDIG.n.toUpperCase() + ' (' + Math.round(HUIDIG.conf*100) + '% zekerheid)'
    : '   Scanning voor wildlife...';
  cx.fillText(statusMsg, 12, H - 9);
  cx.textAlign = 'right'; cx.fillStyle = '#777'; cx.font = '10px monospace';
  cx.fillText('Teachable Machine v2.0', W - 10, H - 9);
  cx.textAlign = 'left';
}}

function loop() {{
  frame++;
  dx += speed;
  if (dx > W + 150) dx = -150;
  drawBG(); drawDier(); drawHUD();
  requestAnimationFrame(loop);
}}
loop();
</script>
"""
            st.components.v1.html(CANVAS_HTML, height=440, scrolling=False)

            # Detectie melding
            if st.session_state.laatste_detectie:
                det = st.session_state.laatste_detectie
                st.success(f"✅ GEDETECTEERD: **{det['dier_key']}** — {det['zekerheid']*100:.1f}% zekerheid")
        else:
            st.warning("⏸️ Feed gepauzeerd.")

        st.markdown("---")
        with st.expander("📷 Teachable Machine — Handmatige Detectie"):
            tm_model, tm_labels = laad_tm_model()
            if tm_model is not None:
                cam_foto = st.camera_input("Neem een foto om een dier te herkennen", key="tm_cam")
                if cam_foto is not None:
                    foto_hash = hashlib.md5(cam_foto.getvalue()).hexdigest()
                    if foto_hash != st.session_state.laatste_foto_hash:
                        st.session_state.laatste_foto_hash = foto_hash
                        afbeelding = Image.open(cam_foto)
                        dier_naam, zekerheid = classificeer_afbeelding(tm_model, tm_labels, afbeelding)
                        dier_key = None
                        for tm_l, app_l in TM_NAAR_DIER.items():
                            if tm_l.lower() in dier_naam.lower():
                                dier_key = app_l
                                break
                        if dier_key and zekerheid > 0.5:
                            st.session_state.dieren_vandaag[dier_key] = st.session_state.dieren_vandaag.get(dier_key, 0) + 1
                            st.session_state.totaal += 1
                            st.success(f"✅ TM Herkend: **{dier_key}** ({zekerheid*100:.1f}%)")
                        else:
                            st.warning(f"⚠️ Onzeker: {dier_naam} ({zekerheid*100:.1f}%)")
            else:
                st.info("ℹ️ Plaats `keras_model.h5` en `labels.txt` in de projectmap.")

        with st.expander("📁 Upload cameraopname voor analyse"):
            uploaded = st.file_uploader("Kies een afbeelding", type=["jpg","jpeg","png"], label_visibility="collapsed")
            if uploaded:
                st.image(uploaded, caption="📸 Geüploade opname", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            if st.button("▶️ Hervat Feed" if st.session_state.detectie_gepauzeerd else "⏸️ Pauzeer Feed", key="btn_feed"):
                st.session_state.detectie_gepauzeerd = not st.session_state.detectie_gepauzeerd
                st.session_state.feed_huidig_dier = None
                st.rerun()
        with b2:
            if st.button("🔄 Reset Tellers", key="btn_reset"):
                st.session_state.dieren_vandaag = {k: 0 for k in st.session_state.dieren_vandaag}
                st.session_state.totaal = 0
                st.session_state.laatste_detectie = None
                st.session_state.feed_huidig_dier = None
                st.rerun()

    # ── Rechter kolom: live dierenlijst ─────────────────────────────────────
    with col_rechts:
        # Huidig dier banner
        if not st.session_state.detectie_gepauzeerd and huidig_key:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(0,200,80,0.14),rgba(45,138,75,0.07));
                border:2.5px solid {ACCENT_GROEN};border-radius:18px;padding:18px 22px;margin-bottom:16px;
                display:flex;align-items:center;gap:16px;">
                <span style="font-size:54px;line-height:1;filter:drop-shadow(0 3px 6px rgba(0,0,0,0.2));">{huidig_emoji}</span>
                <div>
                    <div style="font-size:10px;font-weight:800;letter-spacing:2px;color:{ACCENT_GROEN};text-transform:uppercase;margin-bottom:2px;">&#11044; Nu in beeld</div>
                    <div style="font-size:26px;font-weight:900;color:{TEKST};font-family:'Playfair Display',serif;line-height:1.1;">{huidig_naam}</div>
                    <div style="font-size:13px;color:{SUBTEKST};margin-top:4px;">AI zekerheid: <strong style="color:{ACCENT_ORANJE};">{conf*100:.1f}%</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.laatste_detectie:
            det = st.session_state.laatste_detectie
            em = det['dier_key'].split(' ')[-1]
            nm = det['dier_key'].split(' ')[0]
            st.markdown(f"""
            <div style="background:rgba(0,0,0,0.04);border:2px solid {RAND};border-radius:18px;padding:18px 22px;margin-bottom:16px;
                display:flex;align-items:center;gap:16px;">
                <span style="font-size:54px;line-height:1;opacity:0.5;">{em}</span>
                <div>
                    <div style="font-size:10px;font-weight:800;letter-spacing:2px;color:{SUBTEKST};text-transform:uppercase;margin-bottom:2px;">Laatste detectie</div>
                    <div style="font-size:22px;font-weight:900;color:{SUBTEKST};font-family:'Playfair Display',serif;">{nm}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f'<div class="savanna-card"><h3>&#x1F43E; Geobserveerde Dieren Vandaag</h3></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        for dier, aantal in sorted(st.session_state.dieren_vandaag.items(), key=lambda x: x[1], reverse=True):
            gist  = DIEREN_GISTEREN.get(dier, 0)
            week  = DIEREN_VORIGE_WEEK.get(dier, 0)
            maand = DIEREN_VORIGE_MAAND.get(dier, 0)
            d_gist  = aantal - gist
            d_week  = aantal - week
            d_maand = aantal - maand
            # Highlight het dier dat nu in beeld is
            is_actief = (dier == huidig_key and not st.session_state.detectie_gepauzeerd)
            border_stijl = f"border-color:{ACCENT_GROEN};background:rgba(45,138,75,0.08);" if is_actief else ""
            pijl_g = "🔺" if d_gist > 0 else "🔻" if d_gist < 0 else "➡️"
            pijl_w = "🔺" if d_week > 0 else "🔻" if d_week < 0 else "➡️"
            pijl_m = "🔺" if d_maand > 0 else "🔻" if d_maand < 0 else "➡️"
            st.markdown(f"""
            <div class="dier-observatie-rij" style="{border_stijl}">
                <span style="font-size:24px;min-width:36px;">{dier.split(" ")[-1]}</span>
                <span style="font-weight:700;flex:1;font-size:14px;{"color:"+ACCENT_GROEN+";" if is_actief else ""}">{dier.split(" ")[0]}</span>
                <span style="font-weight:900;color:{ACCENT_ORANJE};font-size:20px;min-width:34px;">{aantal}</span>
                <div style="display:flex;flex-direction:column;gap:1px;font-size:11px;color:{SUBTEKST};">
                    <span>{pijl_g} {'+' if d_gist>0 else ''}{d_gist} vs gist</span>
                    <span>{pijl_w} {'+' if d_week>0 else ''}{d_week} vs week</span>
                    <span>{pijl_m} {'+' if d_maand>0 else ''}{d_maand} vs maand</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Auto-refresh elke 12 seconden zodat Python de teller bijwerkt
    if not st.session_state.detectie_gepauzeerd:
        time.sleep(12)
        st.rerun()

# ─────────────────────────────────────────────
# STATISTIEKEN
# ─────────────────────────────────────────────
elif "Statistieken" in pagina:
    st.markdown(f'<h2 style="font-family:Playfair Display,serif;color:{TEKST};">📈 Gedetailleerde Statistieken</h2>', unsafe_allow_html=True)

    df_v = pd.DataFrame(list(st.session_state.uurdata.items()), columns=["Uur","Vandaag"])
    df_g = pd.DataFrame(list(UURDATA_GISTEREN.items()), columns=["Uur","Gisteren"])
    df_w = pd.DataFrame(list(UURDATA_VORIGE_WEEK.items()), columns=["Uur","Vorige Week"])
    df_m = pd.DataFrame(list(UURDATA_VORIGE_MAAND.items()), columns=["Uur","Vorige Maand"])
    df = df_v.merge(df_g, on="Uur").merge(df_w, on="Uur").merge(df_m, on="Uur").set_index("Uur")
    st.bar_chart(df, color=["#E84E0F","#FFCDB8","#D4890A","#a0c4a0"])

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📋 Uurdata")
        st.dataframe(df.reset_index(), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("#### 📊 Samenvatting")
        tg = sum(UURDATA_GISTEREN.values())
        tw = sum(UURDATA_VORIGE_WEEK.values())
        tm_ = sum(UURDATA_VORIGE_MAAND.values())
        st.metric("Totaal vandaag", st.session_state.totaal)
        st.metric("Totaal gisteren", tg, delta=f"{'+' if (st.session_state.totaal-tg)>=0 else ''}{st.session_state.totaal-tg}")
        st.metric("Vorige week", tw, delta=f"{'+' if (st.session_state.totaal-tw)>=0 else ''}{st.session_state.totaal-tw}")
        st.metric("Vorige maand", tm_, delta=f"{'+' if (st.session_state.totaal-tm_)>=0 else ''}{st.session_state.totaal-tm_}")
        st.metric("Piekuur", max(st.session_state.uurdata, key=st.session_state.uurdata.get))

    st.markdown("---")
    st.markdown("#### 🐾 Dierenobservaties Vergelijking")
    dieren_df = pd.DataFrame({
        "Vandaag": st.session_state.dieren_vandaag,
        "Gisteren": DIEREN_GISTEREN,
        "Vorige Week": DIEREN_VORIGE_WEEK,
        "Vorige Maand": DIEREN_VORIGE_MAAND,
    })
    st.bar_chart(dieren_df, color=["#E84E0F","#FFCDB8","#D4890A","#a0c4a0"])

# ─────────────────────────────────────────────
# INFORMATIE — De Cheeta
# ─────────────────────────────────────────────
elif "Informatie" in pagina:
    st.markdown(f"""
    <div style="text-align:center;padding:30px 0 10px;">
        <div style="font-size:64px;line-height:1;">🐆</div>
        <h1 style="font-family:'Playfair Display',serif;color:#E84E0F;font-size:38px;font-weight:900;margin:12px 0 4px;">De Cheeta</h1>
        <p style="color:{SUBTEKST};font-size:16px;font-style:italic;">Acinonyx jubatus — Het snelste landdier ter wereld</p>
        <div style="display:inline-block;background:rgba(232,78,15,0.12);border:1.5px solid #E84E0F;border-radius:20px;padding:6px 20px;margin-top:10px;">
            <span style="color:#E84E0F;font-weight:800;font-size:14px;">⚠️ KWETSBAAR — IUCN Rode Lijst</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Cheeta foto (svg) embedded als data-URI zodat het altijd laadt op Streamlit Cloud
    st.markdown(
        svg_img_tag(CHEETAH_IMAGE_URL, "width:100%;height:auto;display:block;max-width:900px;margin:0 auto;"),
        unsafe_allow_html=True,
    )
    st.caption("📸 Cheeta (Acinonyx jubatus) — illustratie")

    st.markdown("---")

    feiten = [
        {"titel": "🏃 Topsnelheid", "waarde": "112 km/u", "info": "De cheeta kan in slechts 3 seconden van 0 naar 100 km/u accelereren — sneller dan de meeste sportauto's.", "kleur": "#E84E0F"},
        {"titel": "📏 Lengte & Gewicht", "waarde": "1,2–1,5 m / 21–72 kg", "info": "Cheetahs zijn slanker en lichter gebouwd dan leeuwen of luipaarden, wat bijdraagt aan hun snelheid.", "kleur": "#D4890A"},
        {"titel": "🌍 Leefgebied", "waarde": "Afrika & Iran", "info": "Vroeger verspreid over heel Afrika en Azië, nu enkel in sub-Sahara Afrika en een kleine populatie in Iran.", "kleur": "#2d6a2d"},
        {"titel": "😢 Populatie", "waarde": "~7.100 dieren", "info": "De wereldpopulatie is drastisch gekrompen door habitatverlies, menselijke conflicten en illegale handel.", "kleur": "#8B4513"},
        {"titel": "🍖 Voeding", "waarde": "Carnivoor", "info": "Cheetahs jagen op gazellen, hazen en andere kleine tot middelgrote zoogdieren — overdag, niet 's nachts.", "kleur": "#C4700A"},
        {"titel": "👶 Welpen", "waarde": "3–5 per worp", "info": "Welpen worden blind geboren en hebben een grijze mantel die hen doet lijken op de honigdas — een afschrikkende mimicry.", "kleur": "#E84E0F"},
    ]

    cols = st.columns(3)
    for i, feit in enumerate(feiten):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="dier-card" style="border-top: 4px solid {feit['kleur']}; margin-bottom: 20px;">
                <h3 style="font-family:'Playfair Display',serif;font-size:16px;font-weight:700;margin:0 0 8px;">{feit['titel']}</h3>
                <div style="font-size:22px;font-weight:900;color:{feit['kleur']};margin:8px 0 12px;">{feit['waarde']}</div>
                <p style="font-size:13px;line-height:1.6;margin:0;">{feit['info']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown(f"""
        <div class="savanna-card">
            <h3>⚠️ Belangrijkste Bedreigingen</h3>
            <ul style="margin:0;padding-left:20px;line-height:2;font-size:14px;">
                <li><strong>Habitatverlies</strong> — landbouw en bebouwing versnipperen het leefgebied</li>
                <li><strong>Menselijk conflict</strong> — veehouders doden cheetahs ter bescherming</li>
                <li><strong>Illegale handel</strong> — welpen worden gestolen voor de zwarte markt</li>
                <li><strong>Klimaatverandering</strong> — droogte treft prooidieren en ecosystemen</li>
                <li><strong>Inteelt</strong> — lage genetische diversiteit maakt de soort kwetsbaar</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_r:
        st.markdown(f"""
        <div class="savanna-card">
            <h3>💚 Hoe kun jij helpen?</h3>
            <ul style="margin:0;padding-left:20px;line-height:2;font-size:14px;">
                <li><strong>Doneer</strong> aan Cheetah Conservation Fund (CCF)</li>
                <li><strong>Bewustzijn</strong> — deel informatie over de bedreigingen</li>
                <li><strong>Koop duurzaam</strong> — kies producten zonder ontbossing</li>
                <li><strong>Adopteer een cheeta</strong> via erkende organisaties</li>
                <li><strong>Bezoek verantwoord</strong> — kies ethisch ecotoerisme</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:24px;background:rgba(232,78,15,0.06);border-radius:16px;border:1.5px solid rgba(232,78,15,0.2);margin-top:20px;">
        <p style="font-size:15px;margin:0;">🌍 <strong style="color:#E84E0F;">Geweten weetje:</strong> In 1900 leefden er nog <strong>100.000 cheetahs</strong> op aarde. Vandaag zijn dat er minder dan 7.100. Elke dag telt!</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SPEL — Redde de Cheeta!
# ─────────────────────────────────────────────
elif "Spel" in pagina:
    st.markdown(f"""
    <div style="text-align:center;padding:10px 0 20px;">
        <h1 style="font-family:'Playfair Display',serif;color:#E84E0F;font-size:30px;font-weight:900;">🧍 Red de Cheeta!</h1>
        <p style="color:{SUBTEKST};">Beweeg met ← → en spring met ↑ of Spatie over hindernissen om de cheeta te bereiken!</p>
    </div>
    """, unsafe_allow_html=True)

    st.components.v1.html("""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: linear-gradient(180deg, #f5deb3 0%, #daa520 100%);
    display:flex; flex-direction:column; align-items:center;
    font-family:'Georgia',serif; padding:10px;
  }
  canvas { display:block; border-radius:16px; border:3px solid #E84E0F; box-shadow:0 8px 32px rgba(0,0,0,0.3); }
  #ui { display:flex; gap:20px; align-items:center; margin-bottom:10px; background:rgba(255,255,255,0.88); border-radius:12px; padding:7px 18px; border:2px solid #E84E0F; }
  #score { font-size:19px; font-weight:800; color:#E84E0F; }
  #level { font-size:14px; font-weight:700; color:#555; background:white; padding:4px 13px; border-radius:20px; border:2px solid #E84E0F; }
  #lives { font-size:19px; }
  button {
    background:linear-gradient(135deg,#E84E0F,#D4890A); color:white; border:none;
    padding:12px 36px; border-radius:12px; font-size:17px; font-weight:800;
    cursor:pointer; margin-top:12px; font-family:'Georgia',serif;
    box-shadow:0 4px 16px rgba(232,78,15,0.4); transition:all 0.2s;
  }
  button:hover { background:linear-gradient(135deg,#c43d08,#b87508); transform:translateY(-2px); }
  #hint { font-size:12px; color:#666; margin-top:5px; }
</style>
</head>
<body>
<div id="ui">
  <span id="score">Score: 0</span>
  <span id="level">Level 1</span>
  <span id="lives">❤️❤️❤️</span>
</div>
<canvas id="c" width="620" height="390"></canvas>
<button id="btn" onclick="startGame()">▶ Start Spel</button>
<div id="hint">← → bewegen &nbsp;|&nbsp; ↑ of Spatie = springen</div>
<script>
const cv = document.getElementById('c');
const cx = cv.getContext('2d');
const ACC = '#E84E0F';
const GY  = 310;

let pl, obs, score, level, lives, spd, running, aid, spawnT, fc;

function init() {
  pl = { x:55, y:GY-44, w:28, h:44, sx:5.5, vy:0, ground:true };
  obs=[]; score=0; level=1; lives=3; spd=2.6; spawnT=0; fc=0; running=false;
}
init();

const keys={};
document.addEventListener('keydown', e=>{ keys[e.key]=true; if([' ','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)) e.preventDefault(); });
document.addEventListener('keyup',   e=>{ keys[e.key]=false; });

const OBS=['🪨','🌵','🪵','🦂','🐍'];

function spawnObs(){
  const h=26+Math.floor(Math.random()*20);
  obs.push({x:cv.width+10, y:GY-h+8, w:30, h, emoji:OBS[Math.floor(Math.random()*OBS.length)], sx:spd+Math.random()*1.1});
}

function drawBG(){
  // Lucht
  const g=cx.createLinearGradient(0,0,0,GY);
  g.addColorStop(0,'#6ab4e8'); g.addColorStop(1,'#ffd97d');
  cx.fillStyle=g; cx.fillRect(0,0,cv.width,GY);
  // Zon
  cx.beginPath(); cx.arc(530,55,32,0,Math.PI*2);
  cx.fillStyle='#FFD700'; cx.fill();
  cx.beginPath(); cx.arc(530,55,24,0,Math.PI*2);
  cx.fillStyle='#FFF176'; cx.fill();
  // Heuvels
  cx.fillStyle='rgba(180,140,60,0.28)';
  [[90,130],[280,95],[460,120]].forEach(([cx2,r])=>{
    cx.beginPath(); cx.ellipse(cx2,GY,r,r*0.5,0,Math.PI,0); cx.fill();
  });
  // Grond
  const gg=cx.createLinearGradient(0,GY,0,cv.height);
  gg.addColorStop(0,'#C8A040'); gg.addColorStop(0.4,'#A07828'); gg.addColorStop(1,'#6B4A10');
  cx.fillStyle=gg; cx.fillRect(0,GY,cv.width,cv.height-GY);
  // Grasjes
  cx.strokeStyle='#8B6914'; cx.lineWidth=1.8;
  for(let gx=15;gx<cv.width;gx+=38){
    const o=(fc*0.45+gx)%(cv.width+38)-18;
    cx.beginPath(); cx.moveTo(o,GY); cx.lineTo(o-3,GY-9); cx.stroke();
    cx.beginPath(); cx.moveTo(o+7,GY); cx.lineTo(o+10,GY-7); cx.stroke();
  }
  // Randen
  cx.strokeStyle=ACC; cx.lineWidth=3.5;
  cx.beginPath(); cx.moveTo(14,0); cx.lineTo(14,cv.height); cx.stroke();
  cx.beginPath(); cx.moveTo(cv.width-14,0); cx.lineTo(cv.width-14,cv.height); cx.stroke();
}

function drawCheeta(bob){
  cx.font='42px serif'; cx.textAlign='center';
  const by=bob ? Math.sin(fc*0.1)*3 : 0;
  cx.fillText('🐆', cv.width-38, GY-4+by);
  cx.fillStyle=ACC; cx.font='bold 10px Georgia'; cx.textAlign='center';
  cx.fillText('Red mij!', cv.width-38, GY-50);
}

function drawPlayer(){
  const p=pl;
  const as=p.ground ? Math.sin(fc*0.24)*7 : 0;
  const ls=p.ground ? Math.sin(fc*0.24)*5 : 0;
  // hoofd
  cx.fillStyle='#FFDAB9';
  cx.beginPath(); cx.arc(p.x+p.w/2, p.y+10, 9, 0, Math.PI*2); cx.fill();
  cx.strokeStyle='#8B4513'; cx.lineWidth=1.2; cx.stroke();
  // ogen
  cx.fillStyle='#333';
  cx.beginPath(); cx.arc(p.x+p.w/2-2.5, p.y+9, 1.8, 0, Math.PI*2); cx.fill();
  cx.beginPath(); cx.arc(p.x+p.w/2+2.5, p.y+9, 1.8, 0, Math.PI*2); cx.fill();
  // lichaam
  cx.fillStyle=ACC; cx.fillRect(p.x+6, p.y+19, 16, 19);
  // armen
  cx.fillStyle='#FFDAB9';
  cx.fillRect(p.x+1,  p.y+21+as, 6, 9);
  cx.fillRect(p.x+21, p.y+21-as, 6, 9);
  // benen
  cx.fillStyle='#4a2800';
  cx.fillRect(p.x+6,  p.y+38+ls, 7, 11);
  cx.fillRect(p.x+15, p.y+38-ls, 7, 11);
  // schoenen
  cx.fillStyle='#222';
  cx.fillRect(p.x+4,  p.y+48+ls, 10, 4);
  cx.fillRect(p.x+14, p.y+48-ls, 10, 4);
}

function drawObs(){
  cx.font='27px serif'; cx.textAlign='center';
  obs.forEach(o=>cx.fillText(o.emoji, o.x+o.w/2, o.y+o.h));
}

function drawHUD(){
  cx.fillStyle='rgba(0,0,0,0.42)';
  cx.beginPath();
  if(cx.roundRect) cx.roundRect(9,9,160,32,7); else cx.rect(9,9,160,32);
  cx.fill();
  cx.fillStyle=ACC; cx.font='bold 16px Georgia'; cx.textAlign='left';
  cx.fillText('Score: '+score, 18, 30);
  // voortgangsbalk
  const pw=cv.width-36;
  cx.fillStyle='rgba(0,0,0,0.28)'; cx.fillRect(18,cv.height-18,pw,7);
  const pr=Math.min(score/50,1);
  cx.fillStyle=ACC; cx.fillRect(18,cv.height-18,pw*pr,7);
  cx.font='9px Georgia'; cx.fillStyle='white'; cx.textAlign='center';
  cx.fillText(Math.round(pr*100)+'% — Cheeta bijna bereikt!', cv.width/2, cv.height-22);
}

function hit(a,b){ return a.x+5<b.x+b.w-3 && a.x+a.w-5>b.x+3 && a.y+19<b.y+b.h && a.y+a.h>b.y+5; }
function updUI(){ document.getElementById('lives').textContent='❤️'.repeat(lives)+'🖤'.repeat(3-lives); document.getElementById('level').textContent='Level '+level; document.getElementById('score').textContent='Score: '+score; }

function gameOver(){
  running=false; cancelAnimationFrame(aid);
  drawBG();
  cx.fillStyle='rgba(0,0,0,0.72)'; cx.fillRect(0,0,cv.width,cv.height);
  cx.fillStyle=ACC; cx.font='bold 38px Georgia'; cx.textAlign='center';
  cx.fillText('💀 GAME OVER', cv.width/2, 145);
  cx.fillStyle='white'; cx.font='bold 20px Georgia';
  cx.fillText('De cheeta kon niet gered worden...', cv.width/2, 192);
  cx.fillText('Score: '+score+' | Level: '+level, cv.width/2, 225);
  cx.fillStyle='#ccc'; cx.font='15px Georgia';
  cx.fillText('Klik Opnieuw voor nog een poging!', cv.width/2, 265);
  document.getElementById('btn').textContent='🔄 Opnieuw';
}

function gameWon(){
  running=false; cancelAnimationFrame(aid);
  drawBG();
  cx.fillStyle='rgba(0,0,0,0.68)'; cx.fillRect(0,0,cv.width,cv.height);
  cx.fillStyle='#FFD700'; cx.font='bold 34px Georgia'; cx.textAlign='center';
  cx.fillText('🎉 CHEETA GERED! 🎉', cv.width/2, 138);
  cx.fillStyle='white'; cx.font='bold 19px Georgia';
  cx.fillText('Geweldig! Je hebt de cheeta bereikt!', cv.width/2, 184);
  cx.fillText('Eindscore: '+score+' | Level: '+level, cv.width/2, 218);
  cx.fillStyle='#ccc'; cx.font='14px Georgia';
  cx.fillText('Speel opnieuw om je score te verbeteren!', cv.width/2, 258);
  document.getElementById('btn').textContent='🔄 Opnieuw';
}

let flashMsg='', flashT=0;
function flashLevel(){
  flashMsg='⬆️ LEVEL '+level+'!'; flashT=80;
  (function fl(){ if(flashT-->0){ cx.fillStyle='rgba(232,78,15,'+flashT/80+')'; cx.font='bold 36px Georgia'; cx.textAlign='center'; cx.fillText(flashMsg,cv.width/2,cv.height/2); requestAnimationFrame(fl); } })();
}

function loop(){
  if(!running) return;
  fc++;
  if((keys['ArrowLeft']||keys['a'])&&pl.x>16) pl.x-=pl.sx;
  if((keys['ArrowRight']||keys['d'])&&pl.x<cv.width-pl.w-16) pl.x+=pl.sx;
  if((keys['ArrowUp']||keys['w']||keys[' '])&&pl.ground){ pl.vy=-13; pl.ground=false; }
  pl.vy+=0.55; pl.y+=pl.vy;
  if(pl.y>=GY-pl.h){ pl.y=GY-pl.h; pl.vy=0; pl.ground=true; }
  spawnT++;
  if(spawnT>=Math.max(40,90-level*6)){ spawnObs(); spawnT=0; }
  obs.forEach(o=>o.x-=o.sx);
  obs=obs.filter(o=>{
    if(hit(pl,o)){ lives--; updUI(); if(lives<=0){gameOver();return false;} pl.x=55; return false; }
    if(o.x<-50){score++;updUI();return false;}
    return true;
  });
  if(score>=50){gameWon();return;}
  if(score>0&&score%10===0&&score/10>level-1){ level++; spd=2.6+level*0.7; updUI(); flashLevel(); }
  drawBG(); drawCheeta(true); drawObs(); drawPlayer(); drawHUD();
  aid=requestAnimationFrame(loop);
}

function startGame(){
  cancelAnimationFrame(aid); init(); running=true; updUI();
  document.getElementById('btn').textContent='🔄 Herstart';
  loop();
}

// Startscherm
drawBG(); drawCheeta(false);
cx.fillStyle='rgba(0,0,0,0.62)'; cx.fillRect(0,0,cv.width,cv.height);
cx.font='bold 32px Georgia'; cx.fillStyle=ACC; cx.textAlign='center';
cx.fillText('🐆 Red de Cheeta!', cv.width/2, 138);
cx.font='16px Georgia'; cx.fillStyle='white';
cx.fillText('Beweeg met ← → en spring met ↑ / Spatie', cv.width/2, 185);
cx.fillStyle='#ddd'; cx.font='13px Georgia';
cx.fillText('Ontwijkt rotsen, stekels en gevaar — bereik score 50!', cv.width/2, 220);
</script>
</body>
</html>""", height=520, scrolling=False)

# ─────────────────────────────────────────────
# CREDITS
# ─────────────────────────────────────────────
elif "Credits" in pagina:
    st.markdown("<br>", unsafe_allow_html=True)
    credits_html = textwrap.dedent(f"""
    <div class="credits-card">
        <div style="font-size:72px;margin-bottom:16px;">🤝</div>
        <h1 style="font-family:'Playfair Display',serif;color:#E84E0F;font-size:36px;font-weight:900;margin:0 0 8px;">Een samenwerking van</h1>
        <p style="color:{SUBTEKST};font-size:15px;margin-bottom:40px;">Gemaakt door <strong>Seppe</strong> — in samenwerking met Thomas More &amp; Campus Het Spoor</p>

        <div style="display:flex;justify-content:center;gap:40px;flex-wrap:wrap;margin:20px 0 40px;">

            <div style="background:white;border-radius:20px;padding:32px 40px;border:2px solid #E84E0F;box-shadow:0 4px 20px rgba(232,78,15,0.15);min-width:200px;">
                <div style="color:#E84E0F;font-size:10px;font-weight:900;letter-spacing:2px;text-transform:uppercase;">THOMAS</div>
                <div style="color:#1a1a1a;font-size:38px;font-weight:900;font-family:'Playfair Display',serif;line-height:1;">More</div>
                <p style="color:#555;font-size:13px;margin-top:10px;">Hogeschool<br>Toegepaste Informatica</p>
            </div>

            <div style="background:#1a3a1a;border-radius:20px;padding:32px 40px;border:2px solid #4a9a4a;box-shadow:0 4px 20px rgba(74,154,74,0.2);min-width:200px;">
                <div style="color:#7ecb7e;font-size:10px;font-weight:800;letter-spacing:2px;text-transform:uppercase;">CAMPUS</div>
                <div style="color:white;font-size:26px;font-weight:900;font-family:'Playfair Display',serif;line-height:1.2;">Het Spoor</div>
                <div style="color:#a0d0a0;font-size:13px;margin-top:6px;">Mol</div>
            </div>

        </div>

        <p style="color:{SUBTEKST};font-size:13px;margin-top:20px;">
            📍 Thomas More Hogeschool — Campus Het Spoor, Mol<br>
            Toegepaste Informatica · Fase 6 · {datetime.datetime.now().year}
        </p>
    </div>
    """).strip()

    st.markdown(credits_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INSTELLINGEN
# ─────────────────────────────────────────────
elif "Instellingen" in pagina:
    st.markdown(f'<h2 style="font-family:Playfair Display,serif;color:{TEKST};">⚙️ Instellingen</h2>', unsafe_allow_html=True)
    st.markdown("#### 📷 Camera")
    st.text_input("Camera ID",  value="SAV-001")
    st.text_input("Locatie",    value="Serengeti Nationaal Park")
    st.markdown("#### 🔍 Detectie")
    st.slider("Detectiedrempel (%)", 0, 100, 75)
    st.selectbox("Refresh interval", ["5 seconden", "10 seconden", "30 seconden"])
    st.markdown("#### 🔔 Meldingen")
    st.text_input("E-mailadres voor alerts")
    st.checkbox("Melding bij cheeta-observatie", value=True)
    st.checkbox("Melding bij stroperij-detectie", value=True)
    if st.button("💾 Instellingen opslaan"):
        st.success("✅ Instellingen opgeslagen!")
