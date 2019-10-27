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
from time import time 
#Todas las librerias necesarias para lograr crear el worldCloud, webScraping, timer para llevar el contador de cada metodo 
#además de los hilos para el paralelismo.

ctx = ssl.create_default_context()#Proporciona acceso al cifrado de seguridad y facilidades de autenticación
ctx.check_hostname = False#Verificar nombre de host. 
ctx.verify_mode = ssl.CERT_NONE


# Leer el html de la url y luego pasar esa información al beautifulsoup
url = 'https://www.cia.gov/library/publications/the-world-factbook/'
print("Opening the file connection...")
uh= urllib.request.urlopen(url, context=ctx)
print("HTTP status",uh.getcode())
html =uh.read().decode()
print(f"Reading done. Total {len(html)} characters read.")

soup = BeautifulSoup(html, 'html.parser') #Contiene la información del html la cual se utiliza para formar la nube y adquirir la informacion necesaria
#para el webscraping


country_codes=[]
country_names=[]
for tag in soup.find_all('option'):
    country_codes.append(tag.get('value')[5:7])
    country_names.append(tag.text)
#Almacena la cantidad de países que se van a consultarf para lograr crear los ciclos en base a la cantidad de ellos.
temp=country_codes.pop(0) 
temp=country_names.pop(0) 




urlbase = 'https://www.cia.gov/library/publications/the-world-factbook/geos/'
#Contiene la url a la cual se le van a hacer las peticiones de información 
global productos_Agricolas
global productos_Industriales

global productos_Agricolas2
global productos_Industriales2

#Variables que se utilizarán para crear la nube almacenando la informacion necesaria.


global tiempo_ejecucion_p1

def agriculturaParalelo2():
    
    agricultura=""
    tiempo_inicial = time()
    
    for i in range(1,len(country_names)-1):
        try:
            country_html=country_codes[i]+'.html'
            url_to_get=urlbase+country_html
           
            html = urllib.request.urlopen(url_to_get, context=ctx).read()
            soup = BeautifulSoup(html, 'html.parser')    
            
            txt=soup.get_text()
            pos1=txt.find('Agriculture - products:')
            
            if pos1!=-1: #entró
                   
                    for j in soup.find_all('div',id="field-agriculture-products"):
                        for tag in j:
                            for pro in tag: #pro son los productos
                                agricultura=agricultura+pro
         #Primer metodo paralelo, inicia en la posicion 0 y se va hasta el final de la lista de paises, cargando información de agricultura.             
        except:
            pass

        #termina de hacerlo y crea el wordcloud de agricultura
        if i==266:
            
            tiempo_final = time() 
     
            tiempo_ejecucion = tiempo_final - tiempo_inicial
            
            print ("\nEl tiempo de ejecucion del paralelo 2 fue :",tiempo_ejecucion/60)
                        
            procuctsparalel1 = WordCloud(width = 800, height = 800,
                          background_color = 'white',
                                      min_font_size = 10).generate(agricultura)
            procuctsparalel1.to_file('segundoparaleloagricultura.png')

def industriaParalelo2():
    
    industria=""
    


    for i in range(1,len(country_names)-1):
        try:
            country_html=country_codes[i]+'.html'
            url_to_get=urlbase+country_html
            
            html = urllib.request.urlopen(url_to_get, context=ctx).read()
            soup = BeautifulSoup(html, 'html.parser')    
            
            txt=soup.get_text()
            pos1=txt.find('Industries:')
            
            if pos1!=-1: #entró
                  
                    for j in soup.find_all('div',id="field-industries"):
                        for tag in j:
                            for pro in tag: #pro son los productos
                                industria=industria+pro
                      
        except:
            pass


        #termina y hace el cloudword de industria
        if i==266:
            
           
            procuctsparalel2 = WordCloud(width = 800, height = 800,
                          background_color = 'white',
                                      min_font_size = 10).generate(industria)
            procuctsparalel2.to_file('segudnoparaleloindustria.png')

secuencial() 
threading.Thread(target=agriculturaParalelo2).start()
threading.Thread(target=industriaParalelo2).start()
