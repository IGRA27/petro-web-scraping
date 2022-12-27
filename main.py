import logging 
logging.basicConfig(filename="log.txt", level = logging.DEBUG,
                        format="%(asctime)s %(message)s")
import requests
import datetime
import bs4 as bs
import os
import json
import schedule
import time
from sharepoint import SHAREPOINT_SITE, SHAREPOINT_URL, SharePoint
from datetime import date
from shareplum import Office365
from dotenv import load_dotenv

load_dotenv()
WELLPERF_USER = os.getenv('WELLPERF_USER')
PASSWD = os.getenv('PASSWD')

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

def get_summary(text)->None:
    """Descarga el sumario de operaciones de petroecuador

    Args:
        text (_str_): Promt indicando la descarga
    """
   
    link = get_petro_link()
    data = requests.get(link).content
    with open('docs/sumario.pdf','wb') as file:
        file.write(data)

def month_name():
    datetime_object = datetime.datetime.strptime(str(date.today().month), "%m")
    full_month_name = datetime_object.strftime("%B")
    return full_month_name
    
def upload_to_sharepoint(text):
    # search for .env or secret variables store on host service
    
    
    # Setting the name of the file 
    file_name = "0" + str(date.today().day-1)+ "-" + "0" + str(date.today().day) + '_' + "Resumen" + str(date.today().year) + str(date.today().month) + '.pdf'
    path_to_file = 'docs/sumario.pdf'

    
    try: 

        SharePoint(WELLPERF_USER,PASSWD).upload_file(path_to_file, file_name,str(date.today().year)+"/"+str(date.today().month))
        logging.info('Login Existoso.')
        logging.info(f"Documento {str(date.today().year)}/{str(date.today().month)}/{file_name} subido a Sharepoint.")

        # read creds file
    except FileNotFoundError as e:
        logging.error('Proceso terminado, credenciales no validas, error: ', e)
        
    except:
        logging.error("El documento no se ha subido en Sharepoint.")



def main():
   
    schedule.every().day.at("13:27:30").do(get_summary,"")
    schedule.every().day.at("13:27:50").do(upload_to_sharepoint,"")

    # Loop
    while True:
        schedule.run_pending()
        time.sleep(1) # wait one minute
    


if __name__ == '__main__':
    main()


 
    
    
   




