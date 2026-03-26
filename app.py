import streamlit as st
import pandas as pd

# 1. Configurazione della Pagina (Titolo e Icona nella scheda del browser)
st.set_page_config(page_title="FantaAI Pro", page_icon="⚽", layout="centered")

# Stile CSS personalizzato per rendere le card più belle
st.markdown("""
    <style>
    .player-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #6f42c1;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .price-badge {
        background-color: #2ecc71;
        color: white;
        padding: 2px 8px;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_stdio=True)

# 2. Caricamento Dati (Dal database pubblico)
@st.cache_data
def get_data():
    url = "https://raw.githubusercontent.com/OpenFanta/fanta-data/main/data/players.csv"
    data = pd.read_csv(url)
    # Rinominiamo le colonne per chiarezza se necessario e puliamo
    return data[['name', 'team', 'role', 'price']]

try:
    df = get_data()
except:
    st.error("Errore nel caricamento dei dati. Riprova più tardi.")
    st.stop()

# 3. Interfaccia Laterale (Filtri)
st.sidebar.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
st.sidebar.title("FantaAI Control")
ruolo_filtro = st.sidebar.multiselect("Filtra per Ruolo", ["P", "D", "C", "A"], default=["A"])
budget_filtro = st.sidebar.slider("Prezzo Massimo (Crediti)", 1, 100, 40)
search = st.sidebar.text_input("Cerca calciatore per nome")

# 4. Logica di filtraggio
df_display = df[df['price'] <= budget_filtro]
if ruolo_filtro:
    df_display = df_display[df_display['role'].isin(ruolo_filtro)]
if search:
    df_display = df_display[df_display['name'].str.contains(search, case=False)]

# 5. Visualizzazione Main Page
st.title("⚽ FantaAI: Guru dell'Asta")
st.write(f"Trovati {len(df_display)} calciatori che corrispondono ai tuoi criteri.")

for _, row in df_display.head(20).iterrows():
    # Creiamo una card per ogni giocatore
    with st.container():
        st.markdown(f"""
            <div class="player-card">
                <span class="price-badge">{row['price']} cr</span>
                <b style="font-size: 1.2em;">{row['name']}</b><br>
                <i style="color: #666;">{row['team']} - {row['role']}</i>
            </div>
        """, unsafe_allow_html=True)
        
        # Consiglio IA dinamico
        if row['price'] > 30:
            st.info(f"🤖 **IA ADVISOR:** {row['name']} è un top. Non pagarlo più del 20% oltre la quotazione.")
        elif row['price'] > 15:
            st.success(f"🤖 **IA ADVISOR:** Ottimo titolare. Garantisce costanza, perfetto per il modificatore.")
        else:
            st.warning(f"🤖 **IA ADVISOR:** Scommessa low-cost. Ideale come ultimo slot per risparmiare.")
        st.write("") # Spazio

# Footer per monetizzazione
st.sidebar.markdown("---")
if st.sidebar.button("🚀 Sblocca Versione PRO"):
    st.balloons()
    st.sidebar.write("Vuoi l'algoritmo avanzato? Contattami in DM!")
