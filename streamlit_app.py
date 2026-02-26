import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Studio Luna - Mama Circle", page_icon="🌙")

st.markdown("""
    <style>
    .stApp { background-color: #F9F7F5; }
    h1, h2 { color: #8FA89B; font-family: 'Serif'; }
    .stButton>button { background-color: #C78D76; color: white; border-radius: 20px; border: none; width: 100%; }
    .lesson-card { background: white; padding: 20px; border-radius: 15px; border-left: 5px solid #8FA89B; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE VERBINDING ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# --- NAVIGATIE ---
st.sidebar.title("Studio Luna 🌙")
if st.session_state.logged_in:
    page = st.sidebar.radio("Menu", ["Lessenrooster", "Bibliotheek", "Uitloggen"])
else:
    page = st.sidebar.radio("Menu", ["Lessenrooster", "Inloggen / Registreren"])

# --- LOGICA: LESSENROOSTER ---
if page == "Lessenrooster":
    st.title("Lessenrooster")
    lessen = conn.read(worksheet="Lessen")
    boekingen = conn.read(worksheet="Boekingen")

    for _, row in lessen.iterrows():
        with st.container():
            st.markdown(f'<div class="lesson-card"><h3>{row["Naam"]}</h3><p>📅 {row["Datum"]} om {row["Tijd"]}</p></div>', unsafe_allow_html=True)
            
            if st.session_state.logged_in:
                bezet = len(boekingen[boekingen['Les_ID'] == str(row['ID'])])
                over = row['Max_Plekken'] - bezet
                st.write(f"✨ **Plekken over: {over}**")
                
                if over > 0:
                    if st.button(f"Boek plek voor {row['Naam']}", key=f"btn_{row['ID']}"):
                        new_booking = pd.DataFrame([{"E-mail": st.session_state.user_email, "Les_ID": str(row['ID']), "Tijdstip": str(datetime.now())}])
                        updated_bookings = pd.concat([boekingen, new_booking], ignore_index=True)
                        conn.update(worksheet="Boekingen", data=updated_bookings)
                        st.success("Gereserveerd! Tot dan!")
                        st.balloons()
                else:
                    st.error("Helaas, deze les is vol.")
            else:
                st.info("Log in om plekken te zien en te boeken.")

# --- LOGICA: INLOGGEN / REGISTREREN ---
elif page == "Inloggen / Registreren":
    t1, t2 = st.tabs(["Inloggen", "Account maken"])
    
    with t1:
        email = st.text_input("E-mail").lower()
        pw = st.text_input("Wachtwoord", type="password")
        if st.button("Log in"):
            users = conn.read(worksheet="Gebruikers")
            user_match = users[(users['E-mail'] == email) & (users['Wachtwoord'] == pw)]
            if not user_match.empty:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Onjuiste gegevens.")

    with t2:
        new_email = st.text_input("Nieuw E-mail").lower()
        new_pw = st.text_input("Kies Wachtwoord", type="password")
        if st.button("Registreer"):
            users = conn.read(worksheet="Gebruikers")
            if new_email in users['E-mail'].values:
                st.warning("E-mail bestaat al.")
            else:
                new_user = pd.DataFrame([{"E-mail": new_email, "Wachtwoord": new_pw}])
                updated_users = pd.concat([users, new_user], ignore_index=True)
                conn.update(worksheet="Gebruikers", data=updated_users)
                st.success("Account gemaakt! Log nu in bij de eerste tab.")

elif page == "Bibliotheek":
    st.title("Bibliotheek")
    st.video("https://www.youtube.com/watch?v=voorbeeld")

elif page == "Uitloggen":
    st.session_state.logged_in = False
    st.rerun()
