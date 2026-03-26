import streamlit as st
import pandas as pd

st.set_page_config(page_title="FantaAI Pro COMPLETO", layout="wide")

if 'budget' not in st.session_state:
    st.session_state.budget = 500
if 'squadra' not in st.session_state:
    st.session_state.squadra = []

# --- CARICAMENTO DATABASE COMPLETO ---
@st.cache_data
def load_all_players():
    try:
        # Legge il file csv che hai caricato nella stessa cartella
        df = pd.read_csv("giocatori.csv")
        # Standardizziamo i nomi delle colonne per il codice
        df.columns = [c.lower() for c in df.columns]
        return df
    except:
        # Se il file non c'è, carica i top per non lasciare l'app vuota
        return pd.DataFrame([
            {"name": "ERRORE: Carica giocatori.csv su GitHub", "team": "-", "role": "A", "price": 0}
        ])

df = load_all_players()

# --- SIDEBAR ---
st.sidebar.title("💰 ASTA 2025/26")
st.sidebar.metric("Budget", f"{st.session_state.budget} cr")
menu = st.sidebar.radio("Naviga:", ["🎯 Mercato Completo", "📋 La Mia Rosa", "📊 Classifica"])

if st.sidebar.button("Reset"):
    st.session_state.budget = 500
    st.session_state.squadra = []
    st.rerun()

# --- SEZIONE MERCATO ---
if menu == "🎯 Mercato Completo":
    st.title("🎯 Database Tutti i Giocatori")
    
    c1, c2, c3 = st.columns([1,1,2])
    with c1:
        r_filtro = st.multiselect("Ruolo", ["P", "D", "C", "A"], default=["A"])
    with c2:
        t_filtro = st.selectbox("Squadra", ["Tutte"] + sorted(df['team'].unique().tolist()))
    with c3:
        cerca = st.text_input("Cerca nome...")

    # Filtri incrociati
    mask = df['role'].isin(r_filtro)
    if t_filtro != "Tutte":
        mask = mask & (df['team'] == t_filtro)
    if cerca:
        mask = mask & (df['name'].str.contains(cerca, case=False))
    
    risultati = df[mask]
    st.write(f"Trovati {len(risultati)} giocatori")

    for _, row in risultati.iterrows():
        with st.expander(f"{row['role']} - {row['name']} ({row['team']}) - Q: {row['price']}"):
            col1, col2 = st.columns(2)
            prezzo_a = col1.number_input(f"Prezzo asta", min_value=1, key=f"p_{row['name']}")
            if col2.button(f"COMPRA {row['name']}", key=f"b_{row['name']}"):
                st.session_state.squadra.append({"G": row['name'], "R": row['role'], "S": row['team'], "P": prezzo_a})
                st.session_state.budget -= prezzo_a
                st.rerun()

# --- SEZIONE ROSA ---
elif menu == "📋 La Mia Rosa":
    st.title("📋 La tua Squadra")
    if st.session_state.squadra:
        df_r = pd.DataFrame(st.session_state.squadra)
        st.dataframe(df_r, use_container_width=True)
        st.metric("Spesa Totale", f"{df_r['P'].sum()} cr")
    else:
        st.write("Nessun acquisto.")

# --- SEZIONE CLASSIFICA ---
else:
    st.title("📊 Classifica Live")
    st.info("Dati aggiornati al 2026")
    st.table(pd.DataFrame({"Squadra": ["Inter", "Juve", "Napoli"], "Punti": [60, 58, 55]}))
