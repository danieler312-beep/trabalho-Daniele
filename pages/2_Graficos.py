import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from utils import carregar_dados, preparar_sidebar, saudacao

st.set_page_config(page_title="Gráficos", page_icon="📈", layout="wide")
preparar_sidebar()
saudacao()

st.title("📈 Gráficos de Churn")
df = carregar_dados()
churn = df[df["Churn Label"] == "Yes"].copy()

st.subheader("Clientes que cancelaram x clientes que permaneceram")
status = df["Churn Label"].value_counts().reset_index()
status.columns = ["Churn", "Quantidade"]
fig1 = px.bar(status, x="Churn", y="Quantidade", text="Quantidade", title="Distribuição de churn")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Principais motivos de cancelamento")
motivos = churn["Churn Reason"].value_counts().head(10).sort_values()
fig, ax = plt.subplots(figsize=(11, 6))
motivos.plot(kind="barh", ax=ax)
ax.set_title("Top 10 motivos de cancelamento")
ax.set_xlabel("Quantidade")
ax.set_ylabel("Motivo")
st.pyplot(fig)

st.subheader("Categoria do cancelamento")
cat = churn["Churn Category"].value_counts().reset_index()
cat.columns = ["Categoria", "Quantidade"]
fig2 = px.pie(cat, names="Categoria", values="Quantidade", title="Churn por categoria")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Churn por tipo de contrato")
contrato = df.groupby(["Contract", "Churn Label"]).size().reset_index(name="Quantidade")
fig3 = px.bar(contrato, x="Contract", y="Quantidade", color="Churn Label", barmode="group")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Churn por forma de pagamento")
pagamento = df.groupby(["Payment Method", "Churn Label"]).size().reset_index(name="Quantidade")
fig4 = px.bar(pagamento, x="Payment Method", y="Quantidade", color="Churn Label", barmode="group")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Satisfação x churn")
sat = df.groupby(["Satisfaction Score", "Churn Label"]).size().reset_index(name="Quantidade")
fig5 = px.bar(sat, x="Satisfaction Score", y="Quantidade", color="Churn Label", barmode="group")
st.plotly_chart(fig5, use_container_width=True)

st.subheader("Tempo de empresa x churn")
fig6 = px.histogram(df, x="Tenure in Months", color="Churn Label", nbins=30, barmode="overlay")
st.plotly_chart(fig6, use_container_width=True)

st.subheader("Monthly Charge x churn")
fig7 = px.box(df, x="Churn Label", y="Monthly Charge", points="outliers")
st.plotly_chart(fig7, use_container_width=True)

st.subheader("Churn Score x CLTV")
fig8 = px.scatter(
    df,
    x="Churn Score",
    y="CLTV",
    color="Churn Label",
    hover_data=["Customer ID", "Contract", "Satisfaction Score"],
    title="Risco de churn e valor do cliente",
)
st.plotly_chart(fig8, use_container_width=True)
