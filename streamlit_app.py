import streamlit as st
import pandas as pd
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
        font-weight: 500;
    }}
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

# --- 2. DATA FUNCTIES ---
BASE_URL = "https://docs.google.com/spreadsheets/d/1q3i75-cDz2Y5cAtHHm8E0Cc6qyMH7Q7o0rcn-1F49Fs/export?format=csv"
LESSEN_URL = f"{BASE_URL}&gid=0"

@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)
    
    maanden_vertaling = {
        'januari': 'January', 'februari': 'February', 'maart': 'March',
        'april': 'April', 'mei': 'May', 'juni': 'June',
        'juli': 'July', 'augustus': 'August', 'september': 'September',
        'oktober': 'October', 'november': 'November', 'december': 'December'
    }

    def parse_dutch_date(date_str):
        if not isinstance(date_str, str): return date_str
        d_lower = date_str.lower()
        for nl, en in maanden_vertaling.items():
            if nl in d_lower:
                d_lower = d_lower.replace(nl, en)
        return pd.to_datetime(d_lower, dayfirst=True, errors='coerce')

    df['Datum_DT'] = df['Datum'].apply(parse_dutch_date)
    return df

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# --- 4. NAVIGATIE SIDEBAR ---
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

# --- 5. PAGINA: LESSENROOSTER ---
if menu == "🌙 Lessenrooster":
    st.title("Lessenrooster 🌙")
    try:
        lessen = load_data(LESSEN_URL)
        dagen_nl = {
            'Monday': 'Maandag', 'Tuesday': 'Dinsdag', 'Wednesday': 'Woensdag',
            'Thursday': 'Donderdag', 'Friday': 'Vrijdag', 'Saturday': 'Zaterdag', 'Sunday': 'Zondag'
        }

        for _, row in lessen.iterrows():
            # Dag berekenen
            try:
                engelse_dag = row['Datum_DT'].strftime('%A')
                dag_naam = dagen_nl.get(engelse_dag, engelse_dag)
            except:
                dag_naam = ""
            
            nette_datum = f"{dag_naam} {row['Datum']}"
            
            # Tijd formatteren
            tijd_str = str(row['Tijd']).replace('.', ':')
            if ':' in tijd_str:
                uren, minuten = tijd_str.split(':')
                minuten = minuten.ljust(2, '0')
                tijd_weergave = f"{uren}:{minuten}"
            else:
                tijd_weergave = f"{tijd_str}:00"

            st.markdown(f"""
            <div class='lesson-card'>
                <h3 style='margin-bottom:10px;'>{row['Naam']}</h3>
                <p style='margin:0;'>📅 <b>{nette_datum}</b></p>
                <p style='margin:0;'>⏰ <b>{tijd_weergave} uur</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.logged_in:
                if st.button(f"Reserveer {row['Naam']}", key=f"book_{row['ID']}"):
                    st.success("Gereserveerd! ✨")
                    st.balloons()
            else:
                st.caption("Log in om een plekje te reserveren.")
    except Exception as e:
        st.error(f"Rooster kon niet geladen worden: {e}")

# --- 6. PAGINA: TARIEVEN ---
elif menu == "🏷️ Tarieven":
    st.title("Tarieven & Pakketten 🌿")
    st.markdown("""
    ### Yoga & Community
    * **Proefles:** €10,-
    * **Losse Credit:** €22,50
    * **The First Connection (3 Credits):** €60,- *(Incl. 1 maand app)*
    * **The Growing Tribe (6 Credits):** €115,- *(Incl. 2 maanden app)*
    * **The Trimester Journey (12 Credits):** €210,- *(Incl. 4 maanden app)*

    ### Persoonlijke Begeleiding
    * **1-op-1 pre- of postnatale yoga:** €80,- *(Bij jou thuis)*
    
    *Betalingen vinden plaats in de studio.*
    """)

# --- 7. PAGINA: INLOGGEN ---
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

# --- 8. OVERIGE PAGINA'S ---
elif menu == "✨ Mijn Tribe":
    st.title("Mijn Tribe Feed 🌿")
    st.info("Welkom bij de digitale thee na de les.")

elif menu == "🌿 Bibliotheek":
    st.title("Mama Reset Bibliotheek 🧘")
    st.write("Video's en oefeningen.")

elif menu == "🍲 Village Board":
    st.title("Village Board 🍲")
    st.write("De Mealtrain.")
