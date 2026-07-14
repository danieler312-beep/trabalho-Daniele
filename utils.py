from __future__ import annotations

from pathlib import Path
from typing import Tuple
import smtplib
from email.message import EmailMessage

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "telco.csv"
RELATORIO_PATH = BASE_DIR / "relatorio" / "insights.txt"
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)
RELATORIO_PATH.parent.mkdir(exist_ok=True)


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    return df


def preparar_sidebar() -> str:
    st.sidebar.title("Navegação")
    if "nome_usuario" not in st.session_state:
        st.session_state.nome_usuario = ""
    st.session_state.nome_usuario = st.sidebar.text_input(
        "Digite seu nome", value=st.session_state.nome_usuario
    )
    st.sidebar.caption("Projeto de análise de churn em telecomunicações")
    return st.session_state.nome_usuario


def saudacao() -> None:
    nome = st.session_state.get("nome_usuario", "").strip()
    if nome:
        st.markdown(f"### Olá, {nome}! 👋")
    else:
        st.markdown("### Olá! 👋")


def calcular_kpis(df: pd.DataFrame) -> dict:
    total_clientes = len(df)
    churners = int((df["Churn Label"] == "Yes").sum())
    ativos = int((df["Customer Status"] == "Stayed").sum())
    novos = int((df["Customer Status"] == "Joined").sum())
    taxa_churn = churners / total_clientes if total_clientes else 0
    receita_total = float(df["Total Revenue"].sum()) if "Total Revenue" in df.columns else 0.0
    receita_churn = float(df.loc[df["Churn Label"] == "Yes", "Total Revenue"].sum())
    ticket_medio = float(df["Monthly Charge"].mean())
    satisfacao_media = float(df["Satisfaction Score"].mean())
    return {
        "total_clientes": total_clientes,
        "churners": churners,
        "ativos": ativos,
        "novos": novos,
        "taxa_churn": taxa_churn,
        "receita_total": receita_total,
        "receita_churn": receita_churn,
        "ticket_medio": ticket_medio,
        "satisfacao_media": satisfacao_media,
    }


def tabela_churn_por_coluna(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    tabela = (
        df.groupby(coluna, dropna=False)
        .agg(Clientes=("Customer ID", "count"), Cancelamentos=("Churn Value", "sum"))
        .reset_index()
    )
    tabela["Taxa de churn"] = tabela["Cancelamentos"] / tabela["Clientes"]
    tabela = tabela.sort_values("Taxa de churn", ascending=False)
    tabela["Taxa de churn"] = (tabela["Taxa de churn"] * 100).round(2).astype(str) + "%"
    return tabela


def gerar_insights(df: pd.DataFrame) -> str:
    kpis = calcular_kpis(df)
    churn = df[df["Churn Label"] == "Yes"].copy()

    principal_categoria = "Não identificado"
    principal_motivo = "Não identificado"
    if not churn.empty:
        if churn["Churn Category"].notna().any():
            principal_categoria = churn["Churn Category"].value_counts().idxmax()
        if churn["Churn Reason"].notna().any():
            principal_motivo = churn["Churn Reason"].value_counts().idxmax()

    contrato = tabela_churn_por_coluna(df, "Contract").iloc[0]
    pagamento = tabela_churn_por_coluna(df, "Payment Method").iloc[0]
    internet = tabela_churn_por_coluna(df, "Internet Type").iloc[0]

    churn_baixa_satisfacao = df[df["Satisfaction Score"] <= 2]["Churn Value"].mean() * 100
    churn_alta_satisfacao = df[df["Satisfaction Score"] >= 4]["Churn Value"].mean() * 100
    churn_novos = df[df["Tenure in Months"] <= 12]["Churn Value"].mean() * 100
    churn_antigos = df[df["Tenure in Months"] > 36]["Churn Value"].mean() * 100

    texto = f"""RELATÓRIO EXECUTIVO - ANÁLISE DE CHURN

Resumo geral
Foram analisados {kpis['total_clientes']:,} clientes da base de telecomunicações. Desse total, {kpis['churners']:,} clientes cancelaram os serviços, resultando em uma taxa de churn de {kpis['taxa_churn']:.2%}. A receita total registrada na base foi de R$ {kpis['receita_total']:,.2f}, sendo R$ {kpis['receita_churn']:,.2f} associada a clientes que cancelaram.

Principais achados
O principal grupo de motivo de cancelamento foi "{principal_categoria}" e o motivo específico mais recorrente foi "{principal_motivo}". Isso indica que a perda de clientes está fortemente relacionada à percepção de valor, concorrência, preço e experiência do cliente.

A maior taxa de churn por tipo de contrato aparece em "{contrato['Contract']}". Esse comportamento sugere que clientes com contratos mais flexíveis tendem a cancelar com maior facilidade, principalmente quando não percebem vantagem clara em permanecer com a empresa.

A forma de pagamento com maior taxa de churn foi "{pagamento['Payment Method']}". Esse ponto pode indicar maior sensibilidade de determinados perfis de clientes a cobranças, experiência de pagamento ou relacionamento com a empresa.

Entre os tipos de internet, o grupo com maior taxa de churn foi "{internet['Internet Type']}". Esse dado deve ser analisado junto com qualidade percebida do serviço, preço e ofertas da concorrência.

A satisfação do cliente é um dos fatores mais relevantes. Clientes com nota de satisfação até 2 apresentaram taxa média de churn de {churn_baixa_satisfacao:.2f}%, enquanto clientes com satisfação igual ou superior a 4 apresentaram taxa média de churn de {churn_alta_satisfacao:.2f}%.

O tempo de relacionamento também é importante. Clientes com até 12 meses de empresa apresentaram taxa média de churn de {churn_novos:.2f}%, enquanto clientes com mais de 36 meses apresentaram taxa média de churn de {churn_antigos:.2f}%.

Recomendações estratégicas
1. Criar ações de retenção para clientes com contrato mês a mês, oferecendo migração para contratos anuais com benefícios claros.
2. Priorizar clientes com baixo índice de satisfação, alto Churn Score e alto CLTV, pois representam risco relevante de perda de receita.
3. Monitorar os principais motivos de cancelamento ligados à concorrência e preço, ajustando ofertas comerciais para clientes vulneráveis.
4. Criar uma régua de relacionamento para clientes novos, especialmente nos primeiros 12 meses, com acompanhamento de qualidade, suporte e ofertas personalizadas.
5. Melhorar a experiência de suporte técnico e atendimento, principalmente para clientes que já demonstram insatisfação.
6. Desenvolver campanhas específicas para clientes de alto valor, evitando perda de receita futura.

Conclusão
A empresa deve tratar o churn como um problema de retenção, experiência e valor percebido. Os dados mostram que clientes insatisfeitos, recentes, com contratos flexíveis e expostos à concorrência merecem maior atenção. A combinação de ações comerciais, melhoria de atendimento e monitoramento preditivo pode reduzir os cancelamentos e proteger a receita da empresa.
"""
    RELATORIO_PATH.write_text(texto, encoding="utf-8")
    return texto


def salvar_grafico_churn_reason(df: pd.DataFrame) -> Path:
    churn = df[df["Churn Label"] == "Yes"].copy()
    dados = churn["Churn Reason"].value_counts().head(10).sort_values()
    fig, ax = plt.subplots(figsize=(11, 7))
    dados.plot(kind="barh", ax=ax)
    ax.set_title("Top 10 motivos de cancelamento")
    ax.set_xlabel("Quantidade de clientes")
    ax.set_ylabel("Motivo")
    fig.tight_layout()
    caminho = IMAGES_DIR / "grafico_motivos_churn.png"
    fig.savefig(caminho, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return caminho


def enviar_email(
    destinatario: str,
    assunto: str,
    corpo: str,
    anexo: Path,
    smtp_host: str,
    smtp_port: int,
    remetente: str,
    senha: str,
) -> Tuple[bool, str]:
    try:
        msg = EmailMessage()
        msg["From"] = remetente
        msg["To"] = destinatario
        msg["Subject"] = assunto
        msg.set_content(corpo)
        dados = anexo.read_bytes()
        msg.add_attachment(
            dados,
            maintype="application",
            subtype="octet-stream",
            filename=anexo.name,
        )
        with smtplib.SMTP(smtp_host, smtp_port) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.send_message(msg)
        return True, "E-mail enviado com sucesso."
    except Exception as erro:
        return False, f"Não foi possível enviar o e-mail: {erro}"
