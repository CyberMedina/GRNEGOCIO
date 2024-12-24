from serverEmail import mail
from flask_mail import Message
from decimal import Decimal
import re
from app import *
from db import *
from bs4 import BeautifulSoup
import requests
import calendar
import locale
import pytz
import dropbox
import base64

# Establecer el locale a español para formatear los nombres de días y meses
locale.setlocale(locale.LC_TIME, 'es_ES')

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
import time
from datetime import datetime, timedelta
import datetime
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive 
from functools import wraps
from flask import session, redirect, url_for

from dotenv import load_dotenv

load_dotenv()


def login_requiredUser(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login_system')
        return f(*args, **kwargs)
    return decorated_function


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
    tasacambiomoneda tcm
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
UPDATE tasacambiomoneda
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
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

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

def obtener_quincenaActualStr(date):
        # Si la entrada es una cadena, convertirla a datetime
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

    # Obtener el mes y el año de la fecha
    mes = calendar.month_name[date.month]
    anio = date.year

    # Obtener la quincena actual
    if date.day <= 15:
        quincena = "Primera"
    else:
        quincena = "Segunda"

    quincena_actual_Str = f"{quincena} Quincena de {mes} del {anio} del día {date.day} de {mes} del {anio}"

    return quincena_actual_Str


def obtener_fechaIncioYFin_con_año(año):
    # Verificar si el año es un entero
    if isinstance(año, int):
        # Crear un objeto datetime con el año
        año = datetime.datetime(año, 1, 1)
    elif isinstance(año, str):
        # Si la entrada es una cadena, convertirla a datetime
        año = datetime.datetime.strptime(año, "%Y")
    else:
        # Si el tipo de dato no es ni int ni str, mostrar un mensaje de error
        raise ValueError("El año debe ser un entero o una cadena en formato 'YYYY'.")

    # Obtener la fecha de inicio y fin del año
    fecha_inicio = datetime.datetime(año.year, 1, 1)
    fecha_fin = datetime.datetime(año.year, 12, 31)

    return fecha_inicio, fecha_fin


def sumar_dias(fecha_inicio, dias_a_sumar):
    # Convertir la fecha de inicio a un objeto datetime
    fecha_inicio_obj = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')

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


# Configura tu token de acceso





def get_latest_sql_file(dbx, folder_path):
    # Listar todos los archivos en la carpeta
    response = dbx.files_list_folder(folder_path)
    file_list = response.entries
    
    # Filtrar solo archivos .sql
    sql_files = [file for file in file_list if file.name.endswith('.sql')]
    
    # Ordenar los archivos por fecha de modificación (más reciente primero)
    sql_files.sort(key=lambda x: x.client_modified, reverse=True)
    
    # Retornar el archivo más reciente, si existe
    if sql_files:
        return sql_files[0]
    else:
        return None

def get_all_sql_files(dbx, folder_path):
    # Listar todos los archivos en la carpeta
    response = dbx.files_list_folder(folder_path)
    file_list = response.entries
    
    # Filtrar solo archivos .sql
    sql_files = [file for file in file_list if file.name.endswith('.sql')]
    
    # Ordenar los archivos por fecha de modificación (más reciente primero)
    sql_files.sort(key=lambda x: x.client_modified, reverse=True)
    
    return sql_files if sql_files else None

# def convertir_fecha(fecha_str):
#     # Parsear la fecha y hora original
#     fecha_utc = datetime.datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%S.%fZ')
#     # Convertir a zona horaria local o a una específica
#     fecha_local = fecha_utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('America/Mexico_City'))
#     # Ajustar manualmente la hora si es necesario
#     # Formatear la fecha y hora al formato deseado
#     fecha_formateada = fecha_local.strftime('%A %d de %B de %Y a las %I:%M:%S %p')
#     return fecha_formateada.replace('AM', 'a.m.').replace('PM', 'p.m.')


# Asegúrate de que el locale esté configurado a español


def convertir_fecha(fecha, zona_horaria_local='America/Managua'):
    """Convierte la fecha del servidor a la hora local en un formato más legible"""
    # Zona horaria del servidor (asumido como UTC)
    server_timezone = pytz.utc
    
    # Zona horaria local
    local_timezone = pytz.timezone(zona_horaria_local)
    
    # Localizar la fecha del servidor
    server_time_with_tz = server_timezone.localize(fecha)
    
    # Convertir a la zona horaria local
    local_time = server_time_with_tz.astimezone(local_timezone)
    
    # Formatear la fecha y hora en el formato deseado sin AM/PM
    fecha_formateada = local_time.strftime("%A %d de %B de %Y a las %I:%M:%S")
    
    # Capitalizar el primer carácter de la cadena formateada para una mejor presentación
    fecha_formateada = fecha_formateada.capitalize()
    
    # Añadir manualmente el formato de AM/PM en español
    hora = local_time.hour
    if hora < 12:
        am_pm = "am"
    else:
        am_pm = "pm"
    
    # Agregar AM/PM a la fecha formateada
    fecha_formateada += f" {am_pm}"
    
    return fecha_formateada

# Función para subir archivo a Dropbox
def upload_to_dropbox(dbx, file, dropbox_destination_path):
    """Sube el archivo a Dropbox."""
    try:
        file.seek(0)  # Asegurarse de que el puntero de lectura del archivo esté al inicio
        dbx.files_upload(file.read().encode('utf-8'), dropbox_destination_path)
        return True, None
    except Exception as e:
        return False, str(e)



def obtener_enlace_descarga(dbx, file_path):
    """Genera un enlace de descarga para el archivo de Dropbox, reutilizando el existente si ya existe"""
    try:
        # Verificar si ya existe un enlace compartido
        shared_links = dbx.sharing_list_shared_links(path=file_path, direct_only=True).links
        if shared_links:
            shared_link_metadata = shared_links[0]
        else:
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(file_path)
        
        return shared_link_metadata.url.replace("?dl=0", "?dl=1")
    except dropbox.exceptions.ApiError as e:
        print(f"Error creating or retrieving shared link: {e}")
        return None
    
def obtener_str_fecha_hora():
    """Obtiene la fecha y hora actual en formato de cadena"""
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def enviar_texto_whatsapp(number, textMessage):
    url = f"{os.getenv('URL_SERVER_EVOLUTION_API')}/message/sendText/{os.getenv('EVOLUTION_API_INSTANCE')}"

    payload = {
        "number": number,
        "text": textMessage,
        "delay": 1
    }
    headers = {
        "apikey": os.getenv("EVOLUTION_API_KEY"),
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)





def enviar_media_whatsapp(number, fileName, textMessage, mediatype, media):


    url = f"{os.getenv('URL_SERVER_EVOLUTION_API')}/message/sendMedia/{os.getenv('EVOLUTION_API_INSTANCE')}"

    media_base64 = base64.b64encode(media).decode('utf-8')

    payload = {
        "number": number,
        "mediatype": mediatype,
        "mimetype": "application/pdf",
        "caption": textMessage,
        "media": media_base64,
        "fileName": fileName,
        "delay": 7,
    }
    headers = {
        "apikey": os.getenv("EVOLUTION_API_KEY"),
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

def obtener_dia_actual():
    managua_tz = pytz.timezone('America/Managua')
    current_time = datetime.datetime.now(managua_tz)
    hour = current_time.hour

    if 5 <= hour < 12:
        greeting = "¡Buenos días"
    elif 12 <= hour < 18:
        greeting = "¡Buenas tardes"
    else:
        greeting = "¡Buenas noches"

    return greeting


