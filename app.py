import streamlit as st
import pandas as pd

# 1. Configurazione della Pagina
st.set_page_config(page_title="FantaAI Pro", page_icon="⚽", layout="centered")

# Stile CSS per le card dei giocatori
st.markdown("""
    <style>
    .player-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #6f42c1;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        color: #2c3e50;
    }
    .price-badge {
        background-color: #2ecc71;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: bold;
        float: right;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Caricamento Dati
@st.cache_data
def get_data():
    url = "https://raw.githubusercontent.com/OpenFanta/fanta-data/main/data/players.csv"
    try:
        data = pd.read_csv(url)
        return data[['name', 'team', 'role', 'price']]
    except:
        return pd.DataFrame([{"name": "Errore", "team": "Dati", "role": "!", "price": 0}])

df = get_data()

# 3. Sidebar (Filtri)
st.sidebar.title("🎮 FantaAI Panel")
ruolo_filtro = st.sidebar.multiselect("Ruolo", ["P", "D", "C", "A"], default=["A", "C"])
budget_filtro = st.sidebar.slider("Budget Max", 1, 100, 50)
search = st.sidebar.text_input("Cerca nome...")

# 4. Logica di Filtro
df_display = df[df['price'] <= budget_filtro]
if ruolo_filtro:
    df_display = df_display[df_display['role'].isin(ruolo_filtro)]
if search:
    df_display = df_display[df_display['name'].str.contains(search, case=False)]

# 5. Main Page
st.title("⚽ FantaAI: Guru dell'Asta")
st.write(f"Giocatori trovati: {len(df_display)}")

for _, row in df_display.head(20).iterrows():
    with st.container():
        # Creazione Card
        st.markdown(f"""
            <div class="player-card">
                <span class="price-badge">{row['price']} cr</span>
                <div style="font-size: 1.2em; font-weight: bold;">{row['name']}</div>
                <div style="color: #7f8c8d;">{row['team']} - {row['role']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # IA Advisor
        if row['price'] > 30:
            st.info(f"🤖 **Analisi:** {row['name']} è un top di reparto. Compralo se hai almeno il 20% del budget totale.")
        elif row['price'] > 15:
            st.success(f"🤖 **Analisi:** Ottima pedina. Garantisce titolarità e buoni voti.")
        else:
            st.warning(f"🤖 **Analisi:** Scommessa pura. Prendilo a 1 credito come ultimo slot.")
        st.write("---")
