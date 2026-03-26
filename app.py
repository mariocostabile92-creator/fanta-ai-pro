import streamlit as st
import pandas as pd

# 1. Configurazione della Pagina
st.set_page_config(page_title="FantaAI Pro", page_icon="⚽", layout="centered")

# Stile CSS per rendere l'app professionale
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .player-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border-left: 6px solid #6f42c1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .price-badge {
        background-color: #2ecc71;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        float: right;
    }
    .player-name { font-size: 1.2em; font-weight: bold; color: #2c3e50; }
    .player-meta { color: #7f8c8d; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# 2. Funzione caricamento dati robusta
@st.cache_data
def load_fanta_data():
    url = "https://raw.githubusercontent.com/OpenFanta/fanta-data/main/data/players.csv"
    try:
        data = pd.read_csv(url)
        # Pulizia nomi colonne (mette tutto in minuscolo per evitare errori)
        data.columns = [c.lower() for c in data.columns]
        return data[['name', 'team', 'role', 'price']]
    except:
        # Dati di emergenza se il link non risponde
        return pd.DataFrame([
            {"name": "Lautaro Martinez", "team": "Inter", "role": "A", "price": 40},
            {"name": "Dusan Vlahovic", "team": "Juve", "role": "A", "price": 35},
            {"name": "Khvicha Kvaratskhelia", "team": "Napoli", "role": "A", "price": 32},
            {"name": "Paulo Dybala", "team": "Roma", "role": "A", "price": 30}
        ])

df = load_fanta_data()

# 3. Sidebar (Controlli)
st.sidebar.title("🎮 FantaAI Control")
st.sidebar.markdown("Usa i filtri per trovare i colpi migliori.")

# Filtri
ruoli_disponibili = sorted(df['role'].unique())
ruolo_sel = st.sidebar.multiselect("Seleziona Ruolo", ruoli_disponibili, default=ruoli_disponibili)
budget_max = st.sidebar.slider("Budget Massimo (cr)", 1, 100, 50)
search_query = st.sidebar.text_input("Cerca calciatore...")

# 4. Logica di filtraggio
df_filtrato = df[df['price'] <= budget_max]
if ruolo_sel:
    df_filtrato = df_filtrato[df_filtrato['role'].isin(ruolo_sel)]
if search_query:
    df_filtrato = df_filtrato[df_filtrato['name'].str.contains(search_query, case=False)]

# 5. Pagina Principale
st.title("⚽ FantaAI: Il Guru dell'Asta")
st.write(f"Visualizzando **{len(df_filtrato)}** calciatori")

if len(df_filtrato) == 0:
    st.warning("Nessun calciatore trovato con questi filtri. Prova ad alzare il budget!")
else:
    for _, row in df_filtrato.head(30).iterrows():
        with st.container():
            # Card HTML
            st.markdown(f"""
                <div class="player-card">
                    <span class="price-badge">{row['price']} cr</span>
                    <div class="player-name">{row['name']}</div>
                    <div class="player-meta">{row['team']} - Ruolo: {row['role']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # IA Advisor logic
            if row['price'] >= 30:
                st.info(f"🤖 **IA ADVISOR:** Top di reparto. Da prendere se vuoi puntare ai primi posti.")
            elif row['price'] >= 15:
                st.success(f"🤖 **IA ADVISOR:** Ottimo titolare. Rapporto qualità/prezzo equilibrato.")
            else:
                st.warning(f"🤖 **IA ADVISOR:** Scommessa low-cost. Ideale per completare la rosa.")
            st.write("") # Spaziatore

# Footer
st.sidebar.markdown("---")
st.sidebar.write("💰 **Versione PRO attiva**")
