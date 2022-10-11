# TODO Herramienta para analizar el texto de un pdf
# TODO Trigger o codigo que se ejecute permanentemente y a cierta hora realize algo

import schedule
import time
import requests
import logging 

from sharepoint import SharePoint
from datetime import date
import datetime
from shareplum import Site, Office365
import streamlit as st
import bs4 as bs



import os
import json

# starting login file 
logging.basicConfig(filename="log.txt", level = logging.DEBUG,
                    format="%(asctime)s %(message)s")

# set root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = '/'.join([ROOT_DIR, 'config.json'])

# read config file
with open(config_path) as config_file:
    config = json.load(config_file)
    config = config['share_point']

# take data from json file
SHAREPOINT_URL = config['url']
SHAREPOINT_SITE = config['site']

# Global variables
USR = ""
PASSWD = ""


def set_credentials(usr,passwd):
    try:
        
        Office365(SHAREPOINT_URL,usr, passwd).get_cookies()
        logging.info("Login exitoso.")
    except:
        logging.error("Credenciales invalidas.")

def get_petro_link():
    """ Obtiene el link del pdf.

    Returns:
        _type_: Link
    """
    link = "https://www.eppetroecuador.ec/?p=3721" 
    try: 
        data = requests.get(link).content
        soup = bs.BeautifulSoup(data, "html.parser")
        pdf_link = soup.find('a',string = 'Sumario de Operaciones').get('href')

        logging.info("Se encontro el link de descarga.")
        return pdf_link
    except:
        logging.info("El link de descarga no se encontro en el scraping.")
        return None


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
    try: 
        SharePoint(USR,PASSWD).upload_file(path_to_file, file_name,str(date.today().year)+"/"+str(date.today().month))
        logging.info("Documento subido a Sharepoint.")
    except:
        logging.error("El documento no se ha subido en Sharepoint.")



# def main():
#     schedule.every().day.at("18:30").do(get_summary,'Sumario descargado')
#     schedule.every().day.at("18:31").do(upload_to_sharepoint,'Documento en Sharepoint')

#     # Loopd
#     while True:
#         schedule.run_pending()
#         time.sleep(1) # wait one minute


if __name__ == '__main__':
    # st.title("Petro web Scraping.")
    # usr = st.text_input('Usuario: ')
    # passwd = st.text_input('Contraseña: ', type="password")
    # if st.button('Generar'):
        
    #     try:
    #         log = Office365(SHAREPOINT_URL,usr, passwd).get_cookies()
    #         USR = usr
    #         PASSWD = passwd
    #         st.warning("Credenciales aprobadas")
    #         get_summary()
    #         st.warning("Sumario descargado")
    #         upload_to_sharepoint()
    #         st.warning("Sumario en sharepoint")

    #     except:
    #         st.warning("Credenciales no aprobadas")
    pass 
    
    
   




