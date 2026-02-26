import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

# --- 1. CONFIGURATIE & STYLING ---
st.set_page_config(page_title="Studio Luna - Mama Circle", page_icon="🌙")

st.markdown("""
    <style>
    .stApp { background-color: #F9F7F5; }
    h1, h2 { color: #8FA89B; font-family: 'Serif'; }
    .stButton>button { background-color: #C78D76; color: white; border-radius: 20px; border: none; }
    .lesson-card { background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #8FA89B; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BEVEILIGING FUNCTIES ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# --- 3. DATA LADEN (De nieuwe stabiele methode) ---
# Zorg dat deze GID's kloppen met je tabbladen!
BASE_URL = "https://docs.google.com/spreadsheets/d/1q3i75-cDz2Y5cAtHHm8E0Cc6qyMH7Q7o0rcn-1F49Fs/export?format=csv"
LESSEN_URL = f"{BASE_URL}&gid=0"
BOEKINGEN_URL = f"{BASE_URL}&gid=1121386221"
USERS_URL = f"{BASE_URL}&gid=1903698065" # <--- CHECK DEZE GID IN JE BROWSER

@st.cache_data(ttl=10) # Ververst elke 10 seconden
def get_data(url):
    return pd.read_csv(url)

# --- 4. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# --- 5. NAVIGATIE ---
page = st.sidebar.radio("Navigatie", ["Lessenrooster", "Inloggen / Registreren", "Bibliotheek"])

# --- 6. PAGINA: LESSENROOSTER ---
if page == "Lessenrooster":
    st.title("Lessenrooster 🌙")
    try:
        lessen = get_data(LESSEN_URL)
        boekingen = get_data(BOEKINGEN_URL)
        
        # We hebben de verbinding nodig om te schrijven
        conn = st.connection("gsheets", type=GSheetsConnection)

        for _, row in lessen.iterrows():
            with st.container():
                # Weergeven van de leskaart
                st.markdown(f'''
                    <div class="lesson-card">
                        <h3>{row["Naam"]}</h3>
                        <p>📅 {row["Datum"]} | ⏰ {row["Tijd"]}</p>
                    </div>
                ''', unsafe_allow_html=True)
                
                if st.session_state.logged_in:
                    # Bereken beschikbare plekken
                    bezet = len(boekingen[boekingen['Les_ID'].astype(str) == str(row['ID'])])
                    over = int(row['Max_Plekken']) - bezet
                    st.write(f"✨ **Beschikbare plekken: {over}**")
                    
                    if over > 0:
                        # Check of de gebruiker deze les al geboekt heeft
                        al_geboekt = not boekingen[(boekingen['E-mail'] == st.session_state.user_email) & 
                                                  (boekingen['Les_ID'].astype(str) == str(row['ID']))].empty
                        
                        if al_geboekt:
                            st.warning("Je hebt deze les al geboekt. Tot dan! ❤️")
                        else:
                            if st.button(f"Boek plekje voor {row['Naam']}", key=f"btn_{row['ID']}"):
                                # Maak nieuwe boeking aan
                                new_booking = pd.DataFrame([{
                                    "E-mail": st.session_state.user_email,
                                    "Les_ID": str(row['ID']),
                                    "Tijdstip": datetime.now().strftime("%d-%m-%Y %H:%M")
                                }])
                                
                                # Voeg toe aan bestaande lijst en upload
                                updated_boekingen = pd.concat([boekingen, new_booking], ignore_index=True)
                                conn.update(worksheet="Boekingen", data=updated_boekingen)
                                
                                st.success(f"Gelukt! Je bent aangemeld voor {row['Naam']}. Tot snel!")
                                st.balloons()
                                # Cache legen zodat de nieuwe plek direct zichtbaar is
                                st.cache_data.clear() 
                    else:
                        st.error("Helaas, deze les is volgeboekt.")
                else:
                    st.info("Log in om te zien hoeveel plekjes er nog zijn en om te boeken.")
    except Exception as e:
        st.error(f"Fout bij laden rooster: {e}")
        
# --- 7. PAGINA: INLOGGEN / REGISTREREN ---
elif page == "Inloggen / Registreren":
    if not st.session_state.logged_in:
        t1, t2 = st.tabs(["Inloggen", "Account maken"])
        with t1:
            email = st.text_input("E-mail").lower()
            pw = st.text_input("Wachtwoord", type="password")
            if st.button("Log in"):
                users = get_data(USERS_URL)
                user_row = users[users['E-mail'] == email]
                if not user_row.empty and check_hashes(pw, user_row.iloc[0]['Wachtwoord']):
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error("Email of wachtwoord onjuist.")
    else:
        st.write(f"Je bent ingelogd als {st.session_state.user_email}")
        if st.button("Uitloggen"):
            st.session_state.logged_in = False
            st.rerun()
