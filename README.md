# Análise de Churn de Clientes - Streamlit

Projeto desenvolvido em Streamlit para análise de churn de clientes de uma empresa de telecomunicações.

## Funcionalidades

- Dashboard com múltiplas páginas;
- Sidebar com nome do usuário salvo em sessão;
- Página de tabela estática;
- Página de gráficos estáticos e interativos;
- Página com relatório executivo e insights;
- Página para envio de gráfico ou relatório por e-mail;
- Página para download do relatório em `.txt`.

## Como executar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy no Streamlit Cloud

1. Crie um repositório público no GitHub.
2. Envie todos os arquivos deste projeto para o repositório.
3. Acesse https://streamlit.io/cloud.
4. Clique em **New app**.
5. Selecione o repositório.
6. Em **Main file path**, coloque `app.py`.
7. Clique em **Deploy**.

O nome solicitado para o site deve seguir o padrão:

```text
nome-sobrenome.streamlit.app
```

## Configuração de e-mail

Para usar Gmail, crie uma senha de app e configure os Secrets do Streamlit:

```toml
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "seu-email@gmail.com"
SMTP_PASSWORD = "sua-senha-de-app"
```
