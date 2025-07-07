from serverEmail import mail
from flask_mail import Message
from decimal import Decimal
import re
import pytz
from app import *
from database_connection import *
import requests
import calendar
import locale
import dropbox
import base64


# Establecer el locale a español para formatear los nombres de días y meses
locale.setlocale(locale.LC_TIME, 'es_ES')

import time
import random
import time
from datetime import datetime, timedelta
import datetime
from functools import wraps
from flask import session, redirect, url_for
import cloudinary
# Configure Cloudinary credentials
# (You can also store these in environment variables for security)
cloudinary.config(
    cloud_name= os.getenv('CLOUD_NAME'),
    api_key= os.getenv('API_KEY'),
    api_secret= os.getenv('API_SECRET'),
    secure=True
)

# Configurar el proxy para Cloudinary si existe en las variables de entorno
proxy = os.getenv('API_PROXY')
if proxy:
    cloudinary.config(
        api_proxy = proxy
    )
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import private_download_url

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


def get_most_recent_sql_file(dbx, folder_path):
    """
    Retorna el archivo SQL más reciente de una carpeta en Dropbox.
    
    Args:
        dbx: Instancia de Dropbox
        folder_path: Ruta de la carpeta a buscar
        
    Returns:
        El archivo SQL más reciente o None si no hay archivos SQL
    """
    try:
        # Listar todos los archivos en la carpeta
        response = dbx.files_list_folder(folder_path)
        
        # Filtrar y obtener el archivo SQL más reciente
        sql_files = [file for file in response.entries if file.name.lower().endswith('.sql')]
        if not sql_files:
            return None
            
        return max(sql_files, key=lambda x: x.client_modified)
        
    except Exception as e:
        print(f"Error al obtener el archivo SQL más reciente: {e}")
        return None


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
    """Sube el archivo a Dropbox y devuelve el enlace compartido."""
    try:
        file.seek(0)  # Asegurarse de que el puntero de lectura del archivo esté al inicio
        dbx.files_upload(file.read().encode('utf-8'), dropbox_destination_path)
        
        # Crear y obtener el enlace compartido
        shared_link = dbx.sharing_create_shared_link(dropbox_destination_path)
        download_url = shared_link.url.replace('?dl=0', '?dl=1')  # Convertir a enlace de descarga directa
        
        return True, None, download_url
    except Exception as e:
        return False, str(e), None



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



def subirImagen(db_session, url, public_id, proveedorImagen, estado):
    try:
        # Obtener el ID de la tabla persona
        id_imagen = (ObtenerIDTabla(
                db_session, "id_imagen", "imagenes"))

        query = text("""INSERT INTO imagenes (id_imagen, id_proveedorImagen, url_imagen, public_id, fechaHoraCreacion, estado)
VALUES (:id_imagen, :id_proveedorImagen, :url_imagen, :public_id, NOW(), :estado);""")
        db_session.execute(query, {"id_imagen": id_imagen,
                                    "id_proveedorImagen": proveedorImagen,
                                    "url_imagen": url,
                                    "public_id": public_id,
                                    "estado": estado})
        return id_imagen
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        raise




def actualizar_imagen(db_session, id_imagen, url, public_id):
    """
    Actualiza los datos de una imagen existente en la base de datos.
    
    Args:
        db_session: Sesión de la base de datos
        id_imagen: ID de la imagen a actualizar
        url: URL segura de Cloudinary
        public_id: ID público de Cloudinary
    """
    try:
        query = text("""
            UPDATE imagenes 
            SET url_imagen = :url_imagen,
                public_id = :public_id,
                fechaHoraModificacion = NOW()
            WHERE id_imagen = :id_imagen
        """)
        
        db_session.execute(query, {
            "id_imagen": id_imagen,
            "url_imagen": url,
            "public_id": public_id
        })
        
    except SQLAlchemyError as e:
        print(f"Error al actualizar la imagen: {e}")
        raise



def eliminar_imagen(db_session, id_imagen):
    """
    Elimina una imagen de Cloudinary y actualiza su estado en la base de datos.
    
    Args:
        db_session: Sesión de la base de datos
        id_imagen: ID de la imagen a eliminar
    
    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario
    """
    try:
        # Primero obtener el public_id de la imagen
        query = text("SELECT public_id FROM imagenes WHERE id_imagen = :id_imagen")
        result = db_session.execute(query, {"id_imagen": id_imagen}).fetchone()
        
        if not result:
            return False
            
        public_id = result[0]
        
        # Eliminar la imagen de Cloudinary
        cloudinary.uploader.destroy(public_id, resource_type='image', type='authenticated')
        
        # Actualizar el estado de la imagen en la base de datos
        query = text("""
            DELETE FROM imagenes WHERE id_imagen = :id_imagen;
        """)
        
        db_session.execute(query, {"id_imagen": id_imagen})
        
        return True
        
    except cloudinary.exceptions.Error as e:
        print(f"Error de Cloudinary: {e}")
        db_session.rollback()
        return False
    except SQLAlchemyError as e:
        print(f"Error de base de datos: {e}")
        db_session.rollback()
        return False





def obtener_url_temporal_cloudinary(public_id, file_format='jpg'):
    """
    Generate a time-limited, signed URL for an authenticated resource in Cloudinary.
    
    :param public_id: The public ID of the uploaded asset.
    :param file_format: The file format/extension for the output (e.g., jpg, png).
    :return: A signed URL that can be used to access the authenticated asset.
    """
    # resource_type defaults to 'image', but can be adjusted (e.g., 'video') if needed.
    resource_type = 'image'
    url = private_download_url(
        public_id=public_id,
        format=file_format,
        resource_type=resource_type,
        type='authenticated',
        # sign_url is True by default in private_download_url, but we can explicitly set it:
        sign_url=True
    )
    return url

def convertir_monto_a_string(monto):
    # Convierte el mont a un string en el siguiente formato C$ 1,000.00
    return f"C${monto:,.2f}"

def convertir_fecha_a_string(fecha):
    # Convierte la fecha a un string en el siguiente formato 14 de enero de 2025
    return fecha.strftime("%d de %B de %Y")

def convertir_fecha_a_string_con_hora(fecha):
    # Primero formateamos la fecha en español
    fecha_base = fecha.strftime("%d de %B de %Y a las %I:%M:%S")
    
    # Añadimos AM/PM manualmente basado en la hora
    hora = fecha.hour
    periodo = "Am" if hora < 12 else "Pm"
    
    fecha_formateada = f"{fecha_base} {periodo}"
    return fecha_formateada

