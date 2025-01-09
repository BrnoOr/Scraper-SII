from bs4 import BeautifulSoup
import requests
from lxml import etree
from datetime import datetime, date
import re
import pandas as pd


import warnings
warnings.filterwarnings("ignore")

# Obtención de los urls para hacer scraping
year = date.today().year
anios = list(range(2014,year + 1,1))
urls_uf = [f'https://www.sii.cl/valores_y_fechas/uf/uf{anio}.htm' for anio in anios]
urls_dolar = [f'https://www.sii.cl/valores_y_fechas/dolar/dolar{anio}.htm' for anio in anios]

# Extraccion de datos
data_uf = pd.DataFrame(columns=['Día','Mes','UF'])
data_dolar = pd.DataFrame(columns=['Día','Mes','Dolar'])

for anio in anios:
    page_uf = requests.get(f'https://www.sii.cl/valores_y_fechas/uf/uf{anio}.htm')
    page_dolar = requests.get(f'https://www.sii.cl/valores_y_fechas/dolar/dolar{anio}.htm')
    soup_uf = BeautifulSoup(page_uf.text,'html.parser')
    soup_dolar = BeautifulSoup(page_dolar.text,'html.parser')
    df_uf = pd.read_html(str(soup_uf.find('table',{'id':'table_export'})))[0].melt(id_vars=["Día"], var_name="Mes", value_name="UF")
    df_dolar = pd.read_html(str(soup_dolar.find('table',{'id':'table_export'})))[0].melt(id_vars=["Día"], var_name="Mes", value_name="Dolar")
    data_uf = pd.concat([data_uf,df_uf.dropna()],ignore_index=False)
    data_dolar = pd.concat([data_dolar,df_dolar.dropna()],ignore_index=False)

# Falta corregir el tipo de dato de dolar y UF