import pandas as pd

def unionDataFrames(df, df2):
    """
    Unión de dos dataframes.

    Arguments:
    * df: Pandas Dataframe 1
    * df2: Pandas Dataframe 2

    Return:
    * df: Pandas Dataframe unido
    """
    # Merge entre los dataframes de entrada
    df = df.merge(df2, on="modelo", how="outer")
    # Eliminación columnas duplicadas
    df = df.drop("marca_y", axis=1)
    df = df.drop("peso_x", axis=1)
    df = df.drop("pulgadas_y", axis=1)
    df = df.drop("calidad_imagen_y", axis=1)
    df = df.drop("sistema_operativo", axis=1)
    # Renombrar columnas
    df = df.rename(columns = {'marca_x': 'marca', 'peso_y': 'peso', 'pulgadas_x': 'pulgadas', 'calidad_imagen_x': 'calidad_imagen'}, inplace = False)
    
    return df


################ UNION TABLETS ################

# Para hacer la unión de los dos CSV, se lee del directorio el CSV de Mediamarkt el de DominioVirtual 
df_mediamarkt = pd.read_csv("./csv/mediamark/tabletsMediamarkt.csv")
df_dominiovirtual = pd.read_csv("./csv/dominioVirtual/tabletsDominioVirtual.csv")
df = unionDataFrames(df_mediamarkt, df_dominiovirtual).fillna("NA")
df.to_csv("./csv/union_tablets.csv", index=False, encoding='utf-8')

################ UNION PORTATILES ################

# Para hacer la unión de los dos CSV, se lee del directorio el CSV de Mediamarkt y se aprovecha el DF de DominioVirtual ya cargado 
df_mediamarkt = pd.read_csv("./csv/mediamark/portatilesMediamarkt.csv")
df_dominiovirtual = pd.read_csv("./csv/dominioVirtual/portatilesDominioVirtual.csv")
df = unionDataFrames(df_mediamarkt, df_dominiovirtual).fillna("NA")
df.to_csv("./csv/union_portatiles.csv", index=False, encoding='utf-8')

################ UNION MONITORES ################

# Para hacer la unión de los dos CSV, se lee del directorio el CSV de Mediamarkt y se aprovecha el DF de DominioVirtual ya cargado 
df_mediamarkt = pd.read_csv("./csv/mediamark/monitoresMediamarkt.csv")
df_dominiovirtual = pd.read_csv("./csv/dominioVirtual/monitoresDominioVirtual.csv")
df = unionDataFrames(df_mediamarkt, df_dominiovirtual).fillna("NA")
df.to_csv("./csv/union_monitores.csv", index=False, encoding='utf-8')