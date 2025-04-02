import pandas as pd
import numpy as np

'''
  "Fair",
  "Mostly Cloudy",
  "Cloudy",
  "Clear",
  "Partly Cloudy",
  "Overcast",
  "Light Rain",
  "Scattered Clouds",
  "nan",
  "Light Snow",
  "Fog",
  "Rain",
  "Haze",
  "Fair / Windy",
  "Heavy Rain",
  "Light Drizzle",
  "Thunder in the Vicinity",
  "Cloudy / Windy",
  "T-Storm",
  "Mostly Cloudy / Windy",
  "Snow",
  "Thunder",
  "Light Rain with Thunder",
  "Smoke",
  "Wintry Mix",
  "Partly Cloudy / Windy",
  "Heavy T-Storm",
  "Light Rain / Windy",
  "Light Snow / Windy",
  "Heavy Snow",
  "Light Thunderstorms and Rain",
  "Drizzle",
  "Thunderstorm",
  "Patches of Fog",
  "Mist",
  "Light Freezing Rain",
  "N/A Precipitation",
  "Shallow Fog",
  "Heavy Thunderstorms and Rain",
  "Rain / Windy",
  "Thunderstorms and Rain",
  "Haze / Windy",
  "Heavy Rain / Windy",
  "Showers in the Vicinity",
  "Snow / Windy",
  "Light Freezing Drizzle",
  "Heavy T-Storm / Windy",
  "Light Freezing Fog",
  "Blowing Snow / Windy",
  "Heavy Snow / Windy",
  "T-Storm / Windy",
  "Fog / Windy",
  "Blowing Snow",
  "Thunder / Windy",
  "Heavy Drizzle",
  "Drizzle and Fog",
  "Snow and Sleet",
  "Wintry Mix / Windy",
  "Blowing Dust / Windy",
  "Light Ice Pellets",
  "Light Rain Shower",
  "Light Sleet",
  "Light Drizzle / Windy",
  "Light Snow and Sleet",
  "Freezing Rain",
  "Blowing Dust",
  "Widespread Dust",
  "Light Rain Showers",
  "Sleet",
  "Rain Showers",
  "Ice Pellets",
  "Snow and Sleet / Windy",
  "Smoke / Windy",
  "Light Freezing Rain / Windy",
  "Small Hail",
  "Rain Shower",
  "Sand / Dust Whirlwinds",
  "Squalls / Windy",
  "Light Snow and Sleet / Windy",
  "Light Snow Shower",
  "Partial Fog",
  "Hail",
  "Light Snow with Thunder",
  "Squalls",
  "Heavy Sleet",
  "Freezing Drizzle",
  "Thunder / Wintry Mix",
  "Sleet / Windy",
  "Light Snow Showers",
  "Widespread Dust / Windy",
  "Drizzle / Windy",
  "Light Thunderstorms and Snow",
  "Funnel Cloud",
  "Volcanic Ash",
  "Snow and Thunder",
  "Tornado",
  "Sand",
  "Freezing Rain / Windy",
  "Light Rain Shower / Windy",
  "Mist / Windy",
  "Light Sleet / Windy",
  "Thunder and Hail",
  "Heavy Freezing Rain",
  "Thunder / Wintry Mix / Windy",
  "Light Haze",
  "Snow Grains",
  "Heavy Snow with Thunder",
  "Heavy Rain Showers",
  "Patches of Fog / Windy",
  "Heavy Thunderstorms with Small Hail",
  "Shallow Fog / Windy",
  "Drifting Snow / Windy",
  "Sand / Dust Whirls Nearby",
  "Light Snow Grains",
  "Heavy Freezing Drizzle",
  "Light Snow Shower / Windy",
  "Heavy Thunderstorms and Snow",
  "Low Drifting Snow",
  "Heavy Blowing Snow",
  "Light Fog",
  "Heavy Ice Pellets",
  "Sleet and Thunder",
  "Sand / Dust Whirlwinds / Windy",
  "Duststorm",
  "Light Hail",
  "Thunderstorms and Snow",
  "Light Thunderstorm",
  "Heavy Rain Shower",
  "Light Blowing Snow",
  "Rain Shower / Windy",
  "Blowing Sand",
  "Heavy Sleet and Thunder",
  "Thunder and Hail / Windy",
  "Rain and Sleet",
  "Snow Showers",
  "Snow and Thunder / Windy",
  "Partial Fog / Windy",
  "Heavy Rain Shower / Windy",
  "Blowing Snow Nearby",
  "Heavy Freezing Rain / Windy",
  "Sand / Windy",
  "Heavy Sleet / Windy",
  "Heavy Smoke",
  "Dust Whirls",
  "Drifting Snow"
'''


def etl(df_raw):
    colunas_desejadas = {
        "ID": "ID",
        "Severity": "Gravidade",
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
            if not moda.empty:
                df[col] = df[col].fillna(moda[0])

    # Substituir valores ausentes nas colunas numéricas pela média
    colunas_numericas = [
        "Gravidade", "Distancia(m)", "Temperatura(°C)",
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
    df["Gravidade"] = df["Gravidade"].astype(int)
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
    df["Condição_Tempo"] = df["Condição_Tempo"].replace({
        "Light Rain": "Chuva Leve",
        "Overcast": "Nublado",
        "Mostly Cloudy": "Predominantemente Nublado",
        "Rain": "Chuva",
        "Light Snow": "Neve Leve",
        "Haze": "Névoa",
        "Scattered Clouds": "Nuvens Dispersas",
        "Partly Cloudy": "Parcialmente Nublado",
        "Clear": "Céu Limpo",
        "Snow": "Neve",
        "Light Freezing Drizzle": "Garoa Congelante Leve",
        "Light Drizzle": "Garoa Leve",
        "Fog": "Nevoeiro",
        "Fair": "Ameno"
    })

    # Substituir valores de Gravidade
    df["Gravidade"] = df["Gravidade"].replace({
        1: "Leve",
        2: "Moderada",
        3: "Grave"
    })

    return df.to_dict(orient="records")
