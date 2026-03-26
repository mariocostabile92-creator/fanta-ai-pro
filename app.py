import streamlit as st
import pandas as pd

# 1. Configurazione Pagina
st.set_page_config(page_title="FantaAI Pro", page_icon="⚽")

# 2. Caricamento Dati (Serie A)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/OpenFanta/fanta-data/main/data/players.csv"
    try:
        data = pd.read_csv(url)
        return data[['name', 'team', 'role', 'price']]
    except:
        return pd.DataFrame([{"name": "Errore Dati", "team": "-", "role": "-", "price": 0}])

df = load_data()

# 3. Interfaccia Utente (UI)
st.title("⚽ FantaAI: Il tuo Guru dell'Asta")
st.markdown("---")

st.sidebar.header("Filtri Ricerca")
ruolo_scelto = st.sidebar.selectbox("Ruolo", ["Tutti", "A", "C", "D", "P"])
budget_max = st.sidebar.slider("Budget Massimo", 1, 100, 50)

# 4. Logica di Filtro
df_filtrato = df[df['price'] <= budget_max]
if ruolo_scelto != "Tutti":
    df_filtrato = df_filtrato[df_filtrato['role'] == ruolo_scelto]

# 5. Visualizzazione Risultati
st.subheader(f"Risultati per {ruolo_scelto}")

for _, row in df_filtrato.head(15).iterrows():
    with st.container():
        c1, c2 = st.columns([3, 1])
        c1.write(f"### {row['name']}")
        c1.write(f"*{row['team']}*")
        c2.metric("Prezzo", f"{row['price']} cr")
        
        # IA ADVISOR (La tua funzione monetizzabile)
        with st.expander("✨ Analisi IA Advisor"):
            if row['price'] > 30:
                st.write("💎 **Top di reparto.** Va comprato se hai budget, garantisce bonus pesanti.")
            elif row['price'] > 15:
                st.write("📈 **Titolare sicuro.** Ottimo per la media voto, prezzo onesto.")
            else:
                st.write("🎲 **Scommessa.** Può esplodere, perfetto come 5° o 6° slot.")
        st.write("---")
