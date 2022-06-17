# TODO Herramienta para analizar el texto de un pdf
# TODO Trigger o codigo que se ejecute permanentemente y a cierta hora realize algo

import schedule
import time
import requests
import PyPDF2
import os
from bs4 import BeautifulSoup
from pdf_mail import sendpdf
from sharepoint import SharePoint
from datetime import date
import datetime



def get_petro_link():
    link = "https://www.eppetroecuador.ec/?p=3721" 
    data = requests.get(link).content
    soup = BeautifulSoup(data, "html.parser")
    foo = soup.find('a',string = 'Sumario de Operaciones').get('href')
    return foo 

def get_summary(text:str)->None:
    """Descarga el sumario de operaciones de petroecuador

    Args:
        text (_str_): Promt indicando la descarga
    """
   
    link = get_petro_link()
    print(link)
    data = requests.get(link).content
    print(text)
    with open('docs/sumario.pdf','wb') as file:
        file.write(data)


def month_name():
    datetime_object = datetime.datetime.strptime(str(date.today().month), "%m")
    full_month_name = datetime_object.strftime("%B")
    return full_month_name
    

def upload_to_sharepoint(status):
    # Setting the name of the file 
    file_name = "0" + str(date.today().day-1)+ "-" + "0" + str(date.today().day) + '_' + "Resumen" + str(date.today().year) + str(date.today().month) + '.pdf'
    path_to_file = 'docs/sumario.pdf'
    SharePoint().upload_file(path_to_file, file_name,str(date.today().year)+"/"+str(date.today().month))
    print("Document in this sharepoint location: " + month_name() + '/' + file_name)



def main():
    schedule.every().day.at("10:30").do(get_summary,'Sumario descargado')
    schedule.every().day.at("10:31").do(upload_to_sharepoint,'Documento en Sharepoint')

    # Loop
    while True:
        schedule.run_pending()
        time.sleep(1) # wait one minute

    

if __name__ == '__main__':
   main()
   




