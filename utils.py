from serverEmail import mail
from flask_mail import Message
from decimal import Decimal
import re
from db import *
from bs4 import BeautifulSoup
import requests
import calendar
import locale

# Cambiar la configuración regional a español
locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
import time
from datetime import datetime, timedelta
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive 




def ObtenerIDTabla(db_session, id_tabla, tabla):
    query = text(f'SELECT MAX({id_tabla}) AS id FROM {tabla}')
    result = db_session.execute(query)

    # Intentar obtener el ID
    id_obtenido = result.fetchone()[0]  # Se extrae el valor del resultado

    if id_obtenido is not None:
        # Si se encontró un ID, sumar uno al valor existente
        id_nuevo = id_obtenido + 1
    else:
        # Si no se encontró ningún ID, asignar 1 como valor inicial
        id_nuevo = 1

    return id_nuevo

    # Crea la funcion obtner_index_columna
def obtener_index_columna(cursor, nombre_columna):
    columnas = list(cursor.keys())
    index = columnas.index(nombre_columna)
    return index

    # Crea una función para retornar la cantidad de resultados de una tabla x con x estado
def contar_resultados(db_session, tabla, estado):
    query = text(f'SELECT COUNT(*) FROM {tabla} WHERE estado = :estado')
    result = db_session.execute(query, {"estado": estado})
    return result.fetchone()[0]



def obtener_tasa_cambio_oficial():

    try:

        time.sleep(5)
         # Hacer una petición GET a la página de la tasa de cambio
        page = requests.get("https://www.bcn.gob.ni/")
        soup = BeautifulSoup(page.content, 'html.parser')

        print(soup.prettify())

        # Buscar la tabla que contiene la tasa de cambio
        table = soup.find_all('table')[0]

        # Buscar la fila que contiene la tasa de cambio
        row = table.find_all('tr')[4]

        # Obtener el valor de la tasa de cambio
        tasa_cambio = row.find_all('td')[0].text

    except Exception as e:
        print(e)
        tasa_cambio = "Error"
   

    return tasa_cambio


def obtener_tasa_cambio_local():
    try:
        query = text("""SELECT 
		tcm.id_tasaCambioMoneda,
    mc.id_moneda AS id_moneda_origen,
    mc.nombreMoneda AS nombre_moneda_origen,
    mc.codigoMoneda AS codigo_moneda_origen,
    md.id_moneda AS id_moneda_destino,
    md.nombreMoneda AS nombre_moneda_destino,
    md.codigoMoneda AS codigo_moneda_destino,
    tcm.cifraTasaCambio,
    tcm.cifraTasaCambioAnterior,
    tcm.fechaModificacion
FROM 
    tasaCambioMoneda tcm
INNER JOIN 
    moneda mc ON tcm.moneda_origen = mc.id_moneda
INNER JOIN 
    moneda md ON tcm.moneda_destino = md.id_moneda;
                     """)
        result = db_session.execute(query).fetchone()

        jsonresult = {
            "id_tasaCambioMoneda": result[0],
            "id_moneda_origen": result[1],
            "nombre_moneda_origen": result[2],
            "codigo_moneda_origen": result[3],
            "id_moneda_destino": result[4],
            "nombre_moneda_destino": result[5],
            "codigo_moneda_destino": result[6],
            "cifraTasaCambio": result[7],
            "cifraTasaCambioAnterior": result[8],
            "fechaModificacion": result[9]
        }

        return jsonresult

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()

def actualizar_tasa_cambio_oficial(db_session, id_tasa_cambio, crifra_nueva, cifra_anterior):

    try:


        query= text(""" 
UPDATE tasaCambioMoneda
SET cifraTasaCambioAnterior = cifraTasaCambio,
    cifraTasaCambio = :cifra_nueva,
    fechaModificacion = NOW()
WHERE id_tasaCambioMoneda = :id_tasa_cambio;



""")
        db_session.execute(query, {"cifra_nueva": crifra_nueva, "cifra_anterior": cifra_anterior, "id_tasa_cambio": id_tasa_cambio})
        db_session.commit()
        return True

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()






def convertir_string_a_decimal(input_str):
    # Encontrar el índice del primer carácter numérico
    indice_inicio = next((i for i, c in enumerate(input_str) if c.isdigit()), None)
    
    # Eliminar cualquier carácter no numérico antes del índice del primer carácter numérico
    input_str = input_str[indice_inicio:]
    
    # Eliminar comas del string
    input_str = input_str.replace(',', '')
    
    # Convertir a decimal
    decimal_value = float(input_str)
    
    return decimal_value


def obtener_quincenaActual_letras(date):
    # Si la entrada es una cadena, convertirla a datetime
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")

    # Obtener el mes y el año de la fecha
    mes = calendar.month_name[date.month]
    anio = date.year

    # Obtener la quincena actual
    if date.day <= 15:
        quincena = "Primera"
    else:
        quincena = "Segunda"

    # Retornar la quincena, el mes y el año como una tupla
    return quincena, mes, anio

def obtener_fechaIncioYFin_con_año(año):
    # Verificar si el año es un entero
    if isinstance(año, int):
        # Crear un objeto datetime con el año
        año = datetime(año, 1, 1)
    elif isinstance(año, str):
        # Si la entrada es una cadena, convertirla a datetime
        año = datetime.strptime(año, "%Y")
    else:
        # Si el tipo de dato no es ni int ni str, mostrar un mensaje de error
        raise ValueError("El año debe ser un entero o una cadena en formato 'YYYY'.")

    # Obtener la fecha de inicio y fin del año
    fecha_inicio = datetime(año.year, 1, 1)
    fecha_fin = datetime(año.year, 12, 31)

    return fecha_inicio, fecha_fin


def sumar_dias(fecha_inicio, dias_a_sumar):
    # Convertir la fecha de inicio a un objeto datetime
    fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d')

    # Sumar los días especificados
    fecha_fin_obj = fecha_inicio_obj + timedelta(days=dias_a_sumar)

    # Convertir la fecha resultante a una cadena en el formato deseado
    fecha_fin_totalSaldo = fecha_fin_obj.strftime('%Y-%m-%d')

    return fecha_fin_totalSaldo


# Función genérica para enviar un correo
def enviar_correo(destinatario, asunto, cuerpo):
    mensaje = Message(asunto, recipients=[destinatario])
    mensaje.body = cuerpo
    mail.send(mensaje)





def get_or_create_folder_id(drive, folder_path):
    folder_names = folder_path.split('/')
    parent_id = 'root'
    for folder_name in folder_names:
        query = f"'{parent_id}' in parents and title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        file_list = drive.ListFile({'q': query}).GetList()
        if file_list:
            folder_id = file_list[0]['id']
        else:
            # Create the folder if it doesn't exist
            folder_metadata = {
                'title': folder_name,
                'parents': [{'id': parent_id}],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = drive.CreateFile(folder_metadata)
            folder.Upload()
            folder_id = folder['id']
        parent_id = folder_id
    return parent_id



def auth_to_drive():
    gauth = GoogleAuth()

    # Configura el tipo de acceso en 'offline' para obtener un refresh_token
    gauth.DEFAULT_SETTINGS['oauth_scope'] = ['https://www.googleapis.com/auth/drive.file']
    gauth.DEFAULT_SETTINGS['access_type'] = 'offline'
    gauth.DEFAULT_SETTINGS['include_granted_scopes'] = 'true'

    # Intenta cargar las credenciales de autenticación de un archivo
    try:
        gauth.LoadCredentialsFile("mycreds.txt")
    except Exception as e:
        print("No se pudo cargar el archivo de credenciales. Iniciando autenticación...")

    # Si el archivo no existe o no contiene credenciales válidas, inicia el flujo de autenticación
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        try:
            gauth.Refresh()
        except Exception as e:
            print("No se pudo refrescar el token. Iniciando autenticación...")
            gauth.LocalWebserverAuth()
    else:
        gauth.Authorize()

    # Guarda las credenciales para la próxima ejecución
    gauth.SaveCredentialsFile("mycreds.txt")

    # Retorna una instancia de GoogleDrive autenticada
    return GoogleDrive(gauth)

def upload_to_drive(drive, filepath, folder_id):
    # Extrae solo el nombre del archivo del camino completo
    filename = os.path.basename(filepath)

    # Crea y sube un archivo de texto.
    backup_file = drive.CreateFile({'title': filename, 'parents': [{'id': folder_id}]})
    backup_file.SetContentFile(filepath)
    backup_file.Upload()
    print('El archivo de respaldo ha sido subido con éxito.')
   