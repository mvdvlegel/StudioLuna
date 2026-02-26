import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import hashlib  # Nieuw: voor de beveiliging

# --- HULPFUNCTIE: WACHTWOORD VERSLEUTELEN ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

# --- (Rest van je config en verbinding blijft hetzelfde) ---

# --- AANPASSING BIJ REGISTREREN (Tab 2) ---
# Vervang de regel waar je de nieuwe gebruiker opslaat:
if st.button("Registreer"):
    # ... (je checks voor email en wachtwoord) ...
    hashed_pw = make_hashes(new_pw)  # Het wachtwoord wordt onleesbaar gemaakt
    new_user = pd.DataFrame([{"E-mail": new_email, "Wachtwoord": hashed_pw}])
    # ... (opslaan in Google Sheets) ...

# --- AANPASSING BIJ INLOGGEN (Tab 1) ---
# Vervang de check bij het inloggen:
if st.button("Log in"):
    users = conn.read(worksheet="Gebruikers")
    # Zoek de gebruiker op e-mail
    user_row = users[users['E-mail'] == email.lower()]
    
    if not user_row.empty:
        stored_password = user_row.iloc[0]['Wachtwoord']
        if check_hashes(pw, stored_password): # Check of het ingetypte PW klopt met de hash
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
    else:
        st.error("Onjuiste e-mail of wachtwoord")
