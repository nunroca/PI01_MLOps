from fastapi import FastAPI
import pandas as pd 
import numpy as np
from fastapi.responses import RedirectResponse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

app= FastAPI() 

df_titles=pd.read_csv("DataLab01.csv") 
df_recom=pd.read_csv("DataRecomen.csv") 

#configuramos un pequeño index para que no quede vacio
@app.get("/")
async def index():
    return RedirectResponse("https://pi01-mlops.onrender.com/docs")



############ DESARROLLO API ################

    
@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}',tags=["1. Desarrollo de API"])

async def get_max_duration(year:int, platform:str,duration_type:str): 
    """
       FUNCION #1 Pelicula con Mayor Duración\n
            Parameters º1 : Year (Int)          - [1920,1922,....,2020,2021] \n
            Parameters º2 : Platform (Str)      - [Disney,Hulu,Netflix,Amazon] \n
            Parameters º3 : Duration Type (Str) - [min,season]\n
    """
        
    # capturamos el dataframe transformado desde la variable global
    titles=df_titles
    
    df_filter = titles[(titles['release_year']==year) & (titles['platform'].str.contains(platform)) & (titles['duration_type'].str.contains(duration_type))]
    
    # se optiene el valor maximo de la columna "duration_int" y lo utilizamos como un segundo filtro
    resultado = df_filter[df_filter['duration_int'] == df_filter['duration_int'].max()].iloc[0]

    return {"pelicula" :resultado["title"]}



@app.get('/get_score_count/{platform}/{score}/{year}',tags=["1. Desarrollo de API"])
async def get_score_count(platform:str, score:float, year:int):
    
    """
       FUNCION #2 Cantidad de Peliculas por Plataforma, por score mayor a y por año\n
            Parameters º1 : Platform (Str)      - [disney,hulu,netflix,amazon] \n
            Parameters º2 : Score (float)       - [3.3,....,3.7] \n
            Parameters º3 : Year (Int)          - [1920,1922,....,2020,2021]\n
    """ 
    titles=df_titles
    
    # se filtra el dataframe por año y plataforma
    df_filter =titles[(titles["release_year"]==year) & (titles['id'].str.contains(platform[0], case= False))]
    
    # se calcula el promedio de los rating por pelicula
    df_result = df_filter[df_filter['rating_y']> score]
    
   
    return {"plataforma":platform,
            "cantidad":len(df_result),
            "anio":year,
            "score":score}





@app.get('/get_count_platform/{platform}',tags=["1. Desarrollo de API"])
async def get_count_platform(platform:str):
    """
       FUNCION #3 Cantidad de Peliculas por Plataforma\n
            Parameters º1 : Platform (Str)      - [disney,hulu,netflix,amazon] \n
    """
    titles=df_titles
    
    # se realiza el filtro por plataforma
    df_filter = titles[titles['id'].str.contains(platform[0], case= False)]
    
    # se obtiene la cantidad de registros depues de los filtros
    result = df_filter['id'].count()
    
    return {"plataforma": platform
            , "peliculas": int(result) }





@app.get('/get_actor/{plataforma}/{year}',tags=["1. Desarrollo de API"])
async def get_actor(platform:str, year:int):
    """
        FUNCION #4: Actor que mas se repite por plataforma y año \n
            Parameters º1 : Platform (Str)      - [disney,hulu,netflix,amazon] \n
            Parameters º3 : Year (Int)          - [1920,1922,....,2020,2021]\n
    """
    titles=df_titles
    
    # se realiza un filtro con las variables obligatorias
    df_filter = titles[(titles['platform']==platform) & (titles['release_year']==year)]
    
    # se reemplaza los registros vacion de la columna "cast" con un string "vacio" para efectos de la consigna
    df_filter['cast'].fillna('vacio', inplace=True)
    
    # se elimina los registros con datos vacios en la columan "cast"
    df_filter_no_empty = df_filter[df_filter['cast']!='vacio']
    
    # se reemplaza el coma y espacio(", ") con solamente el coma(",") para no tener espacions en blanco
    df_filter_no_space = df_filter_no_empty['cast'].str.replace(', ',',')
    # se realiza la separacion los nombres de los actores y actrices utilizando for y guardandolos en un arreglo
    lista=[]
    for i in df_filter_no_space:
        s=i.split(',')
        for j in range(len(s)):
            if s[j] not in lista:
                lista.append(s[j])
            else:
                pass         
    lista= list(set(lista))
    
    # se realiza la elaboracion de un diccionario que almacena el nombre e los actores con la cantidad de veces que aparecen
    count = 0
    dict = {}
    for i in lista:
        for j in df_filter_no_space:
            if i in j.split(','):
                count +=1
        dict[i] = count
        
    # se obtiene el valor maximo de cantidad de apariciones
    actor = max(dict, key = dict.get)
    
    return {"plataforma":platform,
            "anio":year,
            "actor":actor,
            "apariciones":str(dict[actor])
            }




@app.get('/prod_per_county/{tipo}/{pais}/{anio}',tags=["1. Desarrollo de API"])

async def prod_per_county(type: str, country: str, year: int):
 
    """
       FUNCION #5 Diccionario filtrado por tipo de contenido, pais, año\n
            Paraneters º1 : type (str)          - [tv show,movie] \n
            Parameters º2 : country (Str)       - [france,canada,india,etc] \n
            Parameters º3 : Year (Int)          - [1920,1922,....,2020,2021]\n
    """
       
    titles=df_titles
    df_filter = titles[(titles['type']==type) & (titles['country']==country) & (titles['release_year']==year)]
    df1=df_filter[["country","release_year","title"]]
    df2=df1.to_dict()
    
    return {"pais":df1["release_year"].tolist(),"anio":df1["country"].tolist(),"peliculas":df1["title"].tolist()}





@app.get('/get_contents/{rating}',tags=["1. Desarrollo de API"])
def get_contents(rating: str):
    """
       FUNCION #6 Cantida de peliculas segun el tipo de rating\n
            Paraneters º1 : ratimng (str)          - [g,13+,17+,18+,16+,etc] \n

    """
    titles=df_titles
    df_filter = titles[(titles['rating_x']==rating)]
    respuesta=df_filter["rating_x"].count()
          
    return {"rating":rating, 
            "contenido":int(respuesta)
            }


@app.get('/get_recomendation/{title}', tags=["2. Sistema de Recomendación"])
def get_recomendation(title: str):
    """
        SISTEMA DE RECOMENDACIÓN \n
            Se vectorizalos titulos, y se establece una similitud por cosenos\n
    
    """
    data1=df_recom
    data2=df_titles
    
    # Vectorizamos la columna de titulos
    vector=TfidfVectorizer(sublinear_tf=True, stop_words='english')
    tf_matrix=vector.fit_transform(data1["title_list"])
    
    # Establecemos una matriz de similitudes por cosenos
    cosine=cosine_similarity(tf_matrix)
    
    #sacamos el indice del titulo a buscar y extraemos la linea de similitudes de la matriz
    index=data2.index[data2["title"]==title.lower()].tolist()[0]
    cosine=cosine[index]
    
    #ordenamos la fila y extraemos los 5 primeros
    mossimp=cosine.argsort()[::-1]
    top=mossimp[1:6]
    
    # creamos la lista de recomendados recorriendolo con un FOR
    recome=data2.iloc[[i for i in top]]["title"].tolist()
    
    return {'recomendacion':recome}

