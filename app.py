import streamlit as st
import pandas as pd

st.set_page_config(page_title="FantaAI Pro - Database Completo", layout="wide")

if 'budget' not in st.session_state:
    st.session_state.budget = 500
if 'squadra' not in st.session_state:
    st.session_state.squadra = []

# --- CARICAMENTO E PULIZIA DATI ---
@st.cache_data
def load_all_players():
    try:
        # Leggiamo il file
        df = pd.read_csv("giocatori.csv", sep=None, engine='python') 
        
        # Forza i nomi delle colonne a minuscolo per evitare KeyError
        df.columns = [c.lower().strip() for c in df.columns]
        
        # Mappatura automatica: se la colonna si chiama 'squadra' rinominala in 'team', ecc.
        mappa = {
            'squadra': 'team', 'club': 'team', 
            'nome': 'name', 'giocatore': 'name',
            'ruolo': 'role', 'r': 'role',
            'quotazione': 'price', 'prezzo': 'price', 'q': 'price'
        }
        df = df.rename(columns=mappa)
        
        # Verifica se mancano colonne vitali e creale vuote se necessario
        for col in ['name', 'team', 'role', 'price']:
            if col not in df.columns:
                df[col] = "N/D"
        
        return df
    except Exception as e:
        # Se il file non esiste o è vuoto, mostra un errore amichevole
        return pd.DataFrame({"name": ["File giocatori.csv non trovato"], "team": ["Aggiorna GitHub"], "role": ["-"], "price": [0]})

df = load_all_players()

# --- SIDEBAR ---
st.sidebar.title("💰 ASTA 2025/26")
st.sidebar.metric("Budget Residuo", f"{st.session_state.budget} cr")
menu = st.sidebar.radio("Naviga:", ["🎯 Mercato", "📋 La Mia Rosa", "📊 Classifica"])

if st.sidebar.button("Reset Totale"):
    st.session_state.budget = 500
    st.session_state.squadra = []
    st.rerun()

# --- SEZIONE MERCATO ---
if menu == "🎯 Mercato":
    st.title("🎯 Database Completo Calciatori")
    
    col1, col2, col3 = st.columns([1,1,2])
    
    with col1:
        # Gestione sicura dei ruoli
        lista_ruoli = sorted(df['role'].unique().tolist())
        r_filtro = st.multiselect("Filtra Ruolo", lista_ruoli, default=lista_ruoli[:1])
    
    with col2:
        # Gestione sicura delle squadre
        lista_squadre = ["Tutte"] + sorted(df['team'].unique().tolist())
        t_filtro = st.selectbox("Filtra Squadra", lista_squadre)
    
    with col3:
        cerca = st.text_input("Cerca nome giocatore...")

    # Applicazione filtri
    mask = df['role'].isin(r_filtro)
    if t_filtro != "Tutte":
        mask = mask & (df['team'] == t_filtro)
    if cerca:
        mask = mask & (df['name'].str.contains(cerca, case=False, na=False))
    
    risultati = df[mask]
    st.caption(f"Giocatori trovati: {len(risultati)}")

    # Visualizzazione a lista compatta
    for _, row in risultati.iterrows():
        with st.container():
            c_a, c_b, c_c = st.columns([2, 1, 1])
            c_a.markdown(f"**{row['name']}** \n*{row['team']} - {row['role']}* (Quotazione: {row['price']})")
            
            p_asta = c_b.number_input(f"Prezzo", min_value=0, key=f"p_{row['name']}")
            
            if c_c.button(f"Acquista", key=f"btn_{row['name']}"):
                st.session_state.squadra.append({
                    "Giocatore": row['name'], 
                    "Ruolo": row['role'], 
                    "Squadra": row['team'], 
                    "Spesa": p_asta
                })
                st.session_state.budget -= p_asta
                st.success(f"{row['name']} preso!")
                st.rerun()
            st.write("---")

# --- SEZIONE ROSA ---
elif menu == "📋 La Mia Rosa":
    st.title("📋 La tua Squadra")
    if st.session_state.squadra:
        df_r = pd.DataFrame(st.session_state.squadra)
        st.dataframe(df_r, use_container_width=True)
        st.metric("Crediti Spesi", f"{df_r['Spesa'].sum()} cr")
    else:
        st.info("Nessun giocatore in rosa.")

# --- SEZIONE CLASSIFICA ---
else:
    st.title("📊 Classifica Serie A")
    st.table(pd.DataFrame({
        "Squadra": ["Inter", "Juventus", "Napoli", "Milan", "Atalanta"],
        "Punti": [42, 38, 37, 34, 33]
    }))
