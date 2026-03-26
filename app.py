import streamlit as st
import pandas as pd

# 1. Configurazione Pagina
st.set_page_config(page_title="FantaAI Pro", layout="wide")

# Inizializzazione Session State (Budget e Rosa)
if 'budget' not in st.session_state:
    st.session_state.budget = 500
if 'squadra' not in st.session_state:
    st.session_state.squadra = []

# --- DATABASE INTEGRATO (Niente più errori 404!) ---
@st.cache_data
def get_giocatori():
    data = [
        # PORTIERI (P)
        {"name": "Sommer", "team": "Inter", "role": "P", "price": 18},
        {"name": "Maignan", "team": "Milan", "role": "P", "price": 17},
        {"name": "Di Gregorio", "team": "Juve", "role": "P", "price": 16},
        {"name": "Meret", "team": "Napoli", "role": "P", "price": 15},
        {"name": "Svilar", "team": "Roma", "role": "P", "price": 14},
        # DIFENSORI (D)
        {"name": "Dimarco", "team": "Inter", "role": "D", "price": 22},
        {"name": "Theo Hernandez", "team": "Milan", "role": "D", "price": 20},
        {"name": "Bremer", "team": "Juve", "role": "D", "price": 18},
        {"name": "Di Lorenzo", "team": "Napoli", "role": "D", "price": 17},
        {"name": "Bastoni", "team": "Inter", "role": "D", "price": 16},
        {"name": "Pavard", "team": "Inter", "role": "D", "price": 15},
        {"name": "Buongiorno", "team": "Napoli", "role": "D", "price": 16},
        # CENTROCAMPISTI (C)
        {"name": "Pulisic", "team": "Milan", "role": "C", "price": 28},
        {"name": "Calhanoglu", "team": "Inter", "role": "C", "price": 26},
        {"name": "Koopmeiners", "team": "Juve", "role": "C", "price": 25},
        {"name": "Barella", "team": "Inter", "role": "C", "price": 22},
        {"name": "Zaccagni", "team": "Lazio", "role": "C", "price": 24},
        {"name": "Mkhitaryan", "team": "Inter", "role": "C", "price": 18},
        {"name": "Douglas Luiz", "team": "Juve", "role": "C", "price": 20},
        {"name": "Pellegrini Lo.", "team": "Roma", "role": "C", "price": 19},
        # ATTACCANTI (A)
        {"name": "Lautaro Martinez", "team": "Inter", "role": "A", "price": 45},
        {"name": "Vlahovic", "team": "Juve", "role": "A", "price": 42},
        {"name": "Lukaku", "team": "Napoli", "price": 40, "role": "A"},
        {"name": "Thuram", "team": "Inter", "role": "A", "price": 38},
        {"name": "Dybala", "team": "Roma", "role": "A", "price": 35},
        {"name": "Kvaratskhelia", "team": "Napoli", "role": "A", "price": 36},
        {"name": "Leao", "team": "Milan", "role": "A", "price": 34},
        {"name": "Retegui", "team": "Atalanta", "role": "A", "price": 32},
        {"name": "Dovbyk", "team": "Roma", "role": "A", "price": 30},
        {"name": "Castellanos", "team": "Lazio", "role": "A", "price": 25},
    ]
    return pd.DataFrame(data)

df = get_giocatori()

# --- SIDEBAR ---
with st.sidebar:
    st.header("💰 Gestione Asta")
    st.metric("Budget Residuo", f"{st.session_state.budget} cr")
    st.write("---")
    menu = st.radio("Scegli Sezione:", ["🎯 Mercato", "📋 La Mia Rosa", "📊 Classifica"])
    
    if st.button("🗑️ Reset Asta"):
        st.session_state.budget = 500
        st.session_state.squadra = []
        st.rerun()

# --- SEZIONE 1: MERCATO ---
if menu == "🎯 Mercato":
    st.title("🎯 Scout & Acquisti Live")
    
    col_a, col_b = st.columns(2)
    with col_a:
        ruolo_filtro = st.multiselect("Filtra Ruolo", ["P", "D", "C", "A"], default=["A", "C"])
    with col_b:
        cerca = st.text_input("Cerca nome giocatore...")

    # Filtro logico
    mostra = df[df['role'].isin(ruolo_filtro)]
    if cerca:
        mostra = mostra[mostra['name'].str.contains(cerca, case=False)]

    for _, row in mostra.iterrows():
        with st.container():
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.subheader(row['name'])
                st.caption(f"{row['team']} | Quotazione: {row['price']} cr")
            with c2:
                prezzo_asta = st.number_input(f"Prezzo pagato", min_value=1, key=f"in_{row['name']}")
            with c3:
                if st.button("PRENDI", key=f"btn_{row['name']}"):
                    st.session_state.squadra.append({"Giocatore": row['name'], "Ruolo": row['role'], "Costo": prezzo_asta})
                    st.session_state.budget -= prezzo_asta
                    st.success(f"Acquistato!")
                    st.rerun()
            st.write("---")

# --- SEZIONE 2: LA MIA ROSA ---
elif menu == "📋 La Mia Rosa":
    st.title("📋 I tuoi colpi di mercato")
    if not st.session_state.squadra:
        st.info("Rosa vuota. Torna al mercato per comprare i tuoi campioni!")
    else:
        rosa_df = pd.DataFrame(st.session_state.squadra)
        st.dataframe(rosa_df, use_container_width=True)
        speso = rosa_df['Costo'].sum()
        st.metric("Totale Speso", f"{speso} cr")

# --- SEZIONE 3: CLASSIFICA ---
else:
    st.title("📊 Classifica Serie A")
    classifica = pd.DataFrame({
        "Squadra": ["Inter", "Napoli", "Juventus", "Milan", "Atalanta", "Lazio", "Roma"],
        "Punti": [76, 68, 65, 62, 60, 58, 55]
    })
    st.table(classifica)
