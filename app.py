import streamlit as st
import pandas as pd

st.set_page_config(page_title="FantaAI Pro", layout="wide")

# Inizializziamo il budget e la squadra
if 'budget' not in st.session_state:
    st.session_state.budget = 500
if 'squadra' not in st.session_state:
    st.session_state.squadra = []

# --- CARICAMENTO DATI (CON PROTEZIONE ERRORI) ---
@st.cache_data
def carica_dati():
    url = "https://raw.githubusercontent.com/OpenFanta/fanta-data/main/data/players.csv"
    try:
        # Prova a leggere online
        df = pd.read_csv(url)
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        # Se il link fallisce (HTTPError), usa questi dati di test
        st.warning("Database online non raggiungibile. Caricamento dati di emergenza...")
        data_emergenza = {
            'name': ['Lautaro Martinez', 'Vlahovic', 'Kvaratskhelia', 'Dybala', 'Barella', 'Theo Hernandez', 'Di Lorenzo', 'Sommer'],
            'team': ['Inter', 'Juve', 'Napoli', 'Roma', 'Inter', 'Milan', 'Napoli', 'Inter'],
            'role': ['A', 'A', 'A', 'A', 'C', 'D', 'D', 'P'],
            'price': [40, 35, 32, 30, 22, 18, 15, 15]
        }
        return pd.DataFrame(data_emergenza)

df = carica_dati()

# --- SIDEBAR ---
st.sidebar.title("💰 Gestione Asta")
st.sidebar.metric("Crediti Rimanenti", f"{st.session_state.budget} cr")

menu = st.sidebar.radio("Scegli sezione:", ["Cerca Giocatori", "La Mia Rosa", "Classifica Serie A"])

if st.sidebar.button("Reset Totale"):
    st.session_state.budget = 500
    st.session_state.squadra = []
    st.rerun()

# --- SEZIONE: CERCA GIOCATORI ---
if menu == "Cerca Giocatori":
    st.title("🎯 Scout & Acquisti")
    
    # Filtri veloci
    col_a, col_b = st.columns(2)
    with col_a:
        ruolo_filtro = st.multiselect("Filtra Ruolo", ["P", "D", "C", "A"], default=["A", "C"])
    with col_b:
        cerca = st.text_input("Cerca nome (es: Lautaro)")

    # Applichiamo i filtri
    mask = df['role'].isin(ruolo_filtro)
    if cerca:
        mask = mask & df['name'].str.contains(cerca, case=False)
    
    risultati = df[mask]

    for _, row in risultati.iterrows():
        with st.container():
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.markdown(f"### {row['name']} ({row['team']})")
                st.write(f"Ruolo: **{row['role']}** | Quotazione: {row['price']} cr")
            with c2:
                prezzo_pagato = st.number_input(f"Prezzo asta", min_value=1, key=f"p_{row['name']}")
            with c3:
                if st.button(f"PRENDI", key=f"btn_{row['name']}"):
                    st.session_state.squadra.append({"Giocatore": row['name'], "Squadra": row['team'], "Spesa": prezzo_pagato})
                    st.session_state.budget -= prezzo_pagato
                    st.success(f"Preso {row['name']}!")
                    st.rerun()
            st.write("---")

# --- SEZIONE: LA MIA ROSA ---
elif menu == "La Mia Rosa":
    st.title("📋 I tuoi acquisti")
    if st.session_state.squadra:
        st.table(pd.DataFrame(st.session_state.squadra))
        spesa_totale = sum(item['Spesa'] for item in st.session_state.squadra)
        st.metric("Totale Speso", f"{spesa_totale} cr")
    else:
        st.info("La tua rosa è ancora vuota. Vai in 'Cerca Giocatori' per iniziare l'asta!")

# --- SEZIONE: CLASSIFICA ---
else:
    st.title("📊 Classifica Serie A")
    st.info("Sezione in fase di collegamento con i risultati live.")
