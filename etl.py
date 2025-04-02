import pandas as pd
import numpy as np


def etl(df_raw):
    colunas_desejadas = {
        "ID": "ID",
        "Severity": "Impacto",
        "Start_Time": "Data_Hora_Inicio",
        "End_Time": "Data_Hora_Fim",
        "Distance(mi)": "Distância(m)",
        "City": "Cidade",
        "State": "Estado",
        "Temperature(F)": "Temperatura(°C)",
        "Visibility(mi)": "Visibilidade(km)",
        "Weather_Condition": "Condição_Tempo",
        "Precipitation(in)": "Precipitação(mm)",
        "Amenity": "Amenidade",
        "Bump": "Quebra_Mola",
        "Crossing": "Cruzamento",
        "Give_Way": "Ceda_Passagem",
        "Junction": "Interseção",
        "No_Exit": "Sem_Saida",
        "Railway": "Ferrovia",
        "Roundabout": "Rotatória",
        "Stop": "Parada",
        "Traffic_Calming": "Redutor_Velocidade",
        "Traffic_Signal": "Semáforo",
        "Turning_Loop": "Retorno",
        "Sunrise_Sunset": "Nascer_Pôr_Sol",
    }

    df = df_raw[list(colunas_desejadas.keys())]
    df = df.rename(columns=colunas_desejadas)

    # Mudar os IDs para int
    def convert_to_int(id_str):
        return int(id_str.split("-")[1]) 

    df["ID"] = df["ID"].apply(convert_to_int)

    # Correção do formato de data e hora
 
    df["Data_Hora_Inicio"] = pd.to_datetime(df["Data_Hora_Inicio"], format='mixed', yearfirst=True)
    df["Data_Hora_Fim"] = pd.to_datetime(df["Data_Hora_Fim"], format='mixed', yearfirst=True)

    df["Duração"] = (df["Data_Hora_Fim"] - df["Data_Hora_Inicio"]).dt.total_seconds() / 3600 


    # Substituir valores ausentes nas colunas categóricas pela moda (valor mais frequente)
    colunas_categoricas = [
        "Cidade", "Estado", "Condição_Tempo", "Amenidade", "Quebra_Mola", "Cruzamento",
        "Ceda_Passagem", "Interseção", "Sem_Saida", "Ferrovia", "Rotatória", "Parada",
        "Redutor_Velocidade", "Semáforo", "Retorno", "Nascer_Pôr_Sol"
    ]

    for col in colunas_categoricas:
        if col in df.columns:
            moda = df[col].mode(dropna=True)
            print(moda)
            if not moda.empty:
                df[col] = df[col].fillna(moda[0])

    # Substituir valores ausentes nas colunas numéricas pela média
    colunas_numericas = [
        "Impacto", "Distancia(m)", "Temperatura(°C)",
        "Visibilidade(m)", "Precipitação(mm)", "Duração"
    ]

    for col in colunas_numericas:
        if col in df.columns:
            media = df[col].mean(skipna=True)
            df[col] = df[col].fillna(media)

    # Converter unidades
    df["Distância(m)"] = df["Distância(m)"] * 1609.34
    df["Temperatura(°C)"] = (df["Temperatura(°C)"] - 32) * 5/9
    df["Visibilidade(km)"] = df["Visibilidade(km)"] * 1.60934
    df["Precipitação(mm)"] = df["Precipitação(mm)"] * 25.4

    # Remover linhas duplicadas
    df = df.drop_duplicates()

    # Forçar tipos de dados
    df["ID"] = df["ID"].astype(int)
    df["Impacto"] = df["Impacto"].astype(int)
    df["Duração"] = df["Duração"].astype(float)
    df["Distância(m)"] = df["Distância(m)"].astype(float)
    df["Temperatura(°C)"] = df["Temperatura(°C)"].astype(float)
    df["Visibilidade(km)"] = df["Visibilidade(km)"].astype(float)
    df["Precipitação(mm)"] = df["Precipitação(mm)"].astype(float)

    # Padronizar capitalização
    colunas_texto = ["Cidade", "Estado", "Condição_Tempo", "Nascer_Pôr_Sol"]
    for col in colunas_texto:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    # Substituir valores de Nascer_Pôr_Sol
    df["Nascer_Pôr_Sol"] = df["Nascer_Pôr_Sol"].replace({
        "Night": "Noite",
        "Day": "Dia"
    })

    # Substituir valores de Condição_Tempo
    trad_df = pd.read_csv("condicoes_traduzidas.csv")
    trad_df = trad_df[trad_df["traduzido"].notna() & (trad_df["traduzido"] != "")]
    trad_dict = dict(zip(trad_df["original"], trad_df["traduzido"]))
    df["Condição_Tempo"] = df["Condição_Tempo"].replace(trad_dict)
    
    condicoes_unicas = df["Condição_Tempo"].unique()
    condicoes_nao_traduzidas = [c for c in condicoes_unicas if c not in trad_dict]
    print("Faltando traduzir:", condicoes_nao_traduzidas)

    # Substituir valores de Impacto
    df["Impacto"] = df["Impacto"].replace({
        1: "Leve",
        2: "Moderado",
        3: "Alto",
        4: "Muito Alto"
    })

    return df.to_dict(orient="records")