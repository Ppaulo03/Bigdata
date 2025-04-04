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

    siglas_estados = {
        'AL': 'Alabama',
        'AK': 'Alasca',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'Califórnia',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Flórida',
        'GA': 'Geórgia',
        'HI': 'Havaí',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'Nova Hampshire',
        'NJ': 'Nova Jersey',
        'NM': 'Novo México',
        'NY': 'Nova York',
        'NC': 'Carolina do Norte',
        'ND': 'Dakota do Norte',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pensilvânia',
        'RI': 'Rhode Island',
        'SC': 'Carolina do Sul',
        'SD': 'Dakota do Sul',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virgínia',
        'WA': 'Washington',
        'WV': 'Virgínia Ocidental',
        'WI': 'Wisconsin',
        'WY': 'Wyoming',
        'DC': 'Distrito de Colúmbia',
        'PR': 'Porto Rico'
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
            else:
                print(f"Coluna {col} não possui valores para calcular a moda.")
                print(df[col].isna().sum())

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

    # Normalizar para minúsculas
    trad_df["original"] = trad_df["original"].str.lower()

    # Remover traduções vazias
    trad_df = trad_df[trad_df["traduzido"].notna() & (trad_df["traduzido"] != "")]

    # Dicionário de substituição
    trad_dict = dict(zip(trad_df["original"], trad_df["traduzido"]))

    # Também normaliza os dados do DataFrame para lowercase antes de substituir
    df["Condição_Tempo"] = df["Condição_Tempo"].str.lower()
    df["Condição_Tempo"] = df["Condição_Tempo"].replace(trad_dict)


    # Substitui as siglas pelos nomes completos
    df["Estado"] = df["Estado"].str.upper()
    df["Estado"] = df["Estado"].replace(siglas_estados)

    # Substituir valores de Impacto
    df["Impacto"] = df["Impacto"].replace({
        1: "Leve",
        2: "Moderado",
        3: "Alto",
        4: "Muito Alto"
    })

    return df.to_dict(orient="records")
