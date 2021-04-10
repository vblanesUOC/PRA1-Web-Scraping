import pandas as pd

def limpiezaDomVirtual(df):
    # En los valores nulos, se colocará el valor 'NA' para ajustar el mismo al de mediamarkt
    df.fillna("NA", inplace=True)
    # Se aprecia que se encuentran nulos de la forma 'No indicado'. Por homogeneidad con el comando anterior,
    # se procederá a reemplazarlo por 'NA'
    df = df.replace('No indicado', 'NA')
    # Para las pulgadas, se encuentra el formato 31,2 cm (12.3") --> en donde tan solo interesa el número que se encuentra entre paréntesis
    df['pulgadas'] = df['pulgadas'].str.extract('\((.*?)"\)')
    #En caso de vacío, como antes, se pondrá NA
    df.fillna("NA", inplace=True)
    # Para el caso del peso (lo dejamos en kg), se eliminará la unidad de medida, dejando todas ellas en kg como en el caso de MediaMarkt
    # Para ello, haremos una nueva columna con el formato de float y sin las unidades, para poder operar en función de la medida
    df.loc[df['peso'].str.contains(pat=' g'), 'peso_sin_unidades'] = df['peso'].str.replace(' g', '')
    df.loc[df['peso'].str.contains(pat=' kg'), 'peso_sin_unidades'] = df['peso'].str.replace(' kg', '')
    #Se cambian las comas por puntos para facilitar su paso a float
    df['peso_sin_unidades'] = df['peso_sin_unidades'].str.replace(',', '.')
    df['peso_sin_unidades'] = df['peso_sin_unidades'].str.replace(' ', '')
    #En caso de nulo, se pondrá el valor 0
    df['peso_sin_unidades'] = df['peso_sin_unidades'].fillna(0)
    df['peso_sin_unidades'] = df['peso_sin_unidades'].astype(float)
    # Tras su creación, se puede realizar la distinción de entre g/kg y operar las medidas haciendo uso de la columna float que se ha generado
    # Nota: el resultado se vuelve a guardar como strinng por el hecho
    df.loc[df['peso'].str.contains(pat=' g'), 'peso'] = (df['peso_sin_unidades'] / 1000).astype(str)
    df.loc[df['peso'].str.contains(pat=' kg'), 'peso'] = df['peso_sin_unidades'].astype(str)
    # Se elimina la columna generada
    del df['peso_sin_unidades']

    # Para el caso del precio, si el mismo es mayor de 1000 la web suele introducir un espacio en blanco, este se eliminará, al igual que la unidad de medida, que se sobre entiende que es €
    df['precio_dominioVirtual'] = df['precio_dominioVirtual'].str.replace('€', '')
    df['precio_dominioVirtual'] = df['precio_dominioVirtual'].str.replace(' ', '')
    #Se cambian las comas por puntos para homogeneizarlo con las demás columnas
    df['precio_dominioVirtual'] = df['precio_dominioVirtual'].str.replace(',', '.')


    #Para el caso del modelo, nos quedaremos solo con el modelo en sí, que para hacerlo similar a mediamark, nos quedaremos con
    # el nombre que hay entre el primer espacio y la coma
    for x in  range(df['modelo'].size):
        #Encontramos la posición de empezar a recortar, en base a la marca (ya que siempre sale) y añadimos también la posición del espacio detrás de la marca
        start = df['modelo'][x].lower().find(df['marca'][x].lower()) + len(df['marca'][x]) + 1
        #La posición final será la primera coma después de la posición de inicio
        end = df['modelo'][x].find(',', start)
        #Si aparece el guión con espacios anteriores y posteriores, es que el producto no ha usado "," sino " - " como separación, por lo que se actualiza la posición final en base a este
        if " - " in df['modelo'][x][start:end]:
            end = df['modelo'][x].find(' -', start)
        #Para cada una se realiza el splitado
        df['modelo'][x]= df['modelo'][x][start:end]
        if(df['modelo'][x]==''):
            df['modelo'][x]='NA'


    #Para realizar la eliminación de duplicados, quedándonos con el de menor precio
    df = df.sort_values('precio_dominioVirtual', ascending=False).drop_duplicates('modelo').sort_index()
    return df

#### CARGA TABLETS DOMINIO VIRTUAL ####
#Se lee el csv y se guarda en un dataFrame, con la propiedad skipinitialspace ya que se encuentran muchos espacios en
# blanco en los registros, que darían problemas al fusionar ambas tablas
dfTabletsSinLimpiar = pd.read_csv ('../csv/dominioVirtual/tabletsDominioVirtualSinLimpiar.csv', skipinitialspace=True)
#Se pasa por la función creada
dfTabletsDominioVirtual = limpiezaDomVirtual(dfTabletsSinLimpiar)

################ CARGA PORTATILES DOMINIO VIRTUAL ################
dfOrdenadoresSinLimpiar = pd.read_csv ('../csv/dominioVirtual/portatilesDominioVirtualSinLimpiar.csv', skipinitialspace=True)
dfOrdenadoresDominioVirtual = limpiezaDomVirtual(dfOrdenadoresSinLimpiar)

################ CARGA MONITORES DOMINIO VIRTUAL ################
dfMonitoresSinLimpiar = pd.read_csv ('../csv/dominioVirtual/monitoresDominioVirtualSinLimpiar.csv', skipinitialspace=True)
dfMonitoresDominioVirtual = limpiezaDomVirtual(dfMonitoresSinLimpiar)

#print(dfTabletsDominioVirtual.to_string())
#print(dfOrdenadoresDominioVirtual.to_string())
#print(dfMonitoresDominioVirtual.to_string())

#Se genera el csv limpio
dfTabletsDominioVirtual.to_csv("tabletsDominioVirtual.csv", index=False, encoding='utf-8')
dfOrdenadoresDominioVirtual.to_csv("portatilesDominioVirtual.csv", index=False, encoding='utf-8')
dfMonitoresDominioVirtual.to_csv("monitoresDominioVirtual.csv", index=False, encoding='utf-8')
