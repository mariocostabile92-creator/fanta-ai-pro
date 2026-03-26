import streamlit as st
import pandas as pd

# 1. Configurazione Pagina
st.set_page_config(page_title="FantaAI Pro - Ultimate", page_icon="⚽", layout="wide")

# Inizializzazione variabili di stato (per non perdere i dati al refresh)
if 'budget_rimanente' not in st.session_state:
    st.session_state.budget_rimanente = 500
if 'miei_giocatori' not in st.session_state:
    st.session_state.miei_giocatori = []

# CSS Personalizzato
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #6f42c1; color: white; }
    .player-card { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px; border-left: 5px solid #6f42c1; }
    .stat-box { background-color: #f8f9fa; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #dee2e6; }
    </style>
    """, unsafe_allow_html=True)

# 2. Funzione Caricamento Dati (Database Reale + Statistiche)
@st.cache_data
def load_full_data():
    # Carichiamo i dati dei giocatori con statistiche (Gol, Media Voto, ecc.)
    url = "https://raw.githubusercontent.com/OpenFanta/fanta-data/main/data/players.csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.lower() for c in df.columns]
        # Simuliamo alcune statistiche avanzate se mancano nel CSV
        if 'mv' not in df.columns: df['mv'] = 6.0 # Media Voto
        if 'gf' not in df.columns: df['gf'] = 0   # Gol Fatti
        return df
    except:
        return pd.DataFrame([{"name": "Errore", "team": "Dati", "role": "A", "price": 0, "mv": 0, "gf": 0}])

df = load_full_data()

# 3. Sidebar - Gestione Budget & Navigazione
st.sidebar.title("💰 Il Mio Portafoglio")
st.session_state.budget_rimanente = st.sidebar.number_input("Budget Iniziale", value=st.session_state.budget_rimanente)
st.sidebar.metric("Crediti Residui", f"{st.session_state.budget_rimanente} cr")

if st.sidebar.button("Reset Asta"):
    st.session_state.miei_giocatori = []
    st.sidebar.success("Reset effettuato!")

menu = st.sidebar.radio("Navigazione", ["🎯 Ricerca & Asta", "📋 La Mia Rosa", "📊 Classifica Live"])

# --- SEZIONE 1: RICERCA & ASTA (CON IA ADVISOR) ---
if menu == "🎯 Ricerca & Asta":
    st.title("🎯 Scout IA & Assistente Asta")
    
    col_f, col_r = st.columns([1, 2])
    
    with col_f:
        st.subheader("Filtri Scout")
        ruolo = st.multiselect("Ruolo", ["P", "D", "C", "A"], default=["A"])
        search = st.text_input("Cerca nome o squadra...")
    
    with col_r:
        df_display = df[df['role'].isin(ruolo)]
        if search:
            df_display = df_display[df_display['name'].str.contains(search, case=False) | df_display['team'].str.contains(search, case=False)]
        
        for _, row in df_display.head(20).iterrows():
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.markdown(f"### {row['name']}")
                    st.caption(f"{row['team']} - Media Voto: {row['mv']}")
                with c2:
                    prezzo_asta = st.number_input(f"Prezzo per {row['name']}", min_value=1, key=f"p_{row['name']}")
                with c3:
                    if st.button("PRENDI", key=f"btn_{row['name']}"):
                        st.session_state.miei_giocatori.append({"nome": row['name'], "prezzo": prezzo_asta, "ruolo": row['role']})
                        st.session_state.budget_rimanente -= prezzo_asta
                        st.rerun()
                
                # IA Advisor Avanzata
                with st.expander("✨ Perché comprarlo? (Analisi IA)"):
                    if row['gf'] > 5:
                        st.write("🔥 **Bombardiere:** Ha un feeling incredibile con il gol. Vale un investimento alto.")
                    elif row['mv'] > 6.2:
                        st.write("💎 **Regolarista:** Media voto altissima. Perfetto per chi usa il modificatore difesa.")
                    else:
                        st.write("🎲 **Rischio calcolato:** Statistiche modeste, ma potrebbe esplodere come titolare fisso.")

# --- SEZIONE 2: LA MIA ROSA ---
elif menu == "📋 La Mia Rosa":
    st.title("📋 La tua Squadra")
    if not st.session_state.miei_giocatori:
        st.info("Non hai ancora acquistato nessun giocatore.")
    else:
        rosa_df = pd.DataFrame(st.session_state.miei_giocatori)
        st.table(rosa_df)
        st.metric("Totale Speso", f"{sum(rosa_df['prezzo'])} cr")

# --- SEZIONE 3: CLASSIFICA LIVE ---
else:
    st.title("📊 Classifica Serie A (Live)")
    # Qui simuliamo la classifica reale che potresti aggiornare via CSV
    classifica = pd.DataFrame({
        "Squadra": ["Inter", "Juventus", "Milan", "Bologna", "Roma"],
        "Punti": [76, 62, 59, 54, 51],
        "Forma": ["✅✅✅", "❌✅➖", "✅✅➖", "✅✅✅", "✅➖✅"]
    })
    st.dataframe(classifica, use_container_width=True)
    st.info("Nota: I dati della classifica vengono aggiornati ogni lunedì mattina.")
