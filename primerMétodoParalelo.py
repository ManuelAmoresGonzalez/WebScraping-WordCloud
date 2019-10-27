import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import threading 
from time import time #Todas las librerias necesarias para lograr crear el worldCloud, webScraping, timer para llevar el contador de cada metodo 
#además de los hilos para el paralelismo.

ListaAgricultura=[]
ListaIndustria=[]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



url = 'https://www.cia.gov/library/publications/the-world-factbook/'
print("Opening the file connection...")
uh= urllib.request.urlopen(url, context=ctx)
print("HTTP status",uh.getcode())
html =uh.read().decode()
print(f"Reading done. Total {len(html)} characters read.")

soup = BeautifulSoup(html, 'html.parser') #tiene el código html


country_codes=[]
country_names=[]
for tag in soup.find_all('option'):
    country_codes.append(tag.get('value')[5:7])
    country_names.append(tag.text)#Almacena la cantidad de países que se van a consultarf para lograr crear los ciclos en base a la cantidad de ellos.

temp=country_codes.pop(0)
temp=country_names.pop(0) 

#imprimir paises


# Base URL
urlbase = 'https://www.cia.gov/library/publications/the-world-factbook/geos/'

global productos_Agricolas
global productos_Industriales

global productos_Agricolas2
global productos_Industriales2

global listAgricola
global lisIndustrial
listAgricola=[]
lisIndustrial=[]

global tiempo_ejecucion_p1

def paralelo1():
   
    print("\nIniciando Paralelo\n")
 
    productos_Agricolas=""
    productos_Industriales=""



    for i in range(1,len(country_names)//2):
        try:
            country_html=country_codes[i]+'.html'
            url_to_get=urlbase+country_html
     
            html = urllib.request.urlopen(url_to_get, context=ctx).read()
            soup = BeautifulSoup(html, 'html.parser')    
            
            txt=soup.get_text()
            pos1=txt.find('Agriculture - products:')
     
    
            if pos1!=-1: #entró
                    print(i)
                    for j in soup.find_all('div',id="field-agriculture-products"):
                        for tag in j:
                            for pro in tag: #pro son los productos
                                productos_Agricolas=productos_Agricolas+pro
                                listAgricola.append(pro)
                    
            for m in soup.find_all('div',id="field-industries"):
                for tag in m:
                    for ind in tag:
                        productos_Industriales=productos_Industriales+ind
                        lisIndustrial.append(ind)
                                     
        except:
            pass
            

def paralelo2():    

    productos_Agricolas2=""
    productos_Industriales2=""

    tiempo_inicial = time()

    for i in range(len(country_names)//2,len(country_names)-1):
        try:
            country_html=country_codes[i]+'.html'
            url_to_get=urlbase+country_html
            
            html = urllib.request.urlopen(url_to_get, context=ctx).read()
            soup = BeautifulSoup(html, 'html.parser')    
            
            txt=soup.get_text()
            pos1=txt.find('Agriculture - products:')
            
            if pos1!=-1: #entró
                    print(i)
                    for j in soup.find_all('div',id="field-agriculture-products"):
                        for tag in j:
                            for pro in tag: #pro son los productos
                                productos_Agricolas2=productos_Agricolas2+pro
                    
            for m in soup.find_all('div',id="field-industries"):
                for tag in m:
                    for ind in tag:
                        productos_Industriales2=productos_Industriales2+ind
                                     
        except:
            pass
               
        if i == 266:
            tiempo_final = time() 
            tiempo_ejecucion = tiempo_final - tiempo_inicial

        
            print ("\nEl tiempo de ejecucion del paralelo 2 fue :",tiempo_ejecucion) #En segundos
            
            productos_Agricolas = " ".join(listAgricola)
            productos_Industriales = " ".join(lisIndustrial)
            A = productos_Agricolas2 + productos_Agricolas
            
            I = productos_Industriales + productos_Industriales2 
            
            procuctsparalel = WordCloud(width = 800, height = 800,
                      background_color = 'white',
                      
                                  min_font_size = 10).generate(A)
            procuctsparalel.to_file('primerparaleloagricola.png')
            
            industrieparalel = WordCloud(width = 800, height = 800,
                                  background_color = 'white',
                                  
                                  min_font_size = 10).generate(I)
            industrieparalel.to_file('primerparaleloindustrial.png')


threading.Thread(target=paralelo1).start()
threading.Thread(target=paralelo2).start()
