import streamlit as st
import pandas as pd

# 1. Configurazione della Pagina
st.set_page_config(page_title="FantaAI Pro", page_icon="⚽", layout="wide")

# Stile CSS per Card e Classifica
st.markdown("""
    <style>
    .player-card {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 10px;
        border-left: 5px solid #6f42c1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 10px;
        color: #333;
    }
    .price-badge {
        background-color: #2ecc71;
        color: white;
        padding: 2px 10px;
        border-radius: 15px;
        font-weight: bold;
        float: right;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Caricamento Dati (Cache per velocità)
@st.cache_data
def load_data():
    # Giocatori
    url_players = "https://raw.githubusercontent.com/OpenFanta/fanta-data/main/data/players.csv"
    try:
        df = pd.read_csv(url_players)
        df.columns = [c.lower() for c in df.columns]
    except:
        df = pd.DataFrame([{"name": "Esempio", "team": "Team", "role": "A", "price": 10}])
    
    # Dati Serie A (Simulati/Placeholder - In una versione reale useresti un'API o CSV aggiornati)
    standings = pd.DataFrame({
        "Squadra": ["Inter", "Juventus", "Milan", "Napoli", "Atalanta", "Lazio", "Roma", "Fiorentina"],
        "Punti": [75, 62, 59, 55, 50, 49, 48, 45],
        "G": [29, 29, 29, 29, 28, 29, 29, 29]
    }).sort_values(by="Punti", ascending=False)
    
    return df, standings

df_players, df_standings = load_data()

# 3. Sidebar
st.sidebar.title("⚽ FantaAI Menu")
menu = st.sidebar.radio("Vai a:", ["🎯 Guru dell'Asta", "📊 Classifica & Calendario"])

# --- SEZIONE 1: GURU DELL'ASTA ---
if menu == "🎯 Guru dell'Asta":
    st.title("🎯 Consigliere IA per l'Asta")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Filtri")
        ruoli = st.multiselect("Ruolo", ["P", "D", "C", "A"], default=["A", "C"])
        budget = st.slider("Budget Max (cr)", 1, 100, 100)
        cerca = st.text_input("Cerca nome...")

    with col2:
        # Filtro
        final_df = df_players[df_players['price'] <= budget]
        if ruoli:
            final_df = final_df[final_df['role'].isin(ruoli)]
        if cerca:
            final_df = final_df[final_df['name'].str.contains(cerca, case=False)]
        
        st.write(f"Trovati {len(final_df)} calciatori")
        
        # Lista Giocatori (Senza limite .head() per vederli tutti)
        for _, row in final_df.iterrows():
            with st.container():
                st.markdown(f"""
                    <div class="player-card">
                        <span class="price-badge">{row['price']} cr</span>
                        <b>{row['name']}</b> ({row['team']}) - {row['role']}
                    </div>
                """, unsafe_allow_html=True)

# --- SEZIONE 2: CLASSIFICA E CALENDARIO ---
else:
    st.title("📊 Situazione Serie A")
    
    tab1, tab2 = st.tabs(["🏆 Classifica", "📅 Calendario & Risultati"])
    
    with tab1:
        st.table(df_standings)
    
    with tab2:
        st.subheader("Prossima Giornata (Esempio)")
        st.info("Qui puoi inserire i risultati dell'ultimo turno o il calendario aggiornato.")
        col_a, col_b = st.columns(2)
        col_a.write("🏠 **Inter vs Empoli**")
        col_b.write("Lunedì 20:45")
        st.write("---")
        col_a.write("🏠 **Lazio vs Juventus**")
        col_b.write("Sabato 18:00")
