import streamlit as st
import pandas as pd
import requests
import matplotlib as plt

st.title("Dashboard - Acidentes de Trânsito nos Estados Unidos (2016 - 2023)")

consulta = st.selectbox("Consulta desejada",['Dias com mais acidentes','Dias com menos acidentes','Acidentes por Estado','Acidentes por Cidade','Acidentes por Condição Climática'])
filtro = st.selectbox("")

# Requisição para a API
params = {"filtro": filtro} if filtro else {}
resposta = requests.get(f"http://localhost:8000/{consulta}", params=params)

if resposta.status_code == 200:
    dados = resposta.json()
    if dados:
        df = pd.DataFrame(dados)

        # Mostra os dados em tabela
        st.dataframe(df)

        # Exemplo de gráfico (ajuste para seu caso)
        if "data" in df.columns and "valor" in df.columns:
            df["data"] = pd.to_datetime(df["data"])
            df = df.sort_values("data")

            st.line_chart(df.set_index("data")["valor"])
        else:
            st.warning("Colunas 'data' e 'valor' não encontradas.")
    else:
        st.info("Nenhum dado encontrado.")
else:
    st.error("Erro ao consultar a API.")