# TODO Herramienta para analizar el texto de un pdf
# TODO Trigger o codigo que se ejecute permanentemente y a cierta hora realize algo

import schedule
import time
import requests
from bs4 import BeautifulSoup
from sharepoint import SharePoint
from datetime import date
import datetime
from shareplum import Site, Office365
import streamlit as st


from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import os
import json


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = '/'.join([ROOT_DIR, 'config.json'])

# read config file
with open(config_path) as config_file:
    config = json.load(config_file)
    config = config['share_point']


SHAREPOINT_URL = config['url']
SHAREPOINT_SITE = config['site']


USR = ""
PASSWD = ""


def set_credentials():
    try:
        usr = input("Ingrese su usuario de Wellperf: \n")
        passwd = input("Ingrese su contraseña: \n")
        creds = [usr, passwd]
        log = Office365(SHAREPOINT_URL,creds[0], creds[1]).get_cookies()
        print("Credenciales aprobadas.")
        return creds 
    except:
        print("Credenciales no validas!")

def get_petro_link():
    link = "https://www.eppetroecuador.ec/?p=3721" 
    data = requests.get(link).content
    soup = BeautifulSoup(data, "html.parser")
    foo = soup.find('a',string = 'Sumario de Operaciones').get('href')
    return foo 

def get_summary()->None:
    """Descarga el sumario de operaciones de petroecuador

    Args:
        text (_str_): Promt indicando la descarga
    """
   
    link = get_petro_link()
    print(link)
    data = requests.get(link).content
    with open('docs/sumario.pdf','wb') as file:
        file.write(data)


def month_name():
    datetime_object = datetime.datetime.strptime(str(date.today().month), "%m")
    full_month_name = datetime_object.strftime("%B")
    return full_month_name
    

def upload_to_sharepoint():
    # Setting the name of the file 
    file_name = "0" + str(date.today().day-1)+ "-" + "0" + str(date.today().day) + '_' + "Resumen" + str(date.today().year) + str(date.today().month) + '.pdf'
    path_to_file = 'docs/sumario.pdf'
    SharePoint(USR,PASSWD).upload_file(path_to_file, file_name,str(date.today().year)+"/"+str(date.today().month))
    print("Document in this` sharepoint location: " + month_name() + '/' + file_name)



def main():
    schedule.every().day.at("22:27").do(get_summary,'Sumario descargado')
    schedule.every().day.at("22:28").do(upload_to_sharepoint,'Documento en Sharepoint')

    # Loopd
    while True:
        schedule.run_pending()
        time.sleep(1) # wait one minute


if __name__ == '__main__':
    st.title("Petro web Scraping.")
    usr = st.text_input('Usuario: ')
    passwd = st.text_input('Contraseña: ', type="password")
    if st.button('Generar'):
        
        try:
            log = Office365(SHAREPOINT_URL,usr, passwd).get_cookies()
            USR = usr
            PASSWD = passwd
            st.warning("Credenciales aprobadas")
            get_summary()
            st.warning("Sumario descargado")
            upload_to_sharepoint()
            st.warning("Sumario en sharepoint")

        except:
            st.warning("Credenciales no aprobadas")

    
    
   




