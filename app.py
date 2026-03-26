import streamlit as st
import pandas as pd

# 1. Configurazione base
st.set_page_config(page_title="FantaAI Pro", layout="wide")

# 2. Inizializzazione dati
if 'budget' not in st.session_state:
    st.session_state.budget = 500
if 'squadra' not in st.session_state:
    st.session_state.squadra = []

# 3. Database Giocatori
data = [
    {"n": "Sommer", "t": "Inter", "r": "P", "p": 18},
    {"n": "Maignan", "t": "Milan", "r": "P", "p": 17},
    {"n": "Dimarco", "t": "Inter", "r": "D", "p": 22},
    {"n": "Theo", "t": "Milan", "r": "D", "p": 20},
    {"n": "Pulisic", "t": "Milan", "r": "C", "p": 28},
    {"n": "Barella", "t": "Inter", "r": "C", "p": 22},
    {"n": "Lautaro", "t": "Inter", "r": "A", "p": 45},
    {"n": "Vlahovic", "t": "Juve", "r": "A", "p": 42},
    {"n": "Lukaku", "t": "Napoli", "r": "A", "p": 40}
]
df = pd.DataFrame(data)

# 4. Sidebar
st.sidebar.title("💰 Fanta Budget")
st.sidebar.metric("Residuo", f"{st.session_state.budget} cr")
scelta = st.sidebar.radio("Menu", ["Mercato", "Rosa", "Classifica"])

if st.sidebar.button("Reset"):
    st.session_state.budget = 500
    st.session_state.squadra = []
    st.rerun()

# 5. Sezioni
if scelta == "Mercato":
    st.title("🎯 Acquista Giocatori")
    for _, row in df.iterrows():
        col1, col2, col3 = st.columns([2,1,1])
        col1.write(f"**{row['n']}** ({row['t']}) - {row['r']}")
        prezzo = col2.number_input("Prezzo", min_value=1, key=f"p_{row['n']}")
        if col3.button("PRENDI", key=f"b_{row['n']}"):
            st.session_state.squadra.append({"G": row['n'], "P": prezzo})
            st.session_state.budget -= prezzo
            st.rerun()

elif scelta == "Rosa":
    st.title("📋 La tua Rosa")
    if st.session_state.squadra:
        st.table(pd.DataFrame(st.session_state.squadra))
    else:
        st.write("Rosa vuota")

else:
    st.title("📊 Classifica")
    st.write("Inter 76, Juve 62, Milan 59")
