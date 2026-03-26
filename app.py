import streamlit as st
import pandas as pd

# 1. Configurazione della Pagina
st.set_page_config(page_title="FantaAI Pro", page_icon="⚽", layout="centered")

# Stile CSS corretto
st.markdown("""
    <style>
    .player-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #6f42c1;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .price-badge {
        background-color: #2ecc71;
        color: white;
        padding: 2px 8px;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True) # <--- CORRETTO QUI

# 2. Caricamento Dati
@st.cache_data
def get_data():
    url = "https://raw.githubusercontent.com/OpenFanta/fanta-data/main/data/players.csv"
    data = pd.read_csv(url)
    return data[['name', 'team', 'role', 'price']]

try:
    df = get_data()
except:
    st.error("Errore caricamento dati.")
    st.stop()

# 3. Sidebar
st.sidebar.title("FantaAI Control")
ruolo_filtro = st.sidebar.multiselect("Filtra Ruolo", ["P", "D", "C", "A"], default=["A"])
budget_filtro = st.sidebar.slider("Prezzo Massimo", 1, 100, 40)
search = st.sidebar.text_input("Cerca nome")

# 4. Filtro
df_display = df[df['price'] <= budget_filtro]
if ruolo_filtro:
    df_display = df_display[df_display['role'].isin(ruolo_filtro)]
if search:
    df_display = df_display[df_display['name'].str.contains(search, case=False)]

# 5. Visualizzazione
st.title("⚽ FantaAI: Guru dell'Asta")

for _, row in df_display.head(20).iterrows():
    with st.container():
        st.markdown(f"""
            <div class="player-card">
                <span class="price-badge">{row['price']} cr</span>
                <b style="font-size: 1.1em; color: black;">{row['name']}</b><br>
                <span style="color: #666;">{row['team']} - {row['role']}</span>
            </div>
        """, unsafe_allow_html=True) # <--- CORRETTO ANCHE QUI
        
        if row['price'] > 30:
            st.info(f"🤖 **IA:** Top player assoluto.")
        else:
            st.success(f"🤖 **IA:** Ottimo per il budget.")
