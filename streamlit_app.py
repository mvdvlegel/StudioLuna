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
if st.session_state.logged_in:
    menu_options = ["🌙 Lessenrooster", "✨ Mijn Tribe", "🌿 Bibliotheek", "🍲 Village Board", "🏷️ Tarieven", "👤 Mijn Account"]
else:
    menu_options = ["🌙 Lessenrooster", "🏷️ Tarieven", "👤 Inloggen"]

with st.sidebar:
    try:
        st.image("logo.jpeg", use_container_width=True)
    except:
        st.markdown("<h1 style='text-align: center;'>Studio Luna</h1>", unsafe_allow_html=True)
    
    st.markdown("---")
    menu = st.radio("MENU", menu_options)

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
            if st.session_state.logged_in:
                if st.button(f"Reserveer {row['Naam']}", key=f"book_{row['ID']}"):
                    st.success("Gereserveerd! ✨")
                    st.balloons()
            else:
                st.caption("Log in om een plekje te reserveren.")
    except:
        st.error("Het rooster kon niet geladen worden.")

# --- 5. PAGINA: TARIEVEN ---
elif menu == "🏷️ Tarieven":
    st.title("Tarieven & Pakketten 🌿")
    st.markdown("""
    ### Yoga & Community
    * **Proefles:** €10,-
    * **Losse Credit:** €22,50
    * **The First Connection (3 Credits):** €60,- *(Inclusief 1 maand app cadeau)*
    * **The Growing Tribe (6 Credits):** €115,- *(Inclusief 2 maanden app cadeau)*
    * **The Trimester Journey (12 Credits):** €210,- *(Inclusief 4 maanden app cadeau)*

    ### Persoonlijke Begeleiding
    * **1-op-1 pre- of postnatale yoga:** €80,- *(Bij jou thuis)*

    ### App Only
    * **Los Mama Circle App-lidmaatschap:** €6,- per maand

    ---
    **Betaling & Credits:** Strippenkaarten en betalingen vinden plaats in de studio. 
    Na betaling voegen wij je credits toe aan je account.
    """)

# --- 6. PAGINA: INLOGGEN / ACCOUNT ---
elif menu in ["👤 Inloggen", "👤 Mijn Account"]:
    if not st.session_state.logged_in:
        st.title("Mijn Account")
        email = st.text_input("E-mailadres")
        passw = st.text_input("Wachtwoord", type="password")
        if st.button("Inloggen"):
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
    else:
        st.title("Mijn Account")
        st.write(f"Ingelogd als: **{st.session_state.user_email}**")
        if st.button("Uitloggen"):
            st.session_state.logged_in = False
            st.rerun()

# --- 7. BEVEILIGDE PAGINA'S ---
elif menu == "✨ Mijn Tribe":
    st.title("Mijn Tribe Feed")
    st.info("Updates voor de Circle.")

elif menu == "🌿 Bibliotheek":
    st.title("Mama Reset Bibliotheek")
    st.write("Video's en oefeningen.")

elif menu == "🍲 Village Board":
    st.title("Village Board")
    st.write("De Mealtrain.")
