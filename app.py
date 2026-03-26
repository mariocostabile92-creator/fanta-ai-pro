import streamlit as st
import pandas as pd

st.set_page_config(page_title="FantaAI Pro", layout="wide")

# Inizializziamo il budget se non esiste
if 'budget' not in st.session_state:
    st.session_state.budget = 500
if 'squadra' not in st.session_state:
    st.session_state.squadra = []

# --- SIDEBAR ---
st.sidebar.title("💰 Gestione Asta")
st.session_state.budget = st.sidebar.number_input("Budget Totale", value=st.session_state.budget)
st.sidebar.metric("Crediti Rimanenti", f"{st.session_state.budget} cr")

menu = st.sidebar.radio("Scegli sezione:", ["Cerca Giocatori", "La Mia Rosa", "Classifica Serie A"])

# --- CARICAMENTO DATI ---
@st.cache_data
def carica_dati():
    url = "https://raw.githubusercontent.com/OpenFanta/fanta-data/main/data/players.csv"
    df = pd.read_csv(url)
    df.columns = [c.lower() for c in df.columns]
    return df

df = carica_dati()

# --- SEZIONE: CERCA GIOCATORI ---
if menu == "Cerca Giocatori":
    st.title("🎯 Trova il tuo Campione")
    cerca = st.text_input("Scrivi il nome di un giocatore (es: Lautaro)")
    
    risultati = df[df['name'].str.contains(cerca, case=False)] if cerca else df.head(10)
    
    for _, row in risultati.iterrows():
        with st.expander(f"⚽ {row['name']} ({row['team']}) - Prezzo: {row['price']} cr"):
            prezzo_acquisto = st.number_input(f"A quanto lo hai preso?", min_value=1, key=f"ins_{row['name']}")
            if st.button(f"Conferma Acquisto {row['name']}", key=f"btn_{row['name']}"):
                st.session_state.squadra.append({"nome": row['name'], "spesa": prezzo_acquisto})
                st.session_state.budget -= prezzo_acquisto
                st.success(f"Preso! {row['name']} aggiunto alla rosa.")
                st.rerun()

# --- SEZIONE: LA MIA ROSA ---
elif menu == "La Mia Rosa":
    st.title("📋 I tuoi acquisti")
    if st.session_state.squadra:
        st.table(pd.DataFrame(st.session_state.squadra))
    else:
        st.write("Ancora nessun acquisto effettuato.")

# --- SEZIONE: CLASSIFICA ---
else:
    st.title("📊 Classifica Serie A")
    st.write("Inter 76, Juve 62, Milan 59... (Dati in aggiornamento)")
