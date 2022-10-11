import logging 
logging.basicConfig(filename="log.txt", level = logging.DEBUG,
                        format="%(asctime)s %(message)s")
import requests
import datetime
import bs4 as bs
import os
import json
from sharepoint import SharePoint
from datetime import date
from shareplum import Office365

# for the creations of creds file
credentials = {}

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



def set_credentials(usr,passwd):
    try:
        

        if (os.path.exists('creds.json')):
            logging.info("Creds.json already created.")
            creds_path = '/'.join([ROOT_DIR, 'creds.json'])

            # read creds file
            with open(creds_path) as creds_file:
                creds = json.load(creds_file)
               
            
            Office365(SHAREPOINT_URL,creds['user'], creds['password']).get_cookies()

        else:
            Office365(SHAREPOINT_URL,usr,passwd).get_cookies()

            creds_dictionary = {
                "user": usr ,
                "password": passwd
            }
            json_object = json.dumps(creds_dictionary, indent=2)
            with open("creds.json", "w") as outfile:
                outfile.write(json_object)
                logging.info('Creds.json creado correctamente.')

            creds_path = '/'.join([ROOT_DIR, 'creds.json'])

            # read creds file
            with open(creds_path) as creds_file:
                creds = json.load(creds_file)
               
            
            
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
        creds_path = '/'.join([ROOT_DIR, 'creds.json'])
        with open(creds_path) as creds_file:
            creds = json.load(creds_file)
        SharePoint(creds['user'],creds['password']).upload_file(path_to_file, file_name,str(date.today().year)+"/"+str(date.today().month))
        logging.info(f"Documento {str(date.today().year)}/{str(date.today().month)}/{file_name} subido a Sharepoint.")

        # read creds file
    except FileNotFoundError as e:
        logging.error('Proceso terminado, credenciales no validas, error: ', e)
        
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


    if(os.path.exists('creds.json')):
        creds_path = '/'.join([ROOT_DIR, 'creds.json'])
        with open(creds_path) as creds_file:
            creds = json.load(creds_file)

        set_credentials(creds['user'],creds['password'])
        get_summary()
        upload_to_sharepoint()
    else:
        user = input('Ingresa correo wellperf: ')
        password = input('Contrasenia: ')
        set_credentials(user,password)
        get_summary()
        upload_to_sharepoint()
    

 
    
    
   




