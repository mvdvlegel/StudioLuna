import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timedelta
import hashlib

# --- 1. BRAND IDENTITY & 6-KLEUREN PALET ---
st.set_page_config(page_title="Studio Luna", page_icon="🌿", layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;1,400&family=Montserrat:wght@300;400;500&display=swap');

    /* 1. Achtergrond (Soft Cloud) */
    .stApp {{ background-color: #f8f7f5 !important; }}

    /* 2. Sidebar (Sand Stone) */
    [data-testid="stSidebar"] {{ background-color: #e6ddd2 !important; }}

    /* 3. Titels (Sage Green) */
    h1, h2, h3 {{ color: #8fa89b !important; font-family: 'Lora', serif; }}

    /* 4. Tekst (Deep Forest) */
    p, span, label, li {{ color: #3a4f41 !important; font-family: 'Montserrat', sans-serif; }}

    /* 5. Knoppen (Terracotta) */
    div.stButton > button {{
        background-color: #c78d76 !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 12px 35px !important;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}

    /* 6. Accent Box (Dusty Rose) */
    .stAlert {{
        background-color: #d5b9b2 !important;
        color: #3a4f41 !important;
        border-radius: 15px !important;
    }}

    /* Leskaarten styling */
    .lesson-card {{
        background-color: white;
        border-left: 6px solid #c78d76;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 2px 4px 12px rgba(58, 79, 65, 0.05);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA VERBINDING ---
# Gebruik de directe CSV export voor snelheid en GSheetsConnection voor schrijven
BASE_URL = "https://docs.google.com/spreadsheets/d/1q3i75-cDz2Y5cAtHHm8E0Cc6qyMH7Q7o0rcn-1F49Fs/export?format=csv"
LESSEN_URL = f"{BASE_URL}&gid=0"
BOEKINGEN_URL = f"{BASE_URL}&gid=1121386221"

@st.cache_data(ttl=60)
def load_data(url):
    return pd.read_csv(url)

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.is_postpartum = False

# --- 4. NAVIGATIE SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>Studio Luna</h1>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("GA NAAR", ["✨ Mijn Tribe", "🌙 Lessenrooster", "🌿 Bibliotheek", "🍲 Village Board", "🏷️ Tarieven", "👤 Mijn Account"])
    st.markdown("---")
    st.markdown("**Onze Circle Codes:**")
    st.caption("• Wat in de Circle wordt gedeeld, blijft er.")
    st.caption("• Luisteren zonder ongevraagd advies.")
    st.caption("• Wees niet bang om hulp te vragen.")

# --- 5. PAGINA: MIJN TRIBE (FEED) ---
if menu == "✨ Mijn Tribe":
    st.title("De Tribe Feed")
    st.info("Welkom bij de digitale thee na de les. Hier deelt de Admin belangrijke updates.")
    
    with st.container():
        st.markdown("""
        <div class='lesson-card'>
            <small>Gisteren 21:00</small>
            <h3>Nagenieten van de les...</h3>
            <p>Wat een mooie verbinding vanavond. De ademrituelen staan voor je klaar in de bibliotheek. Slaap lekker, mama's. 🌿</p>
            <p>❤️ 12 hartjes</p>
        </div>
        """, unsafe_allow_html=True)

# --- 6. PAGINA: LESSENROOSTER ---
elif menu == "🌙 Lessenrooster":
    st.title("Komende Yogalessen")
    st.warning("⚠️ **Annuleren:** Tot uiterlijk 7 uur voor aanvang. Daarna wordt de credit in rekening gebracht.")
    
    try:
        lessen = load_data(LESSEN_URL)
        for _, row in lessen.iterrows():
            st.markdown(f"""
            <div class='lesson-card'>
                <h3>{row['Naam']}</h3>
                <p>📅 {row['Datum']} | ⏰ {row['Tijd']}</p>
                <p><i>Locatie: {row.get('Locatie', 'Studio Luna')}</i></p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Reserveer Plekje", key=f"book_{row['ID']}"):
                if st.session_state.logged_in:
                    st.success("Gereserveerd! ✨")
                    st.balloons()
                else:
                    st.error("Log eerst in via 'Mijn Account' om te boeken.")
    except Exception:
        st.error("Rooster kon niet geladen worden. Controleer je Google Sheet.")

# --- 7. PAGINA: BIBLIOTHEEK ---
elif menu == "🌿 Bibliotheek":
    st.title("Mama Reset Bibliotheek")
    cat = st.selectbox("Categorie", ["Ademrituelen", "Zwangerschapsyoga", "Postpartum Herstel", "Voed je lijf"])
    
    st.markdown(f"### {cat}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Box Breathing**")
        st.write("Adem in (4s), Vast (4s), Uit (4s), Vast (4s).")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    with col2:
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# --- 8. PAGINA: VILLAGE BOARD ---
elif menu == "🍲 Village Board":
    st.title("Village Board (Mealtrain)")
    st.markdown("Alleen de Admin kan een Mealtrain starten. Houd bezoeken kort (max 20 min).")
    
    st.markdown("""
    <div style='background-color: #e6ddd2; padding: 20px; border-radius: 15px;'>
        <h3>🍲 Mealtrain voor Mama Sophie</h3>
        <p><b>Status:</b> Rustmoment (Rust goed uit!) <br>
        <b>Dieetwensen:</b> Geen koemelk, makkelijk opwarmbaar.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ik wil deze week koken"):
        st.success("Wolkje verstuurd! Je ontvangt het adres privé.")

# --- 9. PAGINA: TARIEVEN ---
elif menu == "🏷️ Tarieven":
    st.title("Tarieven & Pakketten")
    st.markdown("""
    - **Proefles:** €10,-
    - **Losse Credit:** €22,50
    - **The First Connection (3 Credits):** €60,- *(Incl. 1 maand app)*
    - **The Growing Tribe (6 Credits):** €115,- *(Incl. 2 maanden app)*
    - **The Trimester Journey (12 Credits):** €210,- *(Incl. 4 maanden app)*
    - **1-op-1 pre- of postnatale yoga:** €80,-
    - **Los Mama Circle App-lidmaatschap:** €6,- per maand
    
    *Strippenkaarten zijn verkrijgbaar in de studio. Na betaling voegen wij je credits toe.*
    """)

# --- 10. PAGINA: MIJN ACCOUNT ---
elif menu == "👤 Mijn Account":
    st.title("Mijn Account")
    if not st.session_state.logged_in:
        email = st.text_input("E-mailadres")
        passw = st.text_input("Wachtwoord", type="password")
        if st.button("Join de mama tribe!"):
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
    else:
        st.write(f"Ingelogd als: {st.session_state.user_email}")
        
        st.markdown("---")
        if not st.session_state.is_postpartum:
            if st.button("✨ IK BEN BEVALLEN! ✨"):
                st.session_state.is_postpartum = True
                st.balloons()
                st.success("Gefeliciteerd mama! 🤍 Rust goed uit en geniet.")
        
        if st.button("Verwijder mijn account"):
            st.warning("Je data wordt verwijderd.")
