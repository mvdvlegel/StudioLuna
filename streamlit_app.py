import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import hashlib
from datetime import datetime

# --- 1. CONFIGURATIE & STYLING (De Studio Luna Look) ---
st.set_page_config(page_title="Studio Luna - Mama Circle", page_icon="🌙", layout="centered")

st.markdown("""
    <style>
    /* Algemene achtergrond */
    .stApp {
        background-color: #F9F7F5;
    }
    
    /* Titels in Sage Green */
    h1, h2, h3 {
        color: #8FA89B !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Leskaarten Styling */
    .lesson-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border-left: 8px solid #C78D76; /* Terracotta */
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    /* Knoppen Styling */
    div.stButton > button:first-child {
        background-color: #C78D76 !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 12px 30px !important;
        font-weight: 500;
        width: 100%;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #E8EFEB !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE VERBINDING ---
# We gebruiken de directe export-methode voor stabiliteit
BASE_URL = "https://docs.google.com/spreadsheets/d/1q3i75-cDz2Y5cAtHHm8E0Cc6qyMH7Q7o0rcn-1F49Fs/export?format=csv"
LESSEN_URL = f"{BASE_URL}&gid=0"
BOEKINGEN_URL = f"{BASE_URL}&gid=1121386221"
USERS_URL = f"{BASE_URL}&gid=1903698065"

@st.cache_data(ttl=10)
def get_data(url):
    return pd.read_csv(url)

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# --- 4. NAVIGATIE ---
with st.sidebar:
    st.title("Studio Luna 🌙")
    page = st.radio("Menu", ["Lessenrooster", "Bibliotheek", "Inloggen / Registreren"])
    st.markdown("---")
    st.info("Tip: Gebruik 2% arrowroot (8g) in de Luna Glow Whip voor de perfecte textuur!")

# --- 5. PAGINA: LESSENROOSTER ---
if page == "Lessenrooster":
    st.title("Lessenrooster 🌙")
    st.markdown("#### *Rust en beweging voor jou*")
    
    try:
        lessen = get_data(LESSEN_URL)
        boekingen = get_data(BOEKINGEN_URL)
        conn = st.connection("gsheets", type=GSheetsConnection)

        for _, row in lessen.iterrows():
            st.markdown(f"""
                <div class="lesson-card">
                    <h3>{row['Naam']}</h3>
                    <p>📅 <b>Datum:</b> {row['Datum']}<br>
                    ⏰ <b>Tijd:</b> {row['Tijd']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.logged_in:
                bezet = len(boekingen[boekingen['Les_ID'].astype(str) == str(row['ID'])])
                over = int(row['Max_Plekken']) - bezet
                st.write(f"✨ **Beschikbare plekken: {over}**")
                
                if over > 0:
                    if st.button(f"Boek {row['Naam']}", key=f"btn_{row['ID']}"):
                        new_booking = pd.DataFrame([{"E-mail": st.session_state.user_email, "Les_ID": str(row['ID']), "Tijdstip": datetime.now().strftime("%d-%m-%Y %H:%M")}])
                        updated = pd.concat([boekingen, new_booking], ignore_index=True)
                        conn.update(worksheet="Boekingen", data=updated)
                        st.success("Gereserveerd! ✨")
                        st.balloons()
                        st.cache_data.clear()
            else:
                st.info("Log in om te reserveren.")

    except Exception as e:
        st.error(f"Rooster kon niet worden geladen: {e}")

# --- 6. PAGINA: BIBLIOTHEEK ---
elif page == "Bibliotheek":
    st.title("Bibliotheek 🌿")
    st.markdown("### *Momentjes voor jezelf*")
    
    tab1, tab2 = st.tabs(["Ademhaling & Audio", "Video's"])
    
    with tab1:
        st.subheader("Oefeningen")
        with st.expander("Box Breathing (4-4-4-4)"):
            st.write("Adem in (4s), Vast (4s), Uit (4s), Vast (4s).")
        
        # Audio placeholder zoals in je ontwerp
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") 
        st.caption("Geleide meditatie voor diepe ontspanning")

    with tab2:
        st.subheader("Video Lessen")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Vervang door je eigen video

# --- 7. PAGINA: ACCOUNT ---
elif page == "Inloggen / Registreren":
    st.title("Mijn Account")
    if not st.session_state.logged_in:
        email = st.text_input("E-mail")
        if st.button("Inloggen"):
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
    else:
        st.write(f"Ingelogd als: {st.session_state.user_email}")
        if st.button("Uitloggen"):
            st.session_state.logged_in = False
            st.rerun()
