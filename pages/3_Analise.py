import streamlit as st
from utils import carregar_dados, preparar_sidebar, saudacao, gerar_insights

st.set_page_config(page_title="Análise", page_icon="🧠", layout="wide")
preparar_sidebar()
saudacao()

st.title("🧠 Relatório Executivo e Insights")
df = carregar_dados()
texto = gerar_insights(df)
st.text_area("Relatório gerado", texto, height=700)
