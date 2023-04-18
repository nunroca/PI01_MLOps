<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>
# <h2 align=center> **NUN ESTEBAN ROCA CARBAJAL** </h2>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

## ¡Bienvenidos a mi primer proyecto individual de la etapa de labs!

<p align=center><img src=https://thedatascientist.com/wp-content/uploads/2019/06/what-is-data-science.jpg><p>

<hr>  

## Resumen del Proyecto
Se cuenta con data de streaming.conteniendo informaciñon tanto peliculas y series, los directores artistas, año de salida, duracion, contenido, etc.

Haciendo uso de lo aprendido en el trancurso de todo el programa de herny , se desarollara lo requerido,teniendo como objetivo mostrar una data accesible por medio web.


<hr>  


## Transformaciones - ETL:

Se realizan los cambios a la data base, segun lo solicitado:

+ Generar campo **`id`**: Cada id se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = **`as123`**)

+ Los valores nulos del campo rating deberán reemplazarse por el string “**`G`**” (corresponde al maturity rating: “general for all audiences”

+ De haber fechas, deberán tener el formato **`AAAA-mm-dd`**

+ Los campos de texto deberán estar en **minúsculas**, sin excepciones

+ El campo ***duration*** debe convertirse en dos campos: **`duration_int`** y **`duration_type`**. El primero será un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas)


            La data resultante sera el archivo: DataLab01.csv


<hr>

## Desarrollo de la API:

Se desarolla una API, que hara uso de funciones para el llamado de la data anteriormente trabajada, suiguiendo una estructura en las respuestas.

Funciones de la API:

+ /get_max_duration/{anio}/{plataforma}/{dtype}
+ /get_score_count/{plataforma}/{scored}/{anio}
+ get_count_platform/{plataforma}
+ /get_actor/{plataforma}/{anio}
+ /prod_per_county/{tipo}/{pais}/{anio}
+ /get_contents/{rating}

            Todo el codigo de las consultas, se encuentran en el archivo: main.py


<hr> 

## Analisis Exploratorio - EDA:

Como parte del analisis, evaluamos la data que sera requerida y trabajada en la etapa de Machine Learnig.

Filtramos la data requerida, y revisamos si cuenta con datos nulos, datos repetido, estandarizamos los textos, acortamos a lo requerido y unimos en una sola columna para el analisis requerido.

La data trbajada son las columnas ["title","listed_in"], que nos facilitan la información de los titulosy generos de las peliculas, lo cual se concatenara en una sola columna que sera luego trabaja por ML.

            La data resultante sera el archivo: DataRecomen.csv


<hr>

## Sistema de recomendacion - ML :

En esta etapa hacemos uso de nuestra data trabajada en el EDA, ya habiendo conocido de lo requerido por ML, con esto es momento de desarrollar un modelo de recomendación.

Este modelo de recomendacion, consiste en obtener un dato de titulo de pelicula, y entregar 5 peliculas recomendadas, siendo analizado por el nombre de la pelicula y su genero.

Tecnicamente este proceso, consiste en vectorizar toda la columna de data trabaja en el EDA, y establecer una similitud por cosenos, con el titulo como variable administrada, se filtra la linea de similitudes de la matris, y se ordena de mayor menor, seleccionado los 5 primeros con similitudes mas altas.

            LA funcion desarrollada se encuentra contenida en el archivo: main.py


<hr>

## Deployment - Render :

Para tener el acceso via web a la ejecuccion de la API, se carga los archivos en los servidores de RENDER

<p align=center><img src=https://th.bing.com/th/id/OIP.045ArS-D5OMZ4AOdB8uDCwHaEK?w=289&h=180&c=7&r=0&o=5&pid=1.7><p>


      El link de acceso a la API:   https://pi01-mlops.onrender.com/


<hr>

## Video:




## **Fuente de datos**

+ [Dataset](https://drive.google.com/drive/folders/1b49OVFJpjPPA1noRBBi1hSmMThXmNzxn):



