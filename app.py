import streamlit as st

st.title("🚀 FantaAI è quasi pronta!")
st.write("Se vedi questo messaggio, il server funziona correttamente.")

if st.button("Cliccami per un consiglio"):
    st.balloons()
    st.success("Il consiglio dell'IA: Compra Lautaro!")
