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
    
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts)

    d = {
        "modelo": [],
        "marca": [],
        "pulgadas": [],
        "calidad_imagen": [],
        "sistema operativo": [],
        "peso": [],
        "precio": []
    }
    
    driver.get(category_url)

    cookies = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'privacy-layer-accept-all-button')))
    cookies.click()

    mas_productos = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@data-test="mms-search-srp-loadmore"]')))
    mas_productos.click()

    for i in range(5):
        js_down = 'window.scrollTo({ left: 0, top: document.body.scrollHeight/1.2, behavior: "smooth" });'
        js_up= 'window.scrollTo({ left: 0, top: document.body.scrollHeight/3, behavior: "smooth" });'
        driver.execute_script(js_down)
        sleep(2.5)
        driver.execute_script(js_up)
        sleep(1.5)

    for i in range(5):
        js_down = 'window.scrollTo({ left: 0, top: document.body.scrollHeight/1.1, behavior: "smooth" });'
        js_up= 'window.scrollTo({ left: 0, top: document.body.scrollHeight/4, behavior: "smooth" });'
        driver.execute_script(js_down)
        sleep(2.5)
        driver.execute_script(js_up)
        sleep(1.5)

    # Lista con todos los links a productos
    links_productos = driver.find_elements_by_xpath('//a[contains(@href, "/es/product/")]')
    links_pag = []

    for tag_a in links_productos:
        links_pag.append(tag_a.get_attribute("href"))

    print(len(links_pag))

    for link in links_pag:
        sleep(random.uniform(1.0, 1.5))
        driver.get(link + "#features")
        try:
            # Espera para carga botón "Mostrar detalles"
            boton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[span[contains(text(), "Mostrar todos los detalles")]]')))
            boton.click()

            # Scroll para carga de características
            js = 'window.scrollTo({ left: 0, top: 0, behavior: "smooth" });'
            driver.execute_script(js)

            # Espera para carga características
            WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, '//td[span[contains(text(),"Color")]]'))
            )

            pattern_modelo = re.compile("- (.+?),")

            # XPath para encontrar características
            marca = driver.find_element_by_xpath('//div[@data-test="mms-select-details-header"]/span/a/span').text
            modelo = driver.find_element_by_xpath('//h1').text
            modelo = pattern_modelo.search(modelo).group(1).replace(marca.title()+" ", "")
            pulgadas = driver.find_element_by_xpath('//td[span[contains(text(),"pulgadas")]]//following-sibling::td').text
            calidad_imagen = driver.find_element_by_xpath('//td[span[contains(text(),"Calidad de imagen")]]//following-sibling::td').text
            precio = driver.find_element_by_xpath('//span[@font-family="price"]').text
            if category != "monitores":
                sistema_operativo = driver.find_element_by_xpath('//td[span[contains(text(),"Sistema operativo")]]//following-sibling::td').text
            if category == "monitores":
                peso = driver.find_element_by_xpath('//td[span[contains(text(),"Peso")]]//following-sibling::td').text

            # Generación nueva entrada en diccionario
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

            driver.back()

        except Exception as e:
            print(e)
            driver.back()

    return d


opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
)

######################
## Monitores
######################

d = parse_specifications("monitores","https://www.mediamarkt.es/es/category/_monitores-701179.html")

df = pd.DataFrame(data=d)

df['precio']=df['precio'].str.extract(r'(^\d+)')
df['pulgadas']=df['pulgadas'].str.extract(r'(^\d+)')
df['peso']=df['peso'].str.extract(r'(^\d+.\d+)')

df.to_csv("monitores.csv", index = False, encoding = 'utf-8')

######################
## Portatiles
######################

d = parse_specifications("portatiles", "https://www.mediamarkt.es/es/category/_port%C3%A1tiles-701175.html")

df = pd.DataFrame(data=d)

df['precio']=df['precio'].str.extract(r'(^\d+)')
df['pulgadas']=df['pulgadas'].str.extract(r'(^\d+)')

df.to_csv("portatiles.csv", index = False, encoding = 'utf-8')

######################
## Tablets
######################

d = parse_specifications("tablets","https://www.mediamarkt.es/es/category/_tablets-701178.html")

df = pd.DataFrame(data=d)

df.to_csv("tablets.csv", index = False, encoding = 'utf-8')