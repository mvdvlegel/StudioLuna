# --- 2. DATA & SESSION STATE ---
BASE_URL = "https://docs.google.com/spreadsheets/d/1q3i75-cDz2Y5cAtHHm8E0Cc6qyMH7Q7o0rcn-1F49Fs/export?format=csv"
LESSEN_URL = f"{BASE_URL}&gid=0"

@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)
    
    # Vertaler voor Nederlandse maanden
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
        # Nu Python de Engelse maand heeft, kan hij het lezen
        return pd.to_datetime(d_lower)

    # Pas de vertaling toe op de Datum kolom
    df['Datum_DT'] = df['Datum'].apply(parse_dutch_date)
    return df
