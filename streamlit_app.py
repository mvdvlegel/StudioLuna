import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. GEAVANCEERDE STYLING (De volledige Replit look) ---
st.set_page_config(page_title="Studio Luna - Mama Circle", page_icon="🌙", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500&display=swap');

    /* De basis */
    .stApp {
        background: linear-gradient(135deg, #F9F7F5 0%, #F1EDE9 100%);
        font-family: 'Quicksand', sans-serif;
    }

    /* Custom Sidebar met kleurverloop */
    [data-testid="stSidebar"] {
        background-color: #E8EFEB !important;
        border-right: 1px solid #D1DBD4;
    }

    /* De Leskaarten (Soft UI / Glassmorphism) */
    .lesson-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 24px;
        border: 1px solid rgba(200, 168, 150, 0.2);
        box-shadow: 10px 10px 20px #ebe8e5, -10px -10px 20px #ffffff;
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    
    .lesson-card:hover {
        transform: translateY(-5px);
    }

    /* Kleuraccenten */
    .sage-text { color: #8FA89B; font-weight: 500; }
    .terra-text { color: #C78D76; font-weight: 600; }
    
    /* Grote titels */
    h1 {
        color: #5F746A !important;
        font-weight: 300 !important;
        letter-spacing: -1px;
    }

    /* Knoppen die eruit 'poppen' */
    div.stButton > button {
        background: #C78D76 !important;
        color: white !important;
        border: none !important;
        padding: 15px 40px !important;
        border-radius: 50px !important;
        box-shadow: 5px 5px 15px rgba(199, 141, 118, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button:hover {
        background: #B67C65 !important;
        box-shadow: 2px 2px 10px rgba(199, 141, 118, 0.5) !important;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA FUNCTIES ---
BASE_URL = "https://docs.google.com/spreadsheets/d/1q3i75-cDz2Y5cAtHHm8E0Cc6qyMH7Q7o0rcn-1F49Fs/export?format=csv"
LESSEN_URL = f"{BASE_URL}&gid=0"
BOEKINGEN_URL = f"{BASE_URL}&gid=1121386221"

@st.cache_data(ttl=10)
def load_data(url):
    return pd.read_csv(url)

# --- 3. SIDEBAR & LOGO ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #8FA89B;'>🌙 Studio Luna</h1>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("GA NAAR", ["✨ Lessenrooster", "🌿 Bibliotheek", "👤 Mijn Account"])
    st.markdown("---")
    st.write("📫 **Contact**")
    st.caption("info@studioluna.nl")

# --- 4. PAGINA'S ---
if menu == "✨ Lessenrooster":
    st.title("Lessenrooster")
    st.markdown("<p class='sage-text'>Vind je moment van rust en verbinding.</p>", unsafe_allow_html=True)
    
    try:
        lessen = load_data(LESSEN_URL)
        # We maken een mooie grid layout
        col1, col2 = st.columns(2)
        
        for i, row in lessen.iterrows():
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                st.markdown(f"""
                    <div class="lesson-card">
                        <h2 style='margin-top:0;'>{row['Naam']}</h2>
                        <p class='terra-text'>📅 {row['Datum']} | ⏰ {row['Tijd']}</p>
                        <p style='color: #666; font-size: 0.9em;'>Kom tot rust in onze warme studio omgeving.</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Reserveer Plekje", key=f"res_{row['ID']}"):
                    st.balloons()
                    st.success("Je aanvraag is verwerkt!")
    except Exception as e:
        st.error("Het rooster kon niet geladen worden.")

elif menu == "🌿 Bibliotheek":
    st.title("Bibliotheek")
    st.markdown("### Audio & Meditatie")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    
    st.markdown("---")
    st.markdown("### Video Lessen")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

elif menu == "👤 Mijn Account":
    st.title("Inloggen")
    st.text_input("E-mailadres")
    st.text_input("Wachtwoord", type="password")
    st.button("Log in")
