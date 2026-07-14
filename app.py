import streamlit as st
from utils import carregar_dados, preparar_sidebar, calcular_kpis, gerar_insights

st.set_page_config(
    page_title="Análise de Churn - Telecom",
    page_icon="📊",
    layout="wide",
)

nome = preparar_sidebar()
df = carregar_dados()
kpis = calcular_kpis(df)

st.title("📊 Análise de Churn de Clientes")
st.markdown(
    """
Este dashboard foi desenvolvido para apoiar uma empresa de telecomunicações na análise dos cancelamentos de clientes.

O objetivo é identificar **quantos clientes cancelaram**, **quais foram os principais motivos**, quais perfis apresentam maior risco de churn e quais ações podem ajudar a reduzir a perda de clientes.
"""
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de clientes", f"{kpis['total_clientes']:,}")
col2.metric("Clientes cancelados", f"{kpis['churners']:,}")
col3.metric("Taxa de churn", f"{kpis['taxa_churn']:.2%}")
col4.metric("Satisfação média", f"{kpis['satisfacao_media']:.2f}")

st.divider()
st.subheader("Sobre o projeto")
st.write(
    """
A navegação está organizada em múltiplas páginas:

- **Tabela:** visão estática dos dados e tabelas-resumo;
- **Gráficos:** visualizações estáticas e interativas sobre churn;
- **Análise:** relatório executivo com insights e recomendações;
- **E-mail:** envio de gráfico ou relatório para o e-mail informado;
- **Download:** botão para baixar o relatório em arquivo `.txt`.
"""
)

st.info("Digite seu nome na barra lateral para personalizar as páginas do dashboard.")

# Gera o relatório automaticamente para uso nas demais páginas.
gerar_insights(df)
