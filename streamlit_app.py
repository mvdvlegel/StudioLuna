import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- 1. BRAND IDENTITY & STYLING ---
st.set_page_config(page_title="Studio Luna", page_icon="🌿", layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;1,400&family=Montserrat:wght@300;400;500&display=swap');
    .stApp {{ background-color: #f8f7f5 !important; }}
    [data-testid="stSidebar"] {{ background-color: #e6ddd2 !important; }}
    h1, h2, h3 {{ color: #8fa89b !important; font-family: 'Lora', serif; }}
    p, span, label, li {{ color: #3a4f41 !important; font-family: 'Montserrat', sans-serif; }}
    div.stButton > button {{
        background-color: #c78d76 !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px 30px !important;
    }}
    .lesson-card {{
        background-color: white;
        border-left: 6px solid #c78d76;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 2px 4px 12px rgba(58, 79, 65, 0.05);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA & SESSION STATE ---
BASE_URL = "https://docs.google.com/spreadsheets/d/1q3i75-cDz2Y5cAtHHm8E0Cc6qyMH7Q7o0rcn-1F49Fs/export?format=csv"
LESSEN_URL = f"{BASE_URL}&gid=0"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

@st.cache_data(ttl=60)
def load_data(url):
    return pd.read_csv(url)

# --- 3. NAVIGATIE LOGICA ---
# Definieer welke menu-opties zichtbaar zijn op basis van inlogstatus
if st.session_state.logged_in:
    menu_options = ["🌙 Lessenrooster", "✨ Mijn Tribe", "🌿 Bibliotheek", "🍲 Village Board", "🏷️ Tarieven", "👤 Mijn Account"]
else:
    menu_options = ["🌙 Lessenrooster", "🏷️ Tarieven", "👤 Inloggen"]

with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>Studio Luna</h1>", unsafe_allow_html=True)
    menu = st.radio("MENU", menu_options)
    st.markdown("---")
    if st.session_state.logged_in:
        st.write(f"Welkom, mama {st.session_state.user_email.split('@')[0]}! 🤍")

# --- 4. PAGINA: LESSENROOSTER ---
if menu == "🌙 Lessenrooster":
    st.title("Lessenrooster 🌙")
    try:
        lessen = load_data(LESSEN_URL)
        for _, row in lessen.iterrows():
            st.markdown(f"""
            <div class='lesson-card'>
                <h3>{row['Naam']}</h3>
                <p>📅 {row['Datum']} | ⏰ {row['Tijd']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Alleen boekingsknop tonen als je ingelogd bent
            if st.session_state.logged_in:
                if st.button(f"Reserveer {row['Naam']}", key=f"book_{row['ID']}"):
                    st.success("Gereserveerd! ✨")
                    st.balloons()
            else:
                st.caption("Log in om een plekje te reserveren.")
    except:
        st.error("Rooster kon niet geladen worden.")

# --- 5. PAGINA: INLOGGEN / ACCOUNT ---
elif menu in ["👤 Inloggen", "👤 Mijn Account"]:
    st.title("Mijn Account")
    if not st.session_state.logged_in:
        st.markdown("### Join de mama tribe!")
        email = st.text_input("E-mailadres")
        passw = st.text_input("Wachtwoord", type="password")
        if st.button("Inloggen"):
            # Voor nu simpele inlog, later koppelen we de Users GSheet
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
    else:
        st.write(f"Je bent ingelogd met: **{st.session_state.user_email}**")
        if st.button("Uitloggen"):
            st.session_state.logged_in = False
            st.rerun()

# --- 6. BEVEILIGDE PAGINA'S (Alleen zichtbaar indien ingelogd) ---
elif menu == "✨ Mijn Tribe":
    st.title("Mijn Tribe Feed")
    st.write("Exclusieve updates voor de Circle.")

elif menu == "🌿 Bibliotheek":
    st.title("Mama Reset Bibliotheek")
    st.write("Video's en ademhalingsoefeningen.")

elif menu == "🍲 Village Board":
    st.title("Village Board")
    st.write("De Mealtrain voor mama's in de kraamtijd.")

# --- 7. PAGINA: TARIEVEN ---
elif menu == "🏷️ Tarieven":
    st.title("Tarieven & Pakketten")
    st.markdown("- **Proefles:** €10,-\n- **Losse Credit:** €22,50\n- **The Trimester Journey:** €210,-")
