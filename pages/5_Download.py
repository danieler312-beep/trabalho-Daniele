import streamlit as st
from utils import carregar_dados, preparar_sidebar, saudacao, gerar_insights

st.set_page_config(page_title="Download", page_icon="⬇️", layout="wide")
preparar_sidebar()
saudacao()

st.title("⬇️ Download do relatório")
df = carregar_dados()
texto = gerar_insights(df)

st.write("Clique no botão abaixo para baixar o relatório em arquivo `.txt`.")
st.download_button(
    label="Baixar relatório em TXT",
    data=texto,
    file_name="relatorio_churn.txt",
    mime="text/plain",
)
