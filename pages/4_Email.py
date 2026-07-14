from pathlib import Path
import streamlit as st
from utils import (
    carregar_dados,
    preparar_sidebar,
    saudacao,
    gerar_insights,
    salvar_grafico_churn_reason,
    enviar_email,
    RELATORIO_PATH,
)

st.set_page_config(page_title="E-mail", page_icon="📧", layout="wide")
preparar_sidebar()
saudacao()

st.title("📧 Envio de gráfico ou relatório por e-mail")
st.warning(
    "Para o envio funcionar no deploy, configure as credenciais SMTP nos Secrets do Streamlit ou preencha os campos abaixo. Para Gmail, use uma senha de app."
)

df = carregar_dados()
gerar_insights(df)
grafico_path = salvar_grafico_churn_reason(df)

opcao = st.radio("O que deseja enviar?", ["Gráfico estático", "Relatório escrito"])
destinatario = st.text_input("E-mail do destinatário")

with st.expander("Configurações SMTP"):
    smtp_host = st.text_input("Servidor SMTP", value=st.secrets.get("SMTP_HOST", "smtp.gmail.com") if hasattr(st, "secrets") else "smtp.gmail.com")
    smtp_port = st.number_input("Porta SMTP", value=int(st.secrets.get("SMTP_PORT", 587)) if hasattr(st, "secrets") else 587)
    remetente = st.text_input("E-mail remetente", value=st.secrets.get("SMTP_EMAIL", "") if hasattr(st, "secrets") else "")
    senha = st.text_input("Senha ou senha de app", type="password", value=st.secrets.get("SMTP_PASSWORD", "") if hasattr(st, "secrets") else "")

assunto = "Relatório de Churn"

if opcao == "Gráfico estático":
    corpo = """Olá,

Segue em anexo o gráfico solicitado referente à análise de churn dos clientes.

Atenciosamente,
Equipe de Análise de Dados"""
    anexo = grafico_path
else:
    corpo = """Olá,

Segue em anexo o relatório com os principais insights obtidos na análise dos dados de churn.

Atenciosamente,
Equipe de Análise de Dados"""
    anexo = RELATORIO_PATH

st.subheader("Prévia do corpo do e-mail")
st.text(corpo)

if st.button("Enviar e-mail"):
    if not destinatario or not remetente or not senha:
        st.error("Preencha destinatário, remetente e senha SMTP antes de enviar.")
    else:
        ok, mensagem = enviar_email(
            destinatario=destinatario,
            assunto=assunto,
            corpo=corpo,
            anexo=Path(anexo),
            smtp_host=smtp_host,
            smtp_port=int(smtp_port),
            remetente=remetente,
            senha=senha,
        )
        if ok:
            st.success(mensagem)
        else:
            st.error(mensagem)
