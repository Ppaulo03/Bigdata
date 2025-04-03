import streamlit as st
import pandas as pd
import requests
import matplotlib as plt
import plotly.express as px

st.title("Dashboard - Acidentes de Trânsito nos Estados Unidos (2016 - 2023)")

consulta = st.selectbox("Consulta desejada",['Dias com mais acidentes','Dias com menos acidentes','Acidentes por Estado','Acidentes por Cidade','Acidentes por Condição Climática'])
endpoints = {
    'Dias com mais acidentes': 'top_10_days',
    'Dias com menos acidentes': 'least_10_days',
    'Acidentes por Estado': 'accidents_by_state',
    'Acidentes por Cidade': 'accidents_by_city',
    'Acidentes por Condição Climática': 'accidents_by_weather'
}

def formatar_dia(dia):
    if isinstance(dia, str) and len(dia) == 5 and "-" in dia:
        try:
            mes, dia = dia.split("-")
            return f"{dia}/{mes}"
        except:
            return dia  # fallback
    return dia  # se não for string válida, retorna como está

# Requisição para a API
params = {}
if consulta == "Acidentes por Cidade":
    filtro = st.selectbox("Selecione o estado", ['',
        'CA', 'TX', 'FL', 'NY', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI',
        'NJ', 'VA', 'WA', 'AZ', 'MA', 'MD', 'IN', 'MO', 'TN', 'WI',
        'CO', 'SC', 'AL', 'KY', 'OR', 'OK', 'CT', 'IA', 'KS', 'NV',
        'UT', 'AR', 'MS'
    ])
    params = {"filtro": filtro.title()}

# Requisição para a API com params (mesmo se estiver vazio)
resposta = requests.get(f"http://127.0.0.1:8000/{endpoints[consulta]}", params=params)
print(resposta)

if resposta.status_code == 200:
    dados = resposta.json()
    if dados:
        df = pd.DataFrame(dados)
        print(df.head)

        # Renomeia colunas esperadas
        if '_id' in df.columns:
            df.rename(columns={'_id': 'dado'}, inplace=True)

        # Detecta nome da outra coluna e renomeia para 'valor'
        for col in df.columns:
            if col != 'dado':
                df.rename(columns={col: 'valor'}, inplace=True)

        if consulta in ["Dias com mais acidentes", "Dias com menos acidentes"]:
            # Reformatar mm-dd para dd/mm
            df["dado"] = df["dado"].apply(formatar_dia)

            st.dataframe(df)
            df = df.sort_values("valor", ascending=(consulta == "Dias com menos acidentes"))
            st.bar_chart(df.set_index("dado")["valor"])
        
        elif consulta == "Acidentes por Estado":
            df = df.sort_values("valor", ascending=True)

            fig = px.bar(
                df,
                x="valor",
                y="dado",
                orientation='h',
                labels={"valor": "Total de Acidentes", "dado": "Estado"},
                title="Acidentes por Estado",
                height=900
            )

            fig.update_layout(
                margin=dict(l=100, r=20, t=60, b=40),
                yaxis=dict(
                    tickfont=dict(size=12),
                    tickmode='linear'
                ),
                xaxis=dict(title_font=dict(size=14)),
            )

            st.plotly_chart(fig, use_container_width=True)
        
        elif consulta == "Acidentes por Cidade":
            # Filtra os 10 com maior número de acidentes
            df = df.nlargest(10, "valor")
            df = df.sort_values("valor", ascending=True)  # ordem crescente pra barra horizontal

            fig = px.bar(
                df,
                x="valor",
                y="dado",
                orientation='h',
                labels={"valor": "Total de Acidentes", "dado": "Cidade"},
                title="Top 10 Cidades com Mais Acidentes",
                height=600
            )

            fig.update_layout(
                margin=dict(l=100, r=20, t=60, b=40),
                yaxis=dict(tickfont=dict(size=12)),
                xaxis=dict(title_font=dict(size=14)),
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Colunas 'dado' e 'valor' não encontradas.")
    else:
        st.info("Nenhum dado encontrado.")
else:
    st.error("Erro ao consultar a API.")
