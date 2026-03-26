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
with st.sidebar:
    st.header("💰 ASTA")
    st.metric("Budget Residuo", f"{st.session_state.budget} cr")
    st.write("---")
    menu = st.radio("Scegli Sezione:", ["🎯 Mercato", "📋 La Mia Rosa", "📊 Classifica"])
    
    if st.button("🗑️ Reset Asta"):
        st.session_state.budget = 500
        st.session_state.squadra = []
        st.rerun()

# --- SEZIONE 1: MERCATO ---
if menu == "🎯 Mercato":
    st.title("🎯 Mercato Live")
    
    c1, c2 = st.columns(2)
    with c1:
        ruolo_filtro = st.multiselect("Ruolo", ["P", "D", "C", "A"], default=["A", "C"])
    with c2:
        cerca = st.text_input("Cerca nome...")

    mostra = df[df['role'].isin(ruolo_filtro)]
    if cerca:
        mostra = mostra[mostra['name'].str.contains(cerca, case=False)]

    for _, row in mostra.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.subheader(row['name'])
                st.caption(f"{row['team']} | Quotazione: {row['price']}")
            with col2:
                p_asta = st.number_input(f"Prezzo", min_value=1, key=f"in_{row['name']}")
            with
