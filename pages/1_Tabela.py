import streamlit as st
from utils import carregar_dados, preparar_sidebar, saudacao, calcular_kpis, tabela_churn_por_coluna

st.set_page_config(page_title="Tabela", page_icon="📋", layout="wide")
preparar_sidebar()
saudacao()

st.title("📋 Tabelas da Base de Clientes")
df = carregar_dados()
kpis = calcular_kpis(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Clientes", f"{kpis['total_clientes']:,}")
col2.metric("Cancelamentos", f"{kpis['churners']:,}")
col3.metric("Taxa de churn", f"{kpis['taxa_churn']:.2%}")
col4.metric("Novos clientes", f"{kpis['novos']:,}")

st.subheader("Amostra estática da base")
st.caption("A tabela abaixo está em modo estático. Para evitar lentidão, são exibidas as primeiras 100 linhas.")
st.table(df.head(100))

st.subheader("Resumo por tipo de contrato")
st.table(tabela_churn_por_coluna(df, "Contract"))

st.subheader("Resumo por forma de pagamento")
st.table(tabela_churn_por_coluna(df, "Payment Method"))

st.subheader("Resumo por tipo de internet")
st.table(tabela_churn_por_coluna(df, "Internet Type"))
