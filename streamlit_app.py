import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import hashlib
from datetime import datetime

# --- 1. CONFIGURATIE & STYLING ---
st.set_page_config(page_title="Studio Luna - Mama Circle", page_icon="🌙")

st.markdown("""
    <style>
    .stApp { background-color: #F9F7F5; }
    h1, h2 { color: #8FA89B; font-family: 'Serif'; }
    .stButton>button { background-color: #C78D76; color: white; border-radius: 20px; border: none; width: 100%; }
    .lesson-card { background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #8FA89B; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .stSidebar { background-color: #F0EDE9 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BEVEILIGING FUNCTIES (HASHING) ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

# --- 3. DATABASE VERBINDING ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 4. SESSION STATE (Inlogstatus) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# --- 5. NAVIGATIE ---
st.sidebar.title("Studio Luna 🌙")
if st.session_state.logged_in:
    page = st.sidebar.radio("Ga naar", ["Lessenrooster", "Bibliotheek", "Uitloggen"])
    st.sidebar.write(f"--- \n Ingelogd als: \n **{st.session_state.user_email}**")
else:
    page = st.sidebar.radio("Ga naar", ["Lessenrooster", "Inloggen / Registreren"])

# --- 6. PAGINA: LESSENROOSTER ---
if page == "Lessenrooster":
    st.title("Lessenrooster")
    
    try:
        lessen = conn.read(worksheet="Lessen")
        boekingen = conn.read(worksheet="Boekingen")

        for _, row in lessen.iterrows():
            with st.container():
                st.markdown(f'''
                    <div class="lesson-card">
                        <h3>{row["Naam"]}</h3>
                        <p>📅 {row["Datum"]} | ⏰ {row["Tijd"]}</p>
                    </div>
                ''', unsafe_allow_html=True)
                
                if st.session_state.logged_in:
                    # Bereken beschikbare plekken
                    aantal_bezet = len(boekingen[boekingen['Les_ID'].astype(str) == str(row['ID'])])
                    plekken_over = int(row['Max_Plekken']) - aantal_bezet
                    
                    st.write(f"✨ **Beschikbare plekken: {plekken_over}**")
                    
                    if plekken_over > 0:
                        if st.button(f"Nu Boeken ({row['Naam']})", key=f"btn_{row['ID']}"):
                            # Opslaan in Google Sheets
                            new_booking = pd.DataFrame([{
                                "E-mail": st.session_state.user_email,
                                "Les_ID": str(row['ID']),
                                "Tijdstip": datetime.now().strftime("%d-%m-%Y %H:%M")
                            }])
                            updated_bookings = pd.concat([boekingen, new_booking], ignore_index=True)
                            conn.update(worksheet="Boekingen", data=updated_bookings)
                            st.success(f"Gereserveerd voor {row['Naam']}! ✨")
                            st.balloons()
                    else:
                        st.error("Deze les is helaas volgeboekt.")
                else:
                    st.info("Log in om beschikbare plekken te zien en te reserveren.")
    except Exception as e:
        st.error("Er is een probleem met het laden van de lessen. Controleer je Google Sheet tabbladen.")

# --- 7. PAGINA: INLOGGEN / REGISTREREN ---
elif page == "Inloggen / Registreren":
    t1, t2 = st.tabs(["Inloggen", "Account aanmaken"])
    
    with t1:
        st.subheader("Welkom terug")
        email = st.text_input("E-mailadres").lower()
        pw = st.text_input("Wachtwoord", type="password")
        if st.button("Inloggen"):
            users = conn.read(worksheet="Gebruikers")
            user_row = users[users['E-mail'] == email]
            
            if not user_row.empty:
                stored_pw = user_row.iloc[0]['Wachtwoord']
                if check_hashes(pw, stored_pw):
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error("Wachtwoord onjuist.")
            else:
                st.error("E-mailadres niet gevonden.")

    with t2:
        st.subheader("Nieuw account")
        new_email = st.text_input("Kies E-mailadres").lower()
        new_pw = st.text_input("Kies Wachtwoord", type="password")
        confirm_pw = st.text_input("Bevestig Wachtwoord", type="password")
        
        if st.button("Registreren"):
            users = conn.read(worksheet="Gebruikers")
            if new_email in users['E-mail'].values:
                st.warning("Dit e-mailadres heeft al een account.")
            elif new_pw != confirm_pw:
                st.error("Wachtwoorden zijn niet gelijk.")
            elif len(new_pw) < 5:
                st.error("Wachtwoord te kort.")
            else:
                hashed_pw = make_hashes(new_pw)
                new_user = pd.DataFrame([{"E-mail": new_email, "Wachtwoord": hashed_pw}])
                updated_users = pd.concat([users, new_user], ignore_index=True)
                conn.update(worksheet="Gebruikers", data=updated_users)
                st.success("Account aangemaakt! Je kunt nu inloggen.")

# --- 8. PAGINA: BIBLIOTHEEK ---
elif page == "Bibliotheek":
    st.title("De Circle Bibliotheek")
    st.write("Hier vind je exclusieve content voor leden.")
    # Vervang deze link door je eigen video-link
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 

# --- 9. UITLOGGEN ---
elif page == "Uitloggen":
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.rerun()
