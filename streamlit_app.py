import streamlit as st
import pandas as pd

st.set_page_config(page_title="Studio Luna", page_icon="🌙")

# De link uit je Secrets halen
url = st.secrets["connections"]["gsheets"]["spreadsheet"]

st.title("Lessenrooster Studio Luna")

try:
    # Direct Pandas gebruiken om de CSV te lezen
    df = pd.read_csv(url)
    
    if df.empty:
        st.write("De lijst is leeg.")
    else:
        for _, row in df.iterrows():
            st.info(f"**Les:** {row['Naam']} | **Datum:** {row['Datum']} | **Tijd:** {row['Tijd']}")

except Exception as e:
    st.error(f"Fout bij het laden: {e}")
    st.write("De link die we gebruiken is:")
    st.code(url)
