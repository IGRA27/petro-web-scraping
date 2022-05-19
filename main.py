# TODO Herramienta para analizar el texto de un pdf
# TODO Trigger o codigo que se ejecute permanentemente y a cierta hora realize algo

import schedule
import time
import requests
import PyPDF2
import os
from pdf_mail import sendpdf
from sharepoint import SharePoint


def get_sumary(text:str)->None:
    """Descarga el sumario de operaciones de petroecuador

    Args:
        text (_str_): Promt indicando la descarga
    """
    link = 'https://www.eppetroecuador.ec/wp-content/uploads/downloads/2022/05/PRD-PEC-RPR-SUMARIO-OPERACIONES.pdf'
    data = requests.get(link).content
    print(text)
    with open('docs/sumario.pdf','wb') as file:
        file.write(data)
    upload_to_sharepoint()
    
        

def update_name():
    pdfObj = open('docs/sumario.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfObj)
    pdfPage = pdfReader.getPage(0)
    text = pdfPage.extractText()
    date_index = text.find('Fecha de Impresión:')
    text_date = text[date_index+20:65]

    month = text_date[0:3]
    day = text_date[4:6]
    year = text_date[8:12]
    hour = text_date[18]
    
    time_set = text_date[26:28]

    time_stamped = month+'-'+day+'-'+year+'-'+hour+time_set
    print(time_stamped)

    formatted_command = 'mv docs/sumario.pdf ' + ' docs/'+time_stamped + '.pdf'
    os.system(formatted_command)
    

def get_name():
    pdfObj = open('docs/sumario.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfObj)
    pdfPage = pdfReader.getPage(0)
    text = pdfPage.extractText()
    date_index = text.find('Fecha de Impresión:')
    text_date = text[date_index+20:65]

    month = text_date[0:3]
    day = text_date[4:6]
    year = text_date[8:12]
    hour = text_date[18]
    
    time_set = text_date[26:28]

    time_stamped = month+'-'+day+'-'+year+'-'+hour+time_set
    print(time_stamped)

   # formatted_command = 'mv docs/sumario.pdf ' + ' docs/'+time_stamped + '.pdf'
    return time_stamped   


def upload_to_sharepoint():
    pdfObj = open('docs/sumario.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfObj)
    pdfPage = pdfReader.getPage(0)
    text = pdfPage.extractText()
    date_index = text.find('Fecha de Impresión:')
    text_date = text[date_index+20:65]

    month = text_date[0:3]
    day = text_date[4:6]
    year = text_date[8:12]
    hour = text_date[18]
    
    time_set = text_date[26:28]

    time_stamped = month+'-'+day+'-'+year+'-'+hour+time_set

    path_to_file = 'docs/sumario.pdf'
    print('Subiendo a sharepoing..')
    SharePoint().upload_file(path_to_file, time_stamped+'.pdf','Sumario_PetroEcuador')
    print('Subido a Sharepoint con exito')

def main():
    schedule.every().day.at("07:00").do(get_sumary,'Descargando documento')
    while True:
        schedule.run_pending()
        print('Im Working!')
        time.sleep(60) # wait one minute

    





