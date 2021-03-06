#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
import re


def parse_specifications(category, category_url):
    """
    A partir de una categoria de productos y su URL, extrae automáticamente
    información técnica de ciertos productos de Mediamarkt.

    Arguments:
    * category: String, categoria de productos a extraer información
    * category_url: String, URL donde se sitúa el listado de un tipo de productos determinado

    Return:
    * d: Diccionario con la información técnica de productos

    """

    # Ejecución del driver de Chrome del que hace uso Selenium
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts)

    d = {
        "modelo": [],
        "marca": [],
        "pulgadas": [],
        "calidad_imagen": [],
        "sistema operativo": [],
        "peso": [],
        "precio_mediamarkt": []
    }

    # Request de la página objetivo a scrapear
    driver.get(category_url)

    # Click en el botón de aceptar cookies, que aparece al cargar la página
    cookies = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'privacy-layer-accept-all-button')))
    cookies.click()

    # Lista con todos los links a productos
    links_productos = driver.find_elements_by_xpath(
        '//a[contains(@href, "/es/product/")]')
    links_pag = []

    # Extracción de links de cada uno de los productos
    for tag_a in links_productos:
        links_pag.append(tag_a.get_attribute("href"))

    # Mostrar la cantidad de productos recogidos tras hacer los "scrolls"
    # print(len(links_pag))

    # Bucle para recoger la información dentro de cada producto
    for link in links_pag:
        # Espera de entre 1 y 1.5 segundos para evitar saturar el servidor
        sleep(random.uniform(1.0, 1.5))

        # Carga del link que contiene al producto (con #features, para cargar
        # desde el inicio el botón de "mostrar detalles")
        driver.get(link + "#features")

        try:
            # Espera para carga y click del botón "Mostrar detalles"
            boton = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//button[span[contains(text(), "Mostrar todos los detalles")]]')))
            boton.click()

            # Scroll para carga de características
            js = 'window.scrollTo({ left: 0, top: 0, behavior: "smooth" });'
            driver.execute_script(js)

            # Espera para carga características
            WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//td[span[contains(text(),"Color")]]'))
            )

            # Regex para recoger el modelo del producto a partir
            # del título de la página
            pattern_modelo = re.compile("- (.+?),")
            pattern_apple = re.compile("(.+?),")

            # Conjunto de XPath para encontrar características
            marca = driver.find_element_by_xpath(
                '//div[@data-test="mms-select-details-header"]/span/a/span').text

            if marca == "APPLE":
                modelo = driver.find_element_by_xpath('//h1').text
                modelo = pattern_apple.search(modelo).group(
                    1).replace(marca.title()+" ", "")
            else:
                modelo = driver.find_element_by_xpath('//h1').text
                modelo = pattern_modelo.search(modelo).group(
                    1).replace(marca.title()+" ", "")
            pulgadas = driver.find_element_by_xpath(
                '//td[span[contains(text(),"pulgadas")]]//following-sibling::td').text
            calidad_imagen = driver.find_element_by_xpath(
                '//td[span[contains(text(),"Calidad de imagen")]]//following-sibling::td').text
            precio = driver.find_element_by_xpath(
                '//span[@font-family="price"]').text
            # El sistema operativo no se recogerá si los productos son monitores
            if category != "monitores":
                sistema_operativo = driver.find_element_by_xpath(
                    '//td[span[contains(text(),"Sistema operativo")]]//following-sibling::td').text
            # El peso sólo se recogerá si los productos son monitores
            if category == "monitores":
                peso = driver.find_element_by_xpath(
                    '//td[span[contains(text(),"Peso")]]//following-sibling::td').text

            # Generación nueva entrada en diccionario
            # en base a los datos recogidos
            d["modelo"].append(modelo)
            d["marca"].append(marca)
            d["pulgadas"].append(pulgadas)
            d["calidad_imagen"].append(calidad_imagen)
            if category != "monitores":
                d["sistema operativo"].append(sistema_operativo)
            else:
                d["sistema operativo"].append("NA")

            if category == "monitores":
                d["peso"].append(peso)
            else:
                d["peso"].append("NA")
            d["precio"].append(precio)

        except Exception as e:
            # En caso de excepción, se muestra por pantalla el error y se
            # vuelve a la página principal para no parar la extracción
            print(e)
            driver.back()

    return d


opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
)

######################
# Monitores
######################

d = parse_specifications("monitores",
                        "https://www.mediamarkt.es/es/category/_monitores-701179.html")

df = pd.DataFrame(data=d)

for i in range(2,10):

    d = parse_specifications("monitores", "https://www.mediamarkt.es/es/category/_monitores-701179.html?page="+str(i))

    df2 = pd.DataFrame(data=d)

    df = df.append(df2, ignore_index=True)

df['precio'] = df['precio'].str.extract(r'(^\d+)')
df['pulgadas'] = df['pulgadas'].str.extract(r'(^\d+)')
df['peso'] = df['peso'].str.extract(r'(^\d+.\d+)')
df = df.sort_values('precio_mediamarkt', ascending=False).drop_duplicates('modelo').sort_index()

df.to_csv("../csv/mediamark/monitoresMediamarkt.csv", index=False, encoding='utf-8')

######################
# Portatiles
######################

d = parse_specifications(
    "portatiles", "https://www.mediamarkt.es/es/category/_port%C3%A1tiles-701175.html")

df = pd.DataFrame(data=d)

for i in range(2,10):

    d = parse_specifications("portatiles", "https://www.mediamarkt.es/es/category/_port%C3%A1tiles-701175.html?page="+str(i))

    df2 = pd.DataFrame(data=d)

    df = df.append(df2, ignore_index=True)

df['precio'] = df['precio'].str.extract(r'(^\d+)')
df['pulgadas'] = df['pulgadas'].str.extract(r'(^\d+)')
df = df.sort_values('precio_mediamarkt', ascending=False).drop_duplicates('modelo').sort_index()

df.to_csv("../csv/mediamark/portatilesMediamarkt.csv", index=False, encoding='utf-8')

######################
# Tablets
######################

d = parse_specifications(
    "tablets", "https://www.mediamarkt.es/es/category/_tablets-701178.html")

df = pd.DataFrame(data=d)

for i in range(2,10):

    d = parse_specifications("tablets", "https://www.mediamarkt.es/es/category/_tablets-701178.html?page="+str(i))

    df2 = pd.DataFrame(data=d)

    df = df.append(df2, ignore_index=True)

df['precio'] = df['precio'].str.extract(r'(^\d+)')
df['pulgadas'] = df['pulgadas'].str.extract(r'(^\d+)')
df = df.sort_values('precio_mediamarkt', ascending=False).drop_duplicates('modelo').sort_index()

df.to_csv("../csv/mediamark/tabletsMediamarkt.csv", index=False, encoding='utf-8')