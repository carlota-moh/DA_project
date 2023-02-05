# Proyecto DA - Spider, Crawler, Wrangler

Este es un proyecto de workflow de adquisición de datos, realizado como práctica en un curso de Adquisición de Datos. 
El objetivo del proyecto es recuperar información de las páginas de Wikipedia de las universidades del mundo. 
Para ello, el proyecto utiliza tres módulos:

+ Spider: Se encarga de recuperar las URLs de la Wikipedia que contienen perfiles de universidades.
+ Crawler: Parsea el contenido HTML de la tarjeta resumen de cada una de las universidades.
+ Wrangler: Se encarga de la limpieza de datos y de realizar ciertas comprobraciones acerca de la información recopilada.

## Ejecución del script

El proyecto se ejecuta desde el directorio raíz usando:

`python3 main`

Las partes del proyecto se pueden ejecutar por separado,
aunque debe tenerse en cuenta que son secuenciales. Para ejecutar
una sección simplemente se debe añadir su nombre como argumento
en la terminal:

`python3 main SPIDER <country_name/>`
`python3 main CRAWLER <country_name/>`
`python3 main WRANGLER <country_name/>`

Para ejecutar todas las secciones, emplear:
`python3 main SPIDER CRAWLER WRANGLER <country_name/>`

## Notas sobre escalado

Si quisiéramos escalar el proyecto para poder recuperar la información
de todas las universidades del mundo, en vez de pasar el nombre de un
país en concreto a través de argumentos en consola deberíamos modificar
el módulo `spider.py` (concretamente, la función `spider_university`) 
para que recuperara de una en una la lista de universidades de cada uno 
de los países contenidos en `countries.csv`. A continuación, encadenaríamos 
lo módulos `crawler.py` y `wrangler.py` para que se ejecutaran sobre 
cada uno de ellos. 

A la hora de escalar el proyecto, es predecible encontrarse con algunos de
los siguientes problemas:

1. Falta de homogeneidad en las páginas que listan las universidades de cada país,
lo que hace que sea difícil automatizar la recuperación de los links de las 
universidades.

2. Falta de homogeneidad en las páginas de wikipedia de las propias universidades, 
lo que causa que no podamos recuperar la información (ej: no hay un infobox card,
la información contenida en dicho infobox no es siempre la misma y hay campos que
faltan, etc).

3. Dificultad a la hora de depurar errores, puesto que se trata de un proyecto muy
grande, por lo que habría que revisar logs eternos donde hay millones de universidades
con probabes puntos de fallo.

4. Cambios inesperados en la estructura del HTML, lo que puede hacer que la información 
que podemos recuperar hoy no la podamos recuperar el día de mañana.
