# PRA1-Web-Scraping

Práctica 1 sobre Web Scraping de la asignatura Tipología y Ciclo de Vida de los datos de la UOC realizada por **Victor Blanes y Carlos Allo**

## ESTRUCTURA GITHUB

* Informe (Carpeta en donde se encontrará el informe final)
  * informe.pdf (Informe de la práctica en PDF)
* csv (Carpeta en donde se encontrarán los csv de la práctica)
  * dominioVirtual (Csv extraídos de la web dominio virtual)
    * monitoresDominioVirtual.csv (Csv extraído de la web dominio virtual con información sobre los monitores una vez limpiados)
    * monitoresDominioVirtualSinLimpiar.csv (Csv extraído de la web dominio virtual con información sobre los monitores directo de Scrapy, sin ser limpiado)
    * portatilesDominioVirtual.csv (Csv extraído de la web dominio virtual con información sobre los portátiles una vez limpiados)
    * portatilesDominioVirtualSinLimpiar.csv (Csv extraído de la web dominio virtual con información sobre los portátiles directo de Scrapy, sin ser limpiado)
    * tabletsDominioVirtual.csv (Csv extraído de la web dominio virtual con información sobre las tablets una vez limpiados)
    * tabletsDominioVirtualSinLimpiar.csv (Csv extraído de la web dominio virtual con información sobre las tablets directo de Scrapy, sin ser limpiado)
  * mediamark
    * monitoresMediamarkt.csv (Csv extraído de la web mediamark con información sobre monitores, que se obtiene directamente limpio)
    * portatilesMediamarkt.csv (Csv extraído de la web mediamark con información sobre portátiles, que se obtiene directamente limpio)
    * tabletsMediamarkt.csv (Csv extraído de la web mediamark con información sobre tablets, que se obtiene directamente limpio)
  * union_monitores.csv (Csv final resultante de la unión de las webs anteriores con información sobre monitores)
  * union_portatiles.csv (Csv final resultante de la unión de las webs anteriores con información sobre portátiles)
  * union_tablets.csv (Csv final resultante de la unión de las webs anteriores con información sobre tablets)
* src
  * MediaMarktSelenium.py (Ejecutable de Python a partir del cual se hace el web Scrapy de la web de MediaMark)
  * dominioVirtualMonitoresScrapy.py  (Ejecutable de Python a partir del cual se hace el web Scrapy de la web de DominioVirtual, de la sección de monitores)
  * dominioVirtualOrdenadoresScrapy.py  (Ejecutable de Python a partir del cual se hace el web Scrapy de la web de DominioVirtual, de la sección de ordenadores)
  * dominioVirtualTabletsScrapy.py  (Ejecutable de Python a partir del cual se hace el web Scrapy de la web de DominioVirtual, de la sección de tablets)
  * limpiezaDominioVirtual.py  (Ejecutable de Python que limpia y adapta los datos para realizar la unión posterior con MediaMarkt)
  * union.py  (Ejecutable de Python a partir del cual se realiza la unión de los csv)

## PAQUETES PYTHON NECESARIOS

Para poder ejecutar el programa, además de Python será necesario instalar algunas librerías propias del manejo de datos y de WebScrapy:
```
pip install requests
pip install lxml
pip install scrapy
pip install selenium
```

Al igual que esta última que permitirá cambiar la cabecera del navegador al hacer peticiones:
```
pip install Scrapy-UserAgents
```

## EJECUCIÓN PROGRAMA
### Web Scrapy de MediaMark

A través del comando de ejecución
```
python MediaMarktSelenium.py
```
Se ejecutará el programa que dará como resultado los 3 csv de las categorías de Medimark

### Web Scrapy de Dominio Virtual 

A través de estos 3 comandos, se ejecutarán los ejecutables referidos a Dominio Virtual:
```
scrapy runspider dominioVirtualTabletsScrapy.py -o tabletsDominioVirtualSinLimpiar.csv -t csv
scrapy runspider dominioVirtualOrdenadoresScrapy.py -o portatilesDominioVirtualSinLimpiar.csv -t csv
scrapy runspider dominioVirtualMonitoresScrapy.py -o monitoresDominioVirtualSinLimpiar.csv -t csv
```
Estos generarán los csv sin limpiar de dominio virtual, en donde para limpiar los mismos se ejecutara:
```
python limpiezaDominioVirtual.py
```
Que dará como resultados los csv de dominio virtual limpios

### Unión de csv de diferentes webs

Una vez generados todos los csv, mediante el programa union se hará la fusión de estos
```
python union.py
```
Obteniendo de esta forma los csv finales 
