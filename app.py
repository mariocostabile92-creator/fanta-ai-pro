import streamlit as st
import pandas as pd

# 1. Configurazione Pagina
st.set_page_config(page_title="FantaAI Pro", layout="wide")

# Inizializzazione dati in memoria
if 'budget' not in st.session_state:
    st.session_state.budget = 500
if 'squadra' not in st.session_state:
    st.session_state.squadra = []

# --- FUNZIONE CARICAMENTO DATI ---
@st.cache_data
def carica_dati():
    # Usiamo dati locali per ora, così non avremo mai più l'errore 404
    data_fissi = {
        'name': ['Lautaro Martinez', 'Vlahovic', 'Kvaratskhelia', 'Dybala', 'Barella', 'Pulisic', 'Koopmeiners', 'Theo Hernandez', 'Dimarco', 'Sommer', 'Maignan'],
        'team': ['Inter', 'Juve', 'Napoli', 'Roma', 'Inter', 'Milan', 'Atalanta', 'Milan', 'Inter', 'Inter', 'Milan'],
        'role': ['A', 'A', 'A', 'A', 'C', 'C', 'C', 'D', 'D', 'P', 'P'],
        'price': [40, 35, 32, 30, 22, 25, 24, 18, 20, 15, 15]
    }
    return pd.DataFrame(data_fissi)

df = carica_dati()

# --- BARRA LATERALE (SIDEBAR) ---
with st.sidebar:
    st.title("💰 ASTA LIVE")
    st.metric("Budget Residuo", f"{st.session_state.budget} cr")
    st.write("---")
    # Menu di navigazione
    scelta = st.radio("VAI A:", ["🎯 Mercato", "📋 La Mia Rosa", "📊 Classifica"])
    
    if st.button("🗑️ Reset Tutto"):
        st.session_state.budget = 500
        st.session_state.squadra = []
        st.rerun()

# --- SEZIONE 1: MERCATO ---
if scelta == "🎯 Mercato":
    st.title("🎯 Scout & Acquisti")
    
    cerca = st.text_input("Cerca giocatore per nome...")
    ruoli = st.multiselect("Filtra Ruolo", ["P", "D", "C", "A"], default=["A", "C", "D", "P"])
    
    filtro = df[df['role'].isin(ruoli)]
    if cerca:
        filtro = filtro[filtro['name'].str.contains(cerca, case=False)]

    for _, row in filtro.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.subheader(row['name'])
                st.write(f"{row['team']} - {row['role']}")
            with col2:
                prezzo = st.number_input("Prezzo pagato", min_value=1, key=f"p_{row['name']}")
            with col3:
                if st.button("PRENDI", key=f"btn_{row['name']}"):
                    st.session_state.squadra.append({"Giocatore": row['name'], "Ruolo": row['role'], "Costo": prezzo})
                    st.session_state.budget -= prezzo
                    st.success(f"Preso {row['name']}!")
                    st.rerun()
            st.write("---")

# --- SEZIONE 2: LA MIA ROSA ---
elif scelta == "📋 La Mia Rosa":
    st.title("📋 I tuoi acquisti")
    if not st.session_state.squadra:
        st.info("Non hai ancora comprato nessuno. Torna nel Mercato!")
    else:
        df_rosa = pd.DataFrame(st.session_state.squadra)
        st.dataframe(df_rosa, use_container_width=True)
        totale_speso = df_rosa['Costo'].sum()
        st.metric("Totale Speso", f"{totale_speso} cr")

# --- SEZIONE 3: CLASSIFICA ---
elif scelta == "📊 Classifica":
    st.title("📊 Classifica Serie A")
    classifica_finta = pd.DataFrame({
        "Pos": [1, 2, 3, 4, 5],
        "Squadra": ["Inter", "Juve", "Milan", "Napoli", "Atalanta"],
        "Punti": [76, 62, 59, 55, 51]
    })
    st.table(classifica_finta)
