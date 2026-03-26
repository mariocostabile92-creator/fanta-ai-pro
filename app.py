import streamlit as st
import pandas as pd

# 1. Configurazione Pagina
st.set_page_config(page_title="FantaAI Pro", layout="wide")

# Inizializzazione Session State
if 'budget' not in st.session_state:
    st.session_state.budget = 500
if 'squadra' not in st.session_state:
    st.session_state.squadra = []

# --- DATABASE INTEGRATO ---
@st.cache_data
def get_giocatori():
    # Lista pulita e verificata
    data = [
        {"name": "Sommer", "team": "Inter", "role": "P", "price": 18},
        {"name": "Maignan", "team": "Milan", "role": "P", "price": 17},
        {"name": "Di Gregorio", "team": "Juve", "role": "P", "price": 16},
        {"name": "Dimarco", "team": "Inter", "role": "D", "price": 22},
        {"name": "Theo Hernandez", "team": "Milan", "role": "D", "price": 20},
        {"name": "Buongiorno", "team": "Napoli", "role": "D", "price": 16},
        {"name": "Pulisic", "team": "Milan", "role": "C", "price": 28},
        {"name": "Calhanoglu", "team": "Inter", "role": "C", "price": 26},
        {"name": "Koopmeiners", "team": "Juve", "role": "C", "price": 25},
        {"name": "Zaccagni", "team": "Lazio", "role": "C", "price": 24},
        {"name": "Lautaro Martinez", "team": "Inter", "role": "A", "price": 45},
        {"name": "Vlahovic", "team": "Juve", "role": "A", "price": 42},
        {"name": "Lukaku", "team": "Napoli", "role": "A", "price": 40},
        {"name": "Thuram", "team": "Inter", "role": "A", "price": 38},
        {"name": "Dybala", "team": "Roma", "role": "A", "price": 35},
        {"name": "Kvaratskhelia", "team": "Napoli", "role": "A", "price": 36},
        {"name": "Leao", "team": "Milan", "role": "A", "price": 34},
        {"name": "Retegui", "team": "Atalanta", "role": "A", "price": 32}
    ]
    return pd.DataFrame(data)

df = get_giocatori()

# --- SIDEBAR ---
with st.
