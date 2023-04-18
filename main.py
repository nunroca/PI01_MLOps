from fastapi import FastAPI
import pandas as pd 
import numpy as np
from fastapi.responses import RedirectResponse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

app= FastAPI() 

df_titles=pd.read_csv("DataLab01.csv") 
df_recom=pd.read_csv("DataRecomen.csv") 

#configuramos un pequeño index para que no quede vacio
@app.get("/")
async def index():
    #return RedirectResponse("https://pi01-mlops.onrender.com/docs")
    return RedirectResponse("http://127.0.0.1:8000/docs")
    


############ DESARROLLO API ################

    
@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}',tags=["1. Desarrollo de API"])

async def get_max_duration(anio:int, plataforma:str,dtype:str): 
    """
       FUNCION #1 Pelicula con Mayor Duración\n
            Parameters º1 : anio (Int)          - [1920,1922,....,2020,2021] \n
            Parameters º2 : plataforma (Str)    - [disney,hulu,netflix,amazon] \n
            Parameters º3 : dtype (Str)         - [min]\n
    """
        
    # capturamos el dataframe transformado desde la variable global
    titles=df_titles
    
    df_filter = titles[(titles['release_year']==anio) & (titles['platform'].str.contains(plataforma)) & (titles['duration_type'].str.contains(dtype))]
    
    # se optiene el valor maximo de la columna "duration_int" y lo utilizamos como un segundo filtro
    respuesta = df_filter[df_filter['duration_int'] == df_filter['duration_int'].max()].iloc[0]

    return {"pelicula" :respuesta["title"]}



@app.get('/get_score_count/{plataforma}/{scored}/{anio}',tags=["1. Desarrollo de API"])
async def get_score_count(plataforma:str, scored:float, anio:int):
    
    """
       FUNCION #2 Cantidad de Peliculas por Plataforma, por score mayor a y por año\n
            Parameters º1 : plataforma (Str)  - [disney,hulu,netflix,amazon] \n
            Parameters º2 : scored (float)    - [3.3,....,3.7] \n
            Parameters º3 : anio (Int)        - [1920,1922,....,2020,2021]\n
    """ 
    titles=df_titles
    
    # se filtra el dataframe por año y plataforma
    df_filter =titles[(titles["release_year"]==anio) & (titles['id'].str.contains(plataforma[0], case= False))]
    #se hace un filtro para que sean solo peliculas
    df_filter=df_filter[df_filter['type']=="movie"]
    # se calcula el promedio de los rating por pelicula
    respuesta = len(df_filter[df_filter['rating_y']> scored])
    
   
    return {"plataforma":plataforma,
            "cantidad":respuesta,
            "anio":anio,
            "score":scored}





@app.get('/get_count_platform/{plataforma}',tags=["1. Desarrollo de API"])
async def get_count_platform(plataforma:str):
    """
       FUNCION #3 Cantidad de Peliculas por Plataforma\n
            Parameters º1 : plataforma (Str)    - [disney,hulu,netflix,amazon] \n
    """
    titles=df_titles
    
    # se realiza el filtro por plataforma
    df_filter = titles[titles['id'].str.contains(plataforma[0], case= False) & (titles['type']=="movie")]
    
    # se obtiene la cantidad de registros depues de los filtros
    resultado = int(df_filter['id'].count())
    
    return {"plataforma": plataforma
            , "peliculas": resultado }





@app.get('/get_actor/{plataforma}/{anio}',tags=["1. Desarrollo de API"])
async def get_actor(plataforma:str, anio:int):
    """
        FUNCION #4: Actor que mas se repite por plataforma y año \n
            Parameters º1 : plataforma (Str)   - [disney,hulu,netflix,amazon] \n
            Parameters º2 : anio (Int)         - [1920,1922,....,2020,2021]\n
    """
    titles=df_titles
    
    # se realiza un filtro con las variables obligatorias
    df_filter = titles[(titles['platform']==plataforma) & (titles['release_year']==anio)]
    
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
    resultado1 = max(dict, key = dict.get)
    resultado2 =int(dict[resultado1])

    return {"plataforma":"netflix",
            "anio":"2020",
            "actor":resultado1,
            "apariciones":resultado2}
    



@app.get('/prod_per_county/{tipo}/{pais}/{anio}',tags=["1. Desarrollo de API"])

async def prod_per_county(tipo: str, pais: str, anio: int):
 
    """
       FUNCION #5 Diccionario filtrado por tipo de contenido, pais, año\n
            Paraneters º1 : tipo (str)    - [tv show  ,  movie] \n
            Parameters º2 : pais (Str)    - [france  ,  canada  ,  india,etc] \n
            Parameters º3 : anio (Int)    - [1920,1922,....,2020,2021]\n
    """
       
    titles=df_titles
    # hacemos filtro por tipo y por anio  
    df_filter = titles[(titles['type']==tipo) & (titles.release_year==anio) & (titles.country.str.contains(pais))]
    
    
    
    resultado=int(len(df_filter[["country","release_year","type"]]))
    
    
    return {"pais":pais,"anio":anio,"contenido":resultado}





@app.get('/get_contents/{rating}',tags=["1. Desarrollo de API"])
def get_contents(rating: str):
    """
       FUNCION #6 Cantida de peliculas segun el tipo de rating\n
            Paraneters º1 : rating (str)          - [g,13+,17+,18+,16+,etc] \n

    """
    titles=df_titles
    df_filter = titles[(titles['rating_x']==rating)]
    respuesta=int(df_filter["rating_x"].count())
          
    return {"rating":rating, 
            "contenido":respuesta
            }





############# SISTEMA DE RECOMENDACION #####################





@app.get('/get_recomendation/{title}', tags=["2. Sistema de Recomendación"])
def get_recomendation(title: str):
    """
        SISTEMA DE RECOMENDACIÓN \n
            Se vectorizalos titulos, y se establece una similitud por cosenos\n
    
    """
  
    data2=df_titles
    
    data1=df_recom.head(5000)
    # Vectorizamos la columna de titulos
    vector=TfidfVectorizer(sublinear_tf=True, min_df=0.1,max_df=0.3,stop_words='english')
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

