from logging import getLogger
import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, session, url_for, redirect, Response, send_file
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
from io import BytesIO
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import scoped_session, sessionmaker
from num2words import num2words
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS, cross_origin
from datetime import datetime
from babel.dates import format_date
from urllib.parse import urlencode
from decimal import Decimal
import tempfile
import weasyprint
import smtplib
import subprocess
import glob
import io



# Importando desde archivos locales
from db import *
from utils import *
from models.clientes import *
from models.constantes import *
from models.prestamos import *
from models.pagos import *
from models.contratos import *
from models.API_Alexa import *
from models.base_de_datos import *
from flask_cors import CORS
from serverEmail import mail

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"
CORS(app)

# Si no hay un número seleccionado en sesión, simplemente se asigna 1



# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

mail.init_app(app)




def initialize_session_variable(key, default_value):
    if key not in session:
        session[key] = default_value


@app.before_request
def before_request():
    initialize_session_variable("numero_seleccionado_ordenar_clientes", '1')
    initialize_session_variable("numero_seleccionado_ordenar_prestamos", '5')
    initialize_session_variable(
        "numero_seleccionado_ordenar_clientesPrestamos", '0')
    initialize_session_variable("año_seleccionado", datetime.now().year)


@app.route('/obtener_tasa_cambio', methods=["GET", "POST"])
def obtener_tasa_cambio():

    tasa_cambio = obtener_tasa_cambio_local()

    return jsonify({"tasa_cambio": tasa_cambio})


logger = getLogger(__name__)



@app.route('/login_system', methods=['GET', 'POST'])
def login_system():

    if request.method == 'POST':

        usuario = request.form['usuario']
        password = request.form['password']

        queryLogin = text("SELECT * FROM usuarios WHERE (usuario = :usuario) LIMIT 1")
        user_row = db_session.execute(queryLogin, {"usuario":usuario}).fetchone()

        if user_row:
            user_password = user_row[5]
            user_id = user_row[0]
        
            if check_password_hash(user_password, password):
                session['user_id'] = user_id
                return render_template('index.html')
        return render_template('auth/login.html', error="Usuario o contraseña incorrectos")

    return render_template('auth/login.html')

@cross_origin()
@app.route('/actualizar_tasa_cambio', methods=['POST'])
def actualizar_tasa_cambio():
    try:
        data = request.get_json()
        cifra_nueva = float(data.get("tasa_cambio"))

        if not isinstance(cifra_nueva, (int, float)):
            return jsonify({"status": "cifra_nueva debe ser un número"}), 400

        tabla_tasa_cambio = obtener_tasa_cambio_local()
        id_tasa_cambio = tabla_tasa_cambio["id_tasaCambioMoneda"]
        cifra_actual = tabla_tasa_cambio["cifraTasaCambio"]

        actualizar_tasa_cambio_oficial(
            db_session, id_tasa_cambio, cifra_nueva, cifra_actual)
    except SQLAlchemyError as e:
        db_session.rollback()
        return jsonify({"status": "Error en la base de datos"}), 500
    finally:
        db_session.close()

    return jsonify({"status": "success"}), 200


@app.route('/')
@login_requiredUser
def index():


    return render_template('index.html')

######## Rutas para guardar en sesión el número seleccionado en diferentes templates ########
##### Clientes#########


@app.route("/guardar_en_sesion_ordenar_clientes", methods=["POST"])
def guardar_en_sesion_ordenar_clientes():
    data = request.get_json()  # Obtener datos enviados desde el frontend
    selected_value = data.get("selectedValue")

    # Guardar el valor en la sesión
    session["numero_seleccionado_ordenar_clientes"] = selected_value

    return jsonify({"message": "Número guardado en sesión correctamente"})


@app.route("/guardar_año_seleccionado", methods=["POST"])
def guardar_año_seleccionado():
    data = request.get_json()
    selected_value = int(data.get("selectedValue"))

    session["año_seleccionado"] = selected_value

    return jsonify({"message": "Año guardado en sesión correctamente"})


@app.route("/convertir_numeros_a_letras", methods=["POST"])
def convertir_numeros_a_letras():
    data = request.get_json()
    monto = data.get("monto")
    monto_letras = num2words(monto, lang='es')
    return jsonify({"monto_letras": monto_letras})


@app.route("/convertir_fechas_a_letras", methods=["POST"])
def convertir_fechas_a_letras():
    data = request.get_json()
    fecha_str = data.get("fecha")  # Obtener la fecha como cadena de texto

    # Convertir la cadena de texto a un objeto de fecha
    # Suponiendo que la cadena de texto está en formato 'YYYY-MM-DD'
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")

    dia = num2words(fecha.day, lang='es')
    mes = format_date(fecha, format='MMMM', locale='es_ES')
    año = num2words(fecha.year, lang='es')

    texto_fecha = f"a los {dia} días del mes de {mes} del año {año}"

    return jsonify({"fecha_letras": texto_fecha})


##### Prestamos ########
@app.route("/guardar_en_sesion_ordenar_prestamos", methods=["POST"])
def guardar_en_sesion_ordenar_prestamos():
    data = request.get_json()  # Obtener datos enviados desde el frontend
    selected_value = data.get("selectedValue")

    # Guardar el valor en la sesión
    session["numero_seleccionado_ordenar_prestamos"] = selected_value

    return jsonify({"message": "Número guardado en sesión correctamente"})


###### Pagos #########
@app.route("/guardar_en_sesion_ordenar_clientesPrestamos", methods=["POST"])
def guardar_en_sesion_ordenar_clientesPrestamos():
    data = request.get_json()
    selected_value = data.get("selectedValue")

    session["numero_seleccionado_ordenar_clientesPrestamos"] = selected_value

    return jsonify({"message": "Número guardado en sesión correctamente"})

########### Empieza el modulo de clientes ###########


@app.route('/clientes', methods=['GET', 'POST'])
@login_requiredUser
def clientes():

    # Obtenemos la lista de clientes cruda sin procesar

    cursor = listar_clientes(
        db_session, [session.get("numero_seleccionado_ordenar_clientes")])
    cantidad_clientes = contar_resultados(
        db_session, "cliente", [session.get("numero_seleccionado_ordenar_clientes")])

    # Procesamos la lista de clientes para mostrarla en el formulario
    formulario_clientes = {
        "companias_telefonicas": obtener_companias_telefonicas(db_session),
        "listar_clientes_data": cursor.fetchall(),
        "listar_clientes_columns": cursor.keys(),
        "cantidad_clientes": cantidad_clientes,
        "index_estado": obtener_index_columna(cursor, "Estado"),
        "index_id": obtener_index_columna(cursor, "id_cliente")
    }

    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['cedula']
        fechaNac = request.form['fechaNac']
        genero = request.form['genero']
        direccion = request.form['direccion']
        direccionMaps = request.form['direccionMaps']
        nombreDireccion = request.form['nombreDireccion']
        idCompaniTelefonica = request.form['idCompaniTelefonica']
        telefono = request.form['telefono']
        nombreTelefono = request.form['nombreTelefono']
        fotoCliente = request.files['fotoCliente']
        foto_cedula = request.files['foto_cedula']

        db_session.begin()

        try:
            id_persona = insertar_persona(
                db_session, nombres, apellidos, genero, cedula, fechaNac, activo)
            id_direccion = insertar_direccion(
                db_session, nombreDireccion, direccion, direccionMaps, activo)
            id_telefono = insertar_telefono(
                db_session, idCompaniTelefonica, nombreTelefono, telefono, activo)
            id_persona_direccion = insertar_persona_direccion(
                db_session, id_persona, id_direccion, activo)
            id_direccion_telefono = insertar_direccion_telelfono(
                db_session, id_direccion, id_telefono, activo)
            id_insertar_cliente = insertar_cliente(
                db_session, id_persona, cliente_en_proceso, fotoCliente, foto_cedula, cliente_en_proceso)

            db_session.commit()

        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {str(e)}")
            return render_template('clientes/clientes.html', **formulario_clientes, error="Error en la base de datos")

        except Exception as e:
            db_session.rollback()
            print(f"Unexpected error: {str(e)}")
            return render_template('error.html', error="Unexpected error occurred"), 500

        finally:
            db_session.close()

        return redirect(url_for('clientes'))

    return render_template('clientes/clientes.html', **formulario_clientes)


@app.route('/datos_cliente', methods=['GET', 'POST'])
@login_requiredUser
def datos_cliente():
    return render_template('datos_cliente.html')


########### Empieza el modulo de prestamos ###########
@app.route('/prestamos', methods=['GET', 'POST'])
@login_requiredUser
def prestamos():

    # Obtenemos la lista de clientes cruda sin procesar

    cursor = listar_prestamos(
        db_session, [session.get("numero_seleccionado_ordenar_prestamos")])
    cantidad_clientes = contar_resultados(
        db_session, "cliente", [session.get("numero_seleccionado_ordenar_prestamos")])

    # Procesamos la lista de clientes para mostrarla en el formulario
    formulario_clientes = {
        "companias_telefonicas": obtener_companias_telefonicas(db_session),
        "listar_clientes_data": cursor.fetchall(),
        "listar_clientes_columns": cursor.keys(),
        "cantidad_clientes": cantidad_clientes,
        "index_estado": obtener_index_columna(cursor, "Estado"),
        "index_id": obtener_index_columna(cursor, "id_cliente")
    }

    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['cedula']
        fechaNac = request.form['fechaNac']
        genero = request.form['genero']
        direccion = request.form['direccion']
        direccionMaps = request.form['direccionMaps']
        nombreDireccion = request.form['nombreDireccion']
        idCompaniTelefonica = request.form['idCompaniTelefonica']
        telefono = request.form['telefono']
        nombreTelefono = request.form['nombreTelefono']
        fotoCliente = request.files['fotoCliente']
        foto_cedula = request.files['foto_cedula']

        db_session.begin()

        try:
            id_persona = insertar_persona(
                db_session, nombres, apellidos, genero, cedula, fechaNac, activo)
            id_direccion = insertar_direccion(
                db_session, nombreDireccion, direccion, direccionMaps, activo)
            id_telefono = insertar_telefono(
                db_session, idCompaniTelefonica, nombreTelefono, telefono, activo)
            id_persona_direccion = insertar_persona_direccion(
                db_session, id_persona, id_direccion, activo)
            id_direccion_telefono = insertar_direccion_telelfono(
                db_session, id_direccion, id_telefono, activo)
            id_insertar_cliente = insertar_cliente(
                db_session, id_persona, cliente_en_proceso, fotoCliente, foto_cedula, inactivo)

            db_session.commit()

        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {str(e)}")
            return render_template('clientes/clientes.html', **formulario_clientes, error="Error en la base de datos")

        except Exception as e:
            db_session.rollback()
            print(f"Unexpected error: {str(e)}")
            return render_template('error.html', error="Unexpected error occurred"), 500

        finally:
            db_session.close()

    return render_template('prestamos/prestamos.html', **formulario_clientes)


@app.route('/anadir_prestamo/<int:id_cliente>', methods=['GET', 'POST'])
@login_requiredUser
def anadir_prestamo(id_cliente):

    datos_cliente = listar_datosClientes_porID(db_session, id_cliente)

    datos_formulario_anadir_prestamo = {
        "companias_telefonicas": obtener_companias_telefonicas(db_session),
        "tipos_monedas": obtener_tipos_monedas(db_session),
        "datos_cliente": datos_cliente
    }

    if request.method == 'POST':

        ## Step-1 form ###
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['cedula']
        fechaNac = request.form['fechaNac']
        genero = request.form['genero']
        direccion = request.form['direccion']
        direccionMaps = request.form['direccionMaps']
        nombreDireccion = request.form['nombreDireccion']
        idCompaniTelefonica = request.form['idCompaniTelefonica']
        telefono = request.form['telefono']
        nombreTelefono = request.form['nombreTelefono']
        fotoCliente = request.files['fotoCliente']
        foto_cedula = request.files['foto_cedula']

        ### Step-2 form ###
        estadoCivil = request.form['estadoCivil']
        nombreDelegacion = request.form['nombreDelegacion']
        dptoArea = request.form['dptoArea']
        ftoColillaINSS = request.files['fotoCopiaColillaInss']
        tipoClienteString = request.form['tipoCliente']
        tipoCliente = int(tipoClienteString)
        montoSolicitado = request.form['montoSolicitado']
        tipoMonedaMontoSolictado = request.form['tipoMonedaMontoSolicitado']
        tasaInteres = request.form['tasaInteres']
        pagoMensual = request.form['pagoMensual']
        pagoQuincenal = request.form['pagoQuincenal']
        fechaPrestamo = request.form['fechaPrestamo']
        fechaPago = request.form['fechaPago']
        # Solo para clientes especiales
        intervalo_tiempoPago = request.form['IntervaloPagoClienteEspecial']
        montoPrimerPago = request.form['montoPrimerPago']

        #### Step-3 form ####
        nombresFiador = request.form['nombresFiador']
        apellidosFiador = request.form['apellidosFiador']
        cedulaFiador = request.form['cedulaFiador']
        fechaNacFiador = request.form['fechaNacFiador']
        generoFiador = request.form['generoFiador']
        estadoCivilFiador = request.form['estadoCivilFiador']
        nombreDelegacionFiador = request.form['nombreDelegacionFiador']
        dptoAreaFiador = request.form['dptoAreaFiador']
        direccionFiador = request.form['direccionFiador']
        direccionMapsFiador = request.form['direccionMapsFiador']
        nombreDireccionFiador = request.form['nombreDireccionFiador']
        idCompaniTelefonicaFiador = request.form['idCompaniTelefonicaFiador']
        telefonoFiador = request.form['telefonoFiador']
        nombreTelefonoFiador = request.form['nombreTelefonoFiador']
        fotoFiador = request.files['fotoFiador']
        foto_cedulaFiador = request.files['foto_cedulaFiador']
        fotoCopiaColillaInssFiador = request.files['fotoCopiaColillaInssFiador']

        db_session.begin()

        try:

            ## Step-1 form ###

            #### Actualizar datos del cliente ####
            actualizar_persona(db_session, datos_cliente.id_persona, nombres, apellidos, genero,
                               cedula, fechaNac, activo)  # Actualizar datos del cliente y cambiar activo

            id_direccionYtelefono = obtenerID_direccionYtelefono(
                db_session, datos_cliente.id_persona)
            actualizar_direccion(db_session, id_direccionYtelefono.id_direccion,
                                 nombreDireccion, direccion, direccionMaps, activo)
            actualizar_telefono(db_session, id_direccionYtelefono.id_telefono,
                                idCompaniTelefonica, nombreTelefono, telefono, activo)
            actualizar_cliente(db_session, id_cliente, datos_cliente.id_persona, tipoCliente,
                               fotoCliente, foto_cedula, activo)  # Actualizar datos del cliente y cambiar activo

            #### Terminar de actualizar datos del cliente ####

            ## Step-2 form ###

            #### Insertamos al fiador ####

            # Si el checbox se encuentra en el formulario quiere decir que no hay deudor
            if 'chckbxNoDeudor' in request.form:
                id_persona = insertar_persona(
                    db_session, sin_especificar, sin_especificar, sin_especificar, sin_especificar, sin_especificar, activo)
                id_direccion = insertar_direccion(
                    db_session, sin_especificar, sin_especificar, sin_especificar, activo)
                id_telefono = insertar_telefono(
                    db_session, sin_especificar, sin_especificar, sin_especificar, activo)
                id_persona_direccion = insertar_persona_direccion(
                    db_session, sin_especificar, sin_especificar, activo)
                id_direccion_telefono = insertar_direccion_telelfono(
                    db_session, sin_especificar, sin_especificar, activo)
                id_insertar_clienteFiador = insertar_cliente(
                    db_session, id_persona, fiador, sin_especificar, sin_especificar, activo)
            else:
                id_persona = insertar_persona(
                    db_session, nombresFiador, apellidosFiador, generoFiador, cedulaFiador, fechaNacFiador, activo)
                id_direccion = insertar_direccion(
                    db_session, nombreDireccionFiador, direccionFiador, direccionMapsFiador, activo)
                id_telefono = insertar_telefono(
                    db_session, idCompaniTelefonicaFiador, nombreTelefonoFiador, telefonoFiador, activo)
                id_persona_direccion = insertar_persona_direccion(
                    db_session, id_persona, id_direccion, activo)
                id_direccion_telefono = insertar_direccion_telelfono(
                    db_session, id_direccion, id_telefono, activo)
                id_insertar_clienteFiador = insertar_cliente(
                    db_session, id_persona, fiador, fotoFiador, foto_cedulaFiador, activo)

            #### Terminamos de insertar al fiador ####

            ##### Insertamos el contrato especificamente datos del fiador #######

            # Si el checbox se encuentra en el formulario quiere decir que no hay deudor
            if 'chckbxNoDeudor' in request.form:
                # Revisar si el fiador es no deudor se recibirá un valor de 5 en el checkbox
                checkbox_no_deudor = request.form['chckbxNoDeudor']
                id_contrato_fiador = insertar_contrato_fiador(
                    db_session, id_insertar_clienteFiador, estadoCivilFiador, nombreDelegacionFiador, dptoAreaFiador, fotoCopiaColillaInssFiador, no_fiador)
            else:
                id_contrato_fiador = insertar_contrato_fiador(
                    db_session, id_insertar_clienteFiador, estadoCivilFiador, nombreDelegacionFiador, dptoAreaFiador, fotoCopiaColillaInssFiador, activo)

            if tipoCliente == cliente_normal:

                id_contrato = insertar_contrato(db_session, id_cliente, estadoCivil, nombreDelegacion, dptoArea, ftoColillaINSS,
                                                montoSolicitado, tipoMonedaMontoSolictado, tasaInteres, pagoMensual, pagoQuincenal, fechaPrestamo,
                                                fechaPago, prestamo_cliente_normal, montoPrimerPago, activo)

            elif tipoCliente == cliente_especial:

                id_contrato = insertar_contrato(db_session, id_cliente, estadoCivil, nombreDelegacion, dptoArea, ftoColillaINSS,
                                                montoSolicitado, tipoMonedaMontoSolictado, tasaInteres, pagoMensual, pagoQuincenal, fechaPrestamo,
                                                fechaPago, intervalo_tiempoPago, montoPrimerPago, activo)

            db_session.commit()

        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {str(e)}")
            return redirect(url_for('prestamos', error="Error en la base de datos"))

        except Exception as e:
            db_session.rollback()
            print(f"Unexpected error: {str(e)}")
            return render_template('error.html', error="Unexpected error occurred"), 500

        finally:
            db_session.close()

        return redirect(url_for('prestamos'))

    return render_template('prestamos/anadir_prestamo.html', **datos_formulario_anadir_prestamo)


@app.route('/datos_prestamoV1', methods=['POST'])
def datos_prestamoV1():

    data = request.get_json()
    id_cliente = data.get("id_cliente")

    datos_pago = datos_pagov1(db_session, id_cliente)


# Suponiendo que obtener_tasa_cambio_local() devuelve un diccionario directamente
    tasa_cambioJSON = obtener_tasa_cambio_local()

    # Asignar la tasa de cambio al diccionario de datos_pago
    datos_pago.append(tasa_cambioJSON)

    return jsonify({"datos_prestamo": datos_pago}), 200


@app.route('/eliminar_todo_rastro_cliente/<int:id_cliente>', methods=['POST'])
def eliminar_cliente_prestamo(id_cliente):


    db_session.begin()

    try:
        # Usar un conjunto para almacenar los IDs de clientes y evitar duplicados
        id_clientes = {id_cliente}

        # Función para convertir resultados a enteros si es necesario
        def convertir_a_entero(tupla):
            if isinstance(tupla, (list, tuple)):
                return int(tupla[0])
            return int(tupla)

        # Agregar los demás clientes que están relacionados con el cliente principal
        clientes_fiador = seleccionar_clientes_contratofiador(db_session, id_cliente)
        id_clientes.update(convertir_a_entero(cliente) for cliente in clientes_fiador if cliente is not None)

        print(id_clientes)

        for id_cliente in id_clientes:
            id_cliente = convertir_a_entero(id_cliente)  # Asegúrate de que id_cliente es un entero
            print("El id cliente es ", id_cliente)
            
            id_persona = convertir_a_entero(seleccionar_personas_por_id_cliente(db_session, id_cliente))
            id_direccion = convertir_a_entero(seleccionar_direccion_por_id_persona(db_session, id_persona))
            id_telefono = convertir_a_entero(seleccionar_id_telefono_por_idDireccion(db_session, id_direccion))

            eliminar_todos_saldos_pagos_por_idCliente(db_session, id_cliente)
            eliminar_todos_transacciones_saldos_por_idCliente(db_session, id_cliente)
            eliminar_todos_detalles_pagos_por_idCliente(db_session, id_cliente)
            eliminar_todos_pagos_por_idCliente(db_session, id_cliente)

            ### Se eliminan todos los contratos de ese cliente ###
            eliminar_todos_contratos_porIdCliente(db_session, id_cliente)
            eliminar_todos_contratos_fiador_porIdCliente(db_session, id_cliente)

            ### Se eliminan todos los clientes y fiadores de ese cliente ###
            eliminar_cliente(db_session, id_cliente)
            eliminar_direccion_telefono(db_session, id_direccion)
            eliminar_persona_direccion(db_session, id_persona)
            eliminar_telefono(db_session, id_telefono)
            eliminar_direccion(db_session, id_direccion)
            eliminar_persona(db_session, id_persona)

        db_session.commit()

        return redirect(url_for('listado_clientes_pagos'))
    except Exception as e:
        db_session.rollback()
        print(f"Error: {e}")
        return "Error"
    finally:
        db_session.close()




########### Empieza el modulo de pagos ############

@app.route('/listado_clientes_pagos', methods=['GET', 'POST'])
@login_requiredUser
def listado_clientes_pagos():




    listado_clientesPagosDict = []

    listado_clientesPagos = listar_cliesntesPagos(db_session)

    for listado in listado_clientesPagos:
        clientePagoDict = {
            "id_cliente": listado[0],
            "id_tipoCliente": listado[1],
            "nombres": listado[2],
            "apellidos": listado[3],
            "id_contrato": listado[4],
            "pagoMensual": listado[5],
            "pagoQuincenal": listado[6]
        }
        PagosEstadosCortes = obtener_estadoPagoClienteCorte(db_session, listado[0], listado[4], listado[6], listado[5], datetime.now())
        clientePagoDict.update(PagosEstadosCortes)
        listado_clientesPagosDict.append(clientePagoDict)

    # Obtenemos la lista de clientes
    print(listado_clientesPagosDict)


    formulario_clientes_pagos = {
        "listado_clientes_pagos": listado_clientesPagosDict
    }

    return render_template('pagos/listado_clientes_pagos_copy.html', **formulario_clientes_pagos)



@app.route('/verificar_tipo_saldo_insertar', methods=['POST'])
def verificar_tipo_saldo_insertar():
    try:
        id_cliente = request.form['formId_cliente']
        id_moneda = request.form['tipoMonedaPago']
        cantidadPagarDolares = request.form['cantidadPagar$']
        cantidadPagarCordobas = request.form.get('cantidadPagoCordobas')
        inputTasaCambioPago = request.form['inputTasaCambioPago']
        fechaPago = request.form['fechaPago']
        observacionPago = request.form['observacionPago']
        evidenciaPago = request.files['evidenciaPago']
        tipoPagoCompletoForm = int(request.form['tipoPagoCompleto'])

        cantidadPagarDolares = convertir_string_a_decimal(cantidadPagarDolares)
        print("La cantidad a pagar en dólares es: ", cantidadPagarDolares)

        if 'checkBoxNoPago' in request.form:
            estadoPago = no_hay_pago
        elif 'checkBoxPrimerPago' in request.form:
            estadoPago = primer_pago_del_prestamo
        else:
            estadoPago = tipoPagoCompletoForm

        print("El estado de pago es: ", estadoPago)

        response = verificar_pago(db_session, id_cliente, id_moneda, cantidadPagarDolares, estadoPago, cantidadPagarCordobas, fechaPago, tipoPagoCompletoForm)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error al procesar la solicitud"}), 500


@app.route('/procesar_pago', methods=['POST'])
def procesar_pago():

    id_cliente = request.form['formId_cliente']  # Cambié () a []
    id_moneda = request.form['tipoMonedaPago']
    cantidadPagarDolares = request.form['cantidadPagar$']
    cantidadPagarCordobas = request.form.get('cantidadPagoCordobas')
    inputTasaCambioPago = request.form['inputTasaCambioPago']
    fechaPago = request.form['fechaPago']
    observacionPago = request.form['observacionPago']
    evidenciaPago = request.files['evidenciaPago']
    tipoPagoCompletoForm = int(request.form['tipoPagoCompleto'])

    
    procesar_todo = False


    cantidadPagarDolares = convertir_string_a_decimal(cantidadPagarDolares)
    print("La cantidad a pagar en dólares es: ", cantidadPagarDolares)

    # Verifica si el checkbox de no pago está marcado
    if 'checkBoxNoPago' in request.form:
        estadoPago = no_hay_pago  # Establece el estado de pago como no pagado

    elif 'checkBoxPrimerPago' in request.form:
        # Establece el estado de pago como primer pago
        estadoPago = primer_pago_del_prestamo
    else:
        estadoPago = tipoPagoCompletoForm  # Utiliza el estado de pago completo
    
    print('checkbox_confirmacion' in request.form)

    if 'checkbox_confirmacion' in request.form:
        procesar_todo =  True

    response = proceder_pago(db_session, procesar_todo, id_cliente, id_moneda, cantidadPagarDolares, estadoPago, cantidadPagarCordobas, 
                fechaPago, tipoPagoCompletoForm, observacionPago, evidenciaPago, inputTasaCambioPago, 
                monedaConversion)
    return response
        




@app.route('/añadir_pago/<int:id_cliente>', methods=['GET', 'POST'])
@login_requiredUser
def añadir_pago(id_cliente):

    if request.method == 'POST':
        pass

        

    id_contrato = obtener_IdContrato(db_session, id_cliente)

    num_pagos = comprobar_primerPago(db_session, id_contrato)

    pagos_cliente = datos_pagov2(id_cliente, db_session)



    # saldo_pendiente = validar_saldo_pendiente_en_contra(db_session, id_cliente)
    # Definimos la cifra pago especial
    monto_pagoEspecial = 0.00

    fecha_actual = datetime.now()

    monto_pagoEspecial = obtener_pagoEspecial(
        db_session, id_cliente, fecha_actual)

    # Procesos para las sesiones de los filtros de los pagos
    años_pagos = obtener_años_pagos(db_session, id_cliente, activo)

    pagos = []

    if años_pagos:
        # Convertir los elementos de años_pagos a enteros
        años_pagos_verificar = [int(año[0]) for año in años_pagos]

        # Luego validamos si está en sesión el año de los pagos de ese contrato
        if session["año_seleccionado"] in años_pagos_verificar:
            fecha_formateadaInicio, fecha_formateadaFin = obtener_fechaIncioYFin_con_año(
                session.get("año_seleccionado"))
            pagos = pagos_por_contrato(db_session, id_cliente, añoInicio=fecha_formateadaInicio,
                                       añoFin=fecha_formateadaFin, estado_contrato=activo, estado_detalle_pago=monedaOriginal)

        else:
            fecha_formateadaInicio, fecha_formateadaFin = obtener_fechaIncioYFin_con_año(
                años_pagos[0][0])
            pagos = pagos_por_contrato(db_session, id_cliente, añoInicio=fecha_formateadaInicio,
                                       añoFin=fecha_formateadaFin, estado_contrato=activo, estado_detalle_pago=monedaOriginal)
    else:
        pagos = []



    print(monto_pagoEspecial)
    formulario_añadir_pago = {
        "datos_cliente": pagos_cliente,
        "monto_pagoEspecial": monto_pagoEspecial,
        "pagos": pagos,
        "años_pagos": años_pagos,
        "saldo_pendiente": validar_existencia_saldo_frontEnd(db_session, id_cliente),
        "estado_pago_corte" : obtener_estadoPagoClienteCorte(db_session, id_cliente, id_contrato, pagos_cliente[0]["pagoQuincenal"], pagos_cliente[0]["pagoMensual"], datetime.now()),
    }

    print(pagos_cliente)

    
    if pagos_cliente[0]["id_tipoCliente"] == cliente_especial:
        total_pagos = Decimal(sumatoria_de_pagos_Cliente_especial(db_session, id_contrato))
        capital = Decimal(pagos_cliente[0]["monto_solicitado"])
        saldo_pendiente = capital - total_pagos
        print("El saldo pendiente es: ", saldo_pendiente)
        formulario_añadir_pago.update({"saldo_pendiente": saldo_pendiente})
        


    return render_template('pagos/añadir_pago.html', **formulario_añadir_pago)


def generar_pdf_desde_html(html):
    htmldoc = weasyprint.HTML(string=html, base_url="")
    return htmldoc.write_pdf()

@app.route('/Imprimir_pago', methods=['GET', 'POST'])
def PruebaImprimir_pago():

        data = request.get_json()
        print(data)
        if not data:
            return jsonify({"error": "No se está recibiendo ninguna información"}), 400

        id_cliente = data.get('id_cliente')
        fecha_inicio = data.get('fechaInicio')
        fecha_fin = data.get('fechaFin')



        fecha_inicio_QUEES = sumar_dias(fecha_inicio, 15)

        fecha_inicio_totalSaldo = '2010-01-01'
        fecha_fin_totalSaldo = fecha_inicio

        if not all([id_cliente, fecha_inicio, fecha_fin]):
            return jsonify({"error": "No se está obteniendo toda la información requerida"}), 400
        
        suma_saldo = transacciones_saldo_contrato(db_session, id_cliente, fecha_inicio_totalSaldo, fecha_fin_totalSaldo, activo, monedaOriginal, consulta_sumatoria_total, 0)

        quincenaFechaFinTs, mesFechaFinTs, anioFechaFinTs = obtener_quincenaActual_letras(fecha_fin_totalSaldo)
        fecha_fin_totalSaldoFormateado = f"{quincenaFechaFinTs} quincena de {mesFechaFinTs} del {anioFechaFinTs}"

        quincenaFechaFin, mesFechaFin, anioFechaFin = obtener_quincenaActual_letras(fecha_fin)
        fecha_finFormateado = f"{quincenaFechaFin} quincena de {mesFechaFin} del {anioFechaFin}"

        dataPagos_cliente = datos_pagov2(id_cliente, db_session)

        datos_pago = {
            'dataPagos_cliente' : dataPagos_cliente,
            'pagos' : pagos_por_contrato(db_session, id_cliente, añoInicio=fecha_inicio,
                                   añoFin=fecha_fin, estado_contrato=activo, estado_detalle_pago=monedaOriginal),
            'transacciones_saldos' : transacciones_saldo_contrato(db_session, id_cliente, fecha_inicio, fecha_fin, activo, monedaOriginal, consulta_normal, suma_saldo),
            'suma_saldo' : suma_saldo,
            'fecha_saldo_inicial': f'{fecha_fin_totalSaldoFormateado} ({fecha_fin_totalSaldo})',
            'fecha_saldo_final': f'{fecha_finFormateado} ({fecha_fin})',
            'saldo_pendiente' : validar_existencia_saldo(db_session, id_cliente),
        }

        html_formulario = render_template('pagos/imprimir_pago_template.html', **datos_pago)

        if data.get('checkBoxEnvioCorreo'):
            correo_electronico = data.get('correoElectronico')
            print(correo_electronico)
            cuerpo = html_formulario

            # Genera el PDF desde tu HTML (ya lo tienes)
            pdf_binario = generar_pdf_desde_html(html_formulario)

            with app.app_context():
                print(dataPagos_cliente)
                mensaje = Message(f'Historial de pagos de: {dataPagos_cliente[0]["nombres"]} {dataPagos_cliente[0]["apellidos"]}', recipients=[correo_electronico])
                mensaje.body = 'Hola! Se envía el historial de pagos en formato PDF del cliente solicitado.'

                # Adjuntar el PDF en formato binario
                mensaje.attach(filename=f'{dataPagos_cliente[0]["nombres"]}_{dataPagos_cliente[0]["apellidos"]}_historial_pagos.pdf', content_type='application/pdf', data=pdf_binario)

                # Enviar el correo electrónico
                mail.send(mensaje)


        

        return Response(html_formulario, mimetype='text/html'), 200




    

@app.route('/eliminar_pago', methods=['POST'])
def eliminar_pago():
    data = request.get_json()
    id_pagos = data.get('id_pago')

    print("El id del pago es " + str(id_pagos))

    db_session.begin()

    try:
        # Obtener el estado del pago para saber si el pago está pagado o no
        estado_pago = int(obtener_estado_pago(db_session, id_pagos))

        # Eliminamos el pago mediante un proceso de eliminación en la función
        eliminar_pago_idPagos(db_session, id_pagos, estado_pago)
        db_session.commit()
        # Emite un evento personalizado a los clientes conectados
        return jsonify({'message': 'Pago eliminado'}), 200

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': f'Error en la base de datos: {str(e)}'}), 500

    except Exception as e:
        db_session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': f'Error desconocido: {str(e)}'}), 500

    finally:
        db_session.close()


@app.route('/informacion_pagoEspecifico', methods=['POST'])
def informacion_pagoEspecifico():
    try:
        data = request.get_json()
        id_pagos = data.get('id_pagos')

        pago = buscar_detalle_pago_idPagos(db_session, id_pagos)
        print(pago)

        return jsonify({"pago": pago}), 200
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': f'Error en la base de datos: {str(e)}'}), 500

    except Exception as e:
        db_session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': f'Error desconocido: {str(e)}'}), 500

    finally:
        db_session.close()


@app.route('/verificar_pago_quincenal', methods=['POST'])
def verificar_pago_quincenal():

    data = request.get_json()
    data_anadida = data.get('data')

    id_cliente = data_anadida.get('id_cliente')
    fecha = data_anadida.get('fecha_a_pagar')

    monto_pagoEspecial = obtener_pagoEspecial(db_session, id_cliente, fecha)

    return jsonify({"monto_pagoEspecial": monto_pagoEspecial}), 200


@app.route('/prueba_extraer_plata', methods=['GET', 'POST'])
def prueba_extraer_plata():

    dolar = obtener_tasa_cambio_oficial()

    return 'Si entró!'

########### Empieza el modulo de contrato ##########

@app.route('/visualizar_contrato/<int:id_cliente>', methods=['GET', 'POST'])
@login_requiredUser
def visualizar_contrato(id_cliente):


    id_contratoActual = obtener_IdContrato(db_session, id_cliente)
    datos_cliente = listar_datosClienteContratoCompleto(db_session, id_cliente)
    datos_contratoCliente = listarDatosContratoID_contrato(db_session, id_contratoActual)

    datos_contratoFiador = listarDatosFiadorContratoID_contratoFiador(db_session, datos_contratoCliente[0])
    datos_fiador = listar_datosClienteContratoCompleto(db_session, datos_contratoFiador[1])

    print(datos_cliente)

    datos_formulario_anadir_prestamo = {
        "id_cliente": id_cliente,
        "id_contratoActual" : id_contratoActual,
        "companias_telefonicas": obtener_companias_telefonicas(db_session),
        "tipos_monedas": obtener_tipos_monedas(db_session),
        "datos_cliente": datos_cliente,
        "datos_contratoCliente": datos_contratoCliente,
        "datos_contratoFiador": datos_contratoFiador,
        "datos_fiador" : datos_fiador,
    }

    return render_template('contrato/visualizar_contrato.html', **datos_formulario_anadir_prestamo)


@app.route('/visualizar_contrato_id/<int:id_contrato>', methods=['GET', 'POST'])
@login_requiredUser
def visualizar_contrato_id(id_contrato):

    id_cliente = seleccionar_idCliente_por_idContrato(db_session, id_contrato)
    datos_cliente = listar_datosClienteContratoCompleto(db_session, id_cliente)
    datos_contratoCliente = listarDatosContratoID_contrato(db_session, id_contrato)

    datos_contratoFiador = listarDatosFiadorContratoID_contratoFiador(db_session, datos_contratoCliente[0])
    datos_fiador = listar_datosClienteContratoCompleto(db_session, datos_contratoFiador[1])

    print(datos_cliente)

    datos_formulario_anadir_prestamo = {
        "id_cliente": id_cliente,
        "id_contratoActual" : id_contrato,
        "companias_telefonicas": obtener_companias_telefonicas(db_session),
        "tipos_monedas": obtener_tipos_monedas(db_session),
        "datos_cliente": datos_cliente,
        "datos_contratoCliente": datos_contratoCliente,
        "datos_contratoFiador": datos_contratoFiador,
        "datos_fiador" : datos_fiador,
    }

    return render_template('contrato/visualizar_contrato.html', **datos_formulario_anadir_prestamo)


@app.route('/finalizar_pago/<int:id_cliente>', methods=['GET', 'POST'])
@login_requiredUser
def finalizar_contrato(id_cliente):

    if request.method == 'POST':

        fechaFinalizacion = request.form['fechaFinalizacion']
        observacionFinalizacion = request.form['observacionFinalizacion']



        db_session.begin()

        try:
            cambiar_estadoContrato_finalizado(db_session, id_cliente, inactivo)

            id_contratoActivo = obtener_IdContratoActivo(db_session, id_cliente)

            finalizacionContratoDescripcion(db_session, id_contratoActivo, fechaFinalizacion, observacionFinalizacion)

            actualizarEstadoCliente(db_session, id_cliente, inactivo)





            db_session.commit()

            

        except:
            db_session.rollback()
            return redirect(url_for('visualizar_contrato', id_cliente=id_cliente, error="Error en la base de datos"))



@app.route('/borrar_sesion', methods=['GET', 'POST'])
def borrar_sesion():
    session.pop("access_token", None)
    session.pop("refresh_token", None)
    return "listo!"


########### Empieza el modulo de capital ###########

########### EMPIZA MODOULO DE CONFIGURACION ###########

########### EMPIZA MODULO DE BASE DE DATOS ###########
app.secret_key = 'your_secret_key'

@app.route('/login')
def login():
    auth_url = "https://www.dropbox.com/oauth2/authorize"
    params = {
        "client_id": os.getenv("DROPBOX_APP_KEY"),
        "response_type": "code",
        "redirect_uri": url_for('callback', _external=True),
        "token_access_type": "offline",
        "scope": "files.content.write sharing.read sharing.write files.metadata.write files.content.read"
    }
    return redirect(auth_url + "?" + urlencode(params))

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = "https://api.dropboxapi.com/oauth2/token"
    response = requests.post(token_url, data={
        "code": code,
        "grant_type": "authorization_code",
        "client_id": os.getenv("DROPBOX_APP_KEY"),
        "client_secret": os.getenv("DROPBOX_APP_SECRET"),
        "redirect_uri": url_for('callback', _external=True)
    })

    try:
        # Intenta decodificar la respuesta JSON
        tokens = response.json()
    except ValueError:
        # Imprime el contenido de la respuesta si no es un JSON válido
        print("Error: no se pudo decodificar la respuesta JSON")
        print("Contenido de la respuesta:", response.text)
        return "Error: no se pudo decodificar la respuesta JSON"

    session['access_token'] = tokens['access_token']
    session['refresh_token'] = tokens['refresh_token']
    print("Tokens saved!")
    return redirect(url_for('base_de_datos'))

def refresh_access_token(refresh_token):
    token_url = "https://api.dropboxapi.com/oauth2/token"
    response = requests.post(token_url, data={
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "client_id": os.getenv("DROPBOX_APP_KEY"),
        "client_secret": os.getenv("DROPBOX_APP_SECRET")
    })
    try:
        tokens = response.json()
    except ValueError:
        print("Error: no se pudo decodificar la respuesta JSON")
        print("Contenido de la respuesta:", response.text)
        return None
    return tokens['access_token']





@app.route('/base_de_datos', methods=['GET', 'POST'])
def base_de_datos():


    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))
    
    
    # Inicializa el cliente de Dropbox
    dbx = dropbox.Dropbox(access_token)



    # ID de la carpeta de Google Drive donde están los backups
    folder_id = "/GRNEGOCIO/Backups"# Reemplaza con tu ID de carpeta

    # Obtener el archivo SQL más reciente de la carpeta
    all_sql_files = get_all_sql_files(dbx, folder_id)
    print(all_sql_files)

    
    backups_files = []

    if all_sql_files:
        for file in all_sql_files:
            download_link = obtener_enlace_descarga(dbx, file.path_lower)
            delete_link = f"/delete_backup/{file.id}"
            filedate = convertir_fecha(file.client_modified)
            response = {
                "filename": file.name,
                "fileDate": filedate,
                "import_link": f"/restore?file_url={download_link}",
                
                "download_link": download_link,
                "delete_link": delete_link
            }
            backups_files.append(response)
    else:
        backups_files = []


        print(backups_files)

        



    template_info = {
        "backups_files": backups_files
    }


    return render_template('base_de_datos/base_de_datos.html', **template_info)

########### TERMINA MODLU DE CONFIGURACION ###########


@app.route('/modals', methods=['GET', 'POST'])
def modals():
    return render_template('modals.html')


def busqueda_capital(nombres):

    query = text("""
    SELECT p.nombres, c.monto_capital
    FROM persona p
    JOIN capital c ON p.id_persona = c.id_persona
    WHERE UPPER(p.nombres) LIKE UPPER(:nombres);
    """)

    result = db_session.execute(query, {"nombres": nombres}).fetchone()

    return result



metadata = MetaData()
metadata.reflect(bind=engine)

def generate_create_table_statements(metadata):
    """Genera sentencias CREATE TABLE para todas las tablas en el metadata sin usar comillas, con validación."""
    create_statements = []
    for table in metadata.sorted_tables:
        try:
            # Compilar el CREATE TABLE statement con quoting deshabilitado
            create_statement = CreateTable(table).compile(dialect=engine.dialect, compile_kwargs={"literal_binds": True})
            # Convertir a string y eliminar las comillas invertidas manualmente
            create_statement = str(create_statement).replace('`', '')
            create_statements.append(create_statement + ";")
        except SQLAlchemyError as e:
            print(f"Error creating table {table.name}: {e}")
            # Puedes decidir si deseas continuar o detener la ejecución aquí
            continue
    return create_statements

def generate_insert_statements(table):
    """Genera sentencias INSERT para todos los datos de una tabla, con validación."""
    insert_statements = []
    try:
        with engine.connect() as connection:
            result = connection.execute(table.select())
            for row in result:
                columns = ', '.join(table.columns.keys())
                values = ', '.join("'{}'".format(str(value).replace("'", "\\'")) if value is not None else 'NULL' for value in row)
                insert_statement = "INSERT INTO {} ({}) VALUES ({});".format(table.name, columns, values)
                insert_statements.append(insert_statement)
    except SQLAlchemyError as e:
        print(f"Error generating insert statements for table {table.name}: {e}")
        # Puedes decidir si deseas continuar o detener la ejecución aquí
    return insert_statements

def drop_all_tables():
    """Elimina todas las tablas y sus datos de la base de datos."""
    metadata.reflect(bind=engine)  # Refleja el estado actual de la base de datos en el MetaData
    metadata.drop_all(bind=engine)

def execute_sql_file(sql_file_path):
    """Ejecuta todas las sentencias SQL en un archivo."""
    with engine.connect() as connection:
        try:
            with open(sql_file_path, 'r', encoding='utf-8') as file:
                sql_statements = file.read()
                for statement in sql_statements.split(';'):
                    if statement.strip():
                        connection.execute(text(statement))
            connection.commit()
        except SQLAlchemyError as e:
            connection.rollback()
            print(f"An error occurred: {e}")
            raise

@app.route('/backup', methods=['GET', 'POST'])
def backup_database_to_sql_file():
    """Genera un backup de la base de datos en forma de sentencias SQL y lo sube a Dropbox."""

    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))

    # Inicializa el cliente de Dropbox
    dbx = dropbox.Dropbox(access_token)

    backup_statements = []

    # Obtener las tablas ordenadas por dependencias de claves foráneas
    ordered_tables = metadata.sorted_tables

    # Generar CREATE TABLE statements
    create_statements = generate_create_table_statements(metadata)
    backup_statements.extend(create_statements)

    # Generar INSERT statements
    for table in ordered_tables:
        backup_statements.extend(generate_insert_statements(table))

    str_fechahora = obtener_str_fecha_hora(datetime.now())
    backup_filename = f'backup_{str_fechahora}.sql'
    backup_file_content = '\n'.join(backup_statements)

    # Crear un archivo en memoria
    backup_file = io.StringIO(backup_file_content)

    # Ruta de destino en Dropbox donde quieres subir el archivo
    dropbox_destination_path = f'/GRNEGOCIO/Backups/{backup_filename}'  # Reemplaza con la ruta deseada

    # Intentar subir el archivo desde memoria y obtener el resultado
    success, error_message = upload_to_dropbox(dbx, backup_file, dropbox_destination_path)
    
    if success:
        print("Backup completed and uploaded to Dropbox")
        return redirect(url_for('base_de_datos'))
    else:
        print(f"Error uploading to Dropbox: {error_message}")
        return f"Error uploading to Dropbox: {error_message}", 500
    

@app.route('/restore', methods=['GET'])
def restore_backup():
    """Restaura la base de datos desde un archivo de respaldo."""
    file_url = request.args.get('file_url')
    
    if not file_url:
        return "No file URL provided", 400

    print(file_url)
    
    # Asegurarse de que la URL descarga el archivo directamente
    file_url = file_url + "&dl=1"
    if "dl=0" in file_url:
        file_url = file_url.replace("dl=0", "dl=1")

    # Descargar el archivo de respaldo
    response = requests.get(file_url)
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if 'text/html' in content_type:
            return "Failed to download the backup file. The URL might be incorrect.", 500

        with tempfile.NamedTemporaryFile(delete=False, suffix='.sql') as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name

        try:
            # Eliminar todas las tablas y sus datos
            drop_all_tables()

            # Ejecutar el archivo SQL descargado
            execute_sql_file(temp_file_path)
            return "Database restored successfully", 200
        finally:
            # Eliminar el archivo temporal
            os.remove(temp_file_path)
    else:
        return "Failed to download the backup file", 500


@app.route('/get_latest_backup', methods=['GET'])
def get_latest_backup():
    # Autenticación con Google Drive

    # ID de la carpeta de Google Drive donde están los backups
    folder_id = os.getenv("ID_FOLDER")   # Reemplaza con tu ID de carpeta

    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))
    
    
    # Inicializa el cliente de Dropbox
    dbx = dropbox.Dropbox(access_token)

    # Obtener el archivo SQL más reciente de la carpeta
    latest_file = get_latest_sql_file(dbx, folder_id)
    print(latest_file)
    
    if latest_file:
        download_link = latest_file['alternateLink']
        delete_link = f"/delete_backup/{latest_file['id']}"
        response = {
            "filename": latest_file['title'],
            "fileDate" : latest_file['modifiedDate'],
            "download_link": download_link,
            "delete_link": delete_link
        }
    else:
        response = {
            "message": "No SQL files found in the specified folder."
        }

    return jsonify(response)


@app.route('/delete_backup/<path:file_path>', methods=['GET'])
def delete_backup(file_path):
    try:

        
        access_token = session.get('access_token')
        if not access_token:
            return redirect(url_for('login'))
        
        
        # Inicializa el cliente de Dropbox
        dbx = dropbox.Dropbox(access_token)


        # Obtener la ruta del archivo utilizando su ID
        metadata = dbx.files_get_metadata(file_path)
        correct_path = metadata.path_lower

        print(f"Attempting to delete file at path: {correct_path}")
        dbx.files_delete_v2(correct_path)
        response = {
            "message": "File deleted successfully."
        }
    except dropbox.exceptions.ApiError as err:
        response = {
            "message": "Failed to delete file.",
            "error": str(err)
        }
    
    return redirect(url_for('base_de_datos'))



# @app.route('/delete_backup/<file_id>', methods=['GET'])
# def delete_backup(file_id):
#     # Autenticación con Google Drive
#     drive = auth_to_drive()

#     # Eliminar el archivo especificado por file_id
#     try:
#         file = drive.CreateFile({'id': file_id})
#         file.Delete()
#         response = {"message": "File deleted successfully."}
#     except Exception as e:
#         response = {"message": f"An error occurred: {str(e)}"}

#     return jsonify(response)

# @app.route('/backup')
# def backup():
#     try:
#         # Define los detalles de la base de datos
#         db_host = "localhost"
#         db_user = "root"
#         db_password = "1233456"
#         db_name = "GRNEGOCIO"

#         # Define la ruta y el nombre del archivo de respaldo
#         backup_dir = os.path.join(os.getcwd(), "static/bd/backups")
#         os.makedirs(backup_dir, exist_ok=True)  # Crea el directorio si no existe

#         # Obtiene la fecha y hora actual y la formatea como una cadena
#         now = datetime.now()
#         timestamp = now.strftime("%Y%m%d_%H%M%S")

#         backup_file = os.path.join(backup_dir, f"backup_{timestamp}.sql").replace("\\", "/")

#         # Crea el comando de respaldo
#         command = f'mysqldump --host={db_host} --user={db_user} --password={db_password} {db_name} > "{backup_file}"'

#         # Ejecuta el comando
#         result = subprocess.run(command, shell=True, capture_output=True, text=True)

#         crear_reespaldoBD(db_session, backup_file)

#         # Crea una instancia de GoogleDrive con las credenciales de autenticación
#         drive = auth_to_drive()

#         # Sube el archivo de respaldo a Google Drive
#         folder_id = get_or_create_folder_id(drive, 'GRNEGOCIO/Bd/Backups')
#         if folder_id is not None:
#             upload_to_drive(drive, backup_file, folder_id)
#         else:
#             print('No se encontró o no se pudo crear la carpeta especificada en Google Drive.')

#         return "Respaldo realizado con éxito", 200
#     except Exception as e:
#         return str(e), 500


# @app.route('/importar_backup', methods=['GET', 'POST'])
# def importar_backup():
#     if request.method == 'POST':
#         try:
#             sql_backup = request.files['sql_backup']
#             # Define los detalles de la base de datos
#             db_host = "localhost"
#             db_user = "root"
#             db_password = "1233456"
#             db_name = "GRNEGOCIO"
#             try:
#                 sql_commands = sql_backup.read().decode()
#                 subprocess.run(['mysql', '-u'+db_user, '-p'+db_password, '-h'+db_host, '-P'+str(3306), '-D'+db_name], input=sql_commands, text=True, check=True)

#                 print("Importación exitosa.")
#             except subprocess.CalledProcessError as e:
#                 print("Hubo un error durante la importación:", str(e))
#             return "Importación exitosa", 200

#         except Exception as e:
#             return str(e), 500

#         finally:
#             db_session.close()
    
#     return 'entró al GET'
    


@app.route('/crear_nuevo_contrato', methods=['GET', 'POST'])
def crear_nuevo_contrato():


    ### DATOS DE LOS CONTRATOS Y CLIENTE
    id_contratoActual = request.form['id_contratoActual']
    id_cliente = request.form['id_cliente']
    id_contrato_fiador = request.form['id_contrato_fiador']
    id_persona = request.form['id_persona']


    ## Step-1 form ###
    
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    cedula = request.form['cedula']
    fechaNac = request.form['fechaNac']
    genero = request.form['genero']
    direccion = request.form['direccion']
    direccionMaps = request.form['direccionMaps']
    nombreDireccion = request.form['nombreDireccion']
    idCompaniTelefonica = request.form['idCompaniTelefonica']
    telefono = request.form['telefono']
    nombreTelefono = request.form['nombreTelefono']
    fotoCliente = request.files['fotoCliente']
    foto_cedula = request.files['foto_cedula']

    ### Step-2 form ###
    estadoCivil = request.form['estadoCivil']
    nombreDelegacion = request.form['nombreDelegacion']
    dptoArea = request.form['dptoArea']
    ftoColillaINSS = request.files['fotoCopiaColillaInss']
    tipoClienteString = request.form['tipoCliente']
    tipoCliente = int(tipoClienteString)
    montoSolicitado = request.form['montoSolicitado']
    tipoMonedaMontoSolictado = request.form['tipoMonedaMontoSolicitado']
    tasaInteres = request.form['tasaInteres']
    pagoMensual = request.form['pagoMensual']
    pagoQuincenal = request.form['pagoQuincenal']
    fechaPrestamo = request.form['fechaPrestamo']
    fechaPago = request.form['fechaPago']
    # Solo para clientes especiales
    intervalo_tiempoPago = request.form['IntervaloPagoClienteEspecial']
    montoPrimerPago = request.form['montoPrimerPago']

    #### Step-3 form ####
    nombresFiador = request.form['nombresFiador']
    apellidosFiador = request.form['apellidosFiador']
    cedulaFiador = request.form['cedulaFiador']
    fechaNacFiador = request.form['fechaNacFiador']
    generoFiador = request.form['generoFiador']
    estadoCivilFiador = request.form['estadoCivilFiador']
    nombreDelegacionFiador = request.form['nombreDelegacionFiador']
    dptoAreaFiador = request.form['dptoAreaFiador']
    direccionFiador = request.form['direccionFiador']
    direccionMapsFiador = request.form['direccionMapsFiador']
    nombreDireccionFiador = request.form['nombreDireccionFiador']
    idCompaniTelefonicaFiador = request.form['idCompaniTelefonicaFiador']
    telefonoFiador = request.form['telefonoFiador']
    nombreTelefonoFiador = request.form['nombreTelefonoFiador']
    fotoFiador = request.files['fotoFiador']
    foto_cedulaFiador = request.files['foto_cedulaFiador']
    fotoCopiaColillaInssFiador = request.files['fotoCopiaColillaInssFiador']

    db_session.begin()

    try:

        ## Step-1 form ###

        #### Actualizar datos del cliente ####
        actualizar_persona(db_session, id_persona, nombres, apellidos, genero,
                            cedula, fechaNac, activo)  # Actualizar datos del cliente y cambiar activo

        id_direccionYtelefono = obtenerID_direccionYtelefono(
            db_session, id_persona)
        actualizar_direccion(db_session, id_direccionYtelefono.id_direccion,
                                nombreDireccion, direccion, direccionMaps, activo)
        actualizar_telefono(db_session, id_direccionYtelefono.id_telefono,
                            idCompaniTelefonica, nombreTelefono, telefono, activo)
        actualizar_cliente(db_session, id_cliente, id_persona, tipoCliente,
                            fotoCliente, foto_cedula, activo)  # Actualizar datos del cliente y cambiar activo

        #### Terminar de actualizar datos del cliente ####

        ## Step-2 form ###

        #### Insertamos al fiador ####

        # Si el checbox se encuentra en el formulario quiere decir que no hay deudor
        if 'chckbxNoDeudor' in request.form:
            id_persona = insertar_persona(
                db_session, sin_especificar, sin_especificar, sin_especificar, sin_especificar, sin_especificar, activo)
            id_direccion = insertar_direccion(
                db_session, sin_especificar, sin_especificar, sin_especificar, activo)
            id_telefono = insertar_telefono(
                db_session, sin_especificar, sin_especificar, sin_especificar, activo)
            id_persona_direccion = insertar_persona_direccion(
                db_session, sin_especificar, sin_especificar, activo)
            id_direccion_telefono = insertar_direccion_telelfono(
                db_session, sin_especificar, sin_especificar, activo)
            id_insertar_clienteFiador = insertar_cliente(
                db_session, id_persona, fiador, sin_especificar, sin_especificar, activo)
        else:
            id_persona = insertar_persona(
                db_session, nombresFiador, apellidosFiador, generoFiador, cedulaFiador, fechaNacFiador, activo)
            id_direccion = insertar_direccion(
                db_session, nombreDireccionFiador, direccionFiador, direccionMapsFiador, activo)
            id_telefono = insertar_telefono(
                db_session, idCompaniTelefonicaFiador, nombreTelefonoFiador, telefonoFiador, activo)
            id_persona_direccion = insertar_persona_direccion(
                db_session, id_persona, id_direccion, activo)
            id_direccion_telefono = insertar_direccion_telelfono(
                db_session, id_direccion, id_telefono, activo)
            id_insertar_clienteFiador = insertar_cliente(
                db_session, id_persona, fiador, fotoFiador, foto_cedulaFiador, activo)

        #### Terminamos de insertar al fiador ####

        ##### Insertamos el contrato especificamente datos del fiador #######

        # Si el checbox se encuentra en el formulario quiere decir que no hay deudor
        if 'chckbxNoDeudor' in request.form:
            # Revisar si el fiador es no deudor se recibirá un valor de 5 en el checkbox
            checkbox_no_deudor = request.form['chckbxNoDeudor']
            id_contrato_fiador = insertar_contrato_fiador(
                db_session, id_insertar_clienteFiador, estadoCivilFiador, nombreDelegacionFiador, dptoAreaFiador, fotoCopiaColillaInssFiador, no_fiador)
        else:
            id_contrato_fiador = insertar_contrato_fiador(
                db_session, id_insertar_clienteFiador, estadoCivilFiador, nombreDelegacionFiador, dptoAreaFiador, fotoCopiaColillaInssFiador, activo)

        if tipoCliente == cliente_normal:

            id_contrato = insertar_contrato(db_session, id_cliente, estadoCivil, nombreDelegacion, dptoArea, ftoColillaINSS,
                                            montoSolicitado, tipoMonedaMontoSolictado, tasaInteres, pagoMensual, pagoQuincenal, fechaPrestamo,
                                            fechaPago, prestamo_cliente_normal, montoPrimerPago, activo)

        elif tipoCliente == cliente_especial:

            id_contrato = insertar_contrato(db_session, id_cliente, estadoCivil, nombreDelegacion, dptoArea, ftoColillaINSS,
                                            montoSolicitado, tipoMonedaMontoSolictado, tasaInteres, pagoMensual, pagoQuincenal, fechaPrestamo,
                                            fechaPago, intervalo_tiempoPago, montoPrimerPago, activo)

        # Le decimos que el contrato actual pasa a ser inactivo para darle al nuevo contrato!
        cambiar_estado_contrato(db_session, id_contratoActual, inactivo)
        cambiar_estado_contrato_fiador(db_session, id_contrato_fiador, inactivo)
        db_session.commit()

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {str(e)}")
        return redirect(url_for('prestamos', error="Error en la base de datos"))

    except Exception as e:
        db_session.rollback()
        print(f"Unexpected error: {str(e)}")
        return render_template('error.html', error="Unexpected error occurred"), 500

    finally:
        db_session.close()


    return jsonify({'status': 'success'}), 200

    




@app.route('/obtener_datos_ultimo_backup' , methods=['GET', 'POST'])
def obtener_datos_ultimo_backup():
    try:
        backup = seleccionar_ultimo_backup(db_session)
        return jsonify({"backup": backup}), 200
    except Exception as e:
        return str(e), 500

@app.route('/api/obtener_capital', methods=['GET', 'POST'])
@cross_origin()
def obtener_capital():
    if request.method == 'POST':
        data = request.json

        nombres = data['person']

        try:
            result = busqueda_capital(nombres)
            if result:
                montoCapital_Texto = f"{num2words(result.monto_capital, lang='es')} cordobas"
                return jsonify({"nombres": result.nombres, "monto_capital": montoCapital_Texto}), 200
            else:
                return jsonify({"message": "No se encontro el nombre"}), 404
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {e}")
            return jsonify({"message": "Error en la base de datos"}), 500
    else:
        return jsonify({"message": "Metodo no permitido"}), 400
    


@app.route('/Cerrar_Sesion')
def Cerrar_Sesion():
    
    session.pop('user_id', None)
    session.pop('name', None)
    session.pop('lastname', None)
    return redirect(url_for('index'))




########### Empieza API ###########

@app.route('/api/obtener_estadoCliente', methods=['GET', 'POST'])
@cross_origin()
def obtener_estadoCliente():
    if request.method == 'POST':
        data = request.json

        nombre_cliente = data['person']

       


        try:
            cadena_respuesta = crear_cadena_respuesta_estado_cliente(db_session, nombre_cliente)
            return jsonify({"respuesta": cadena_respuesta}), 200
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {e}")
            return jsonify({"message": "Error en la base de datos"}), 500
    else:
        return jsonify({"message": "Metodo no permitido"}), 400
    

@app.route('/api/obtener_cantidad_pago_cliente', methods=['GET', 'POST'])
@cross_origin()
def obtener_cantidad_pago_cliente():
    if request.method == 'POST':
        data = request.json

        nombre_cliente = data['person']
        print(nombre_cliente)

       


        try:
            cadena_respuesta = crear_cadena_respuesta_cantidad_pago_cliente(db_session, nombre_cliente)
            return jsonify({"respuesta": cadena_respuesta}), 200
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {e}")
            return jsonify({"message": "Error en la base de datos"}), 500
    else:
        return jsonify({"message": "Metodo no permitido"}), 400
    

@app.route('/api/obtener_cantidad_clientes_pagados', methods=['GET'])
@cross_origin()
def obtener_cantidad_clientes_pagados():

    try:
        cadena_respuesta = crear_cadena_respuesta_cantidad_de_clientes_pagados(db_session)
        return jsonify({"respuesta": cadena_respuesta}), 200
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": "Error en la base de datos"}), 500


@app.route('/api/obtener_cantidad_total_dinero_quincenal_clientes', methods=['GET'])
@cross_origin()
def obtener_cantidad_total_dinero_quincenal_clientes():

    try:
        cadena_respuesta = crear_cadena_respuesta_cantidad_total_dinero_quincenal_clientes(db_session)
        return jsonify({"respuesta": cadena_respuesta}), 200
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": "Error en la base de datos"}), 500

    

@app.route('/api/imprimir_pago_alexa', methods=['GET', 'POST'])
def imprimir_pago_alexa():



        data = request.json

        nombre_cliente = data['person']

        try:

            # Obtener ID del cliente por nombre
            id_cliente = seleccionar_clientes_activos(db_session, nombre_cliente)

            mes_estatico, dia_estatico = 1, 1  # Mes: enero, Día: 15
            fecha_inicio = datetime.now().replace(month=mes_estatico, day=dia_estatico).strftime('%Y-%m-%d')

            fecha_fin = datetime.now().strftime('%Y-%m-%d')



            fecha_inicio_QUEES = sumar_dias(fecha_inicio, 15)

            fecha_inicio_totalSaldo = '2010-01-01'
            fecha_fin_totalSaldo = fecha_inicio

            if not all([id_cliente, fecha_inicio, fecha_fin]):
                return jsonify({"error": "No se está obteniendo toda la información requerida"}), 400
            
            suma_saldo = transacciones_saldo_contrato(db_session, id_cliente, fecha_inicio_totalSaldo, fecha_fin_totalSaldo, activo, monedaOriginal, consulta_sumatoria_total, 0)

            quincenaFechaFinTs, mesFechaFinTs, anioFechaFinTs = obtener_quincenaActual_letras(fecha_fin_totalSaldo)
            fecha_fin_totalSaldoFormateado = f"{quincenaFechaFinTs} quincena de {mesFechaFinTs} del {anioFechaFinTs}"

            quincenaFechaFin, mesFechaFin, anioFechaFin = obtener_quincenaActual_letras(fecha_fin)
            fecha_finFormateado = f"{quincenaFechaFin} quincena de {mesFechaFin} del {anioFechaFin}"

            dataPagos_cliente = datos_pagov2(id_cliente, db_session)

            datos_pago = {
                'dataPagos_cliente' : dataPagos_cliente,
                'pagos' : pagos_por_contrato(db_session, id_cliente, añoInicio=fecha_inicio,
                                    añoFin=fecha_fin, estado_contrato=activo, estado_detalle_pago=monedaOriginal),
                'transacciones_saldos' : transacciones_saldo_contrato(db_session, id_cliente, fecha_inicio, fecha_fin, activo, monedaOriginal, consulta_normal, suma_saldo),
                'suma_saldo' : suma_saldo,
                'fecha_saldo_inicial': f'{fecha_fin_totalSaldoFormateado} ({fecha_fin_totalSaldo})',
                'fecha_saldo_final': f'{fecha_finFormateado} ({fecha_fin})',
                'saldo_pendiente' : validar_existencia_saldo(db_session, id_cliente),
            }

            html_formulario = render_template('pagos/imprimir_pago_template.html', **datos_pago)

            
            correo_electronico = os.getenv('CORREO_ELECTRONICO_ALEXA_API')
            print(correo_electronico)
            cuerpo = html_formulario

            # Genera el PDF desde tu HTML (ya lo tienes)
            pdf_binario = generar_pdf_desde_html(html_formulario)

            with app.app_context():
                print(dataPagos_cliente)
                mensaje = Message(f'Historial de pagos de: {dataPagos_cliente[0]["nombres"]} {dataPagos_cliente[0]["apellidos"]}', recipients=[correo_electronico])
                mensaje.body = 'Hola! Se envía el historial de pagos en formato PDF del cliente solicitado.'

                # Adjuntar el PDF en formato binario
                mensaje.attach(filename=f'{dataPagos_cliente[0]["nombres"]}_{dataPagos_cliente[0]["apellidos"]}_historial_pagos.pdf', content_type='application/pdf', data=pdf_binario)

                # Enviar el correo electrónico
                mail.send(mensaje)

            return jsonify({"respuesta": "Listo, he enviado el historial de pagos a tu teléfono"}), 200

        except SQLAlchemyError as e:
            print(f"Error: {e}")
            return jsonify({"error": "Error en la base de datos"}), 500
        
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "Error desconocido"}), 500
        
        finally:
            db_session.close()

from flask import request, jsonify

@app.route('/api/registrar_pago_completo', methods=['POST'])
def registrar_pago_completo():
    # Aquí puedes obtener datos de la solicitud si es necesario
    # data = request.json

    # Lógica para registrar el pago completo
    # Por ejemplo, actualizar una base de datos o realizar otra operación de backend
    # Este es un paso ficticio, reemplázalo con la lógica real de tu aplicación
    pago_registrado = True  # Simula la lógica de registro de pago

    if pago_registrado:
        # Si el pago se registró correctamente, devuelve una respuesta positiva
        return jsonify({"mensaje": "Pago completo registrado con éxito"}), 200
    else:
        # Si hubo un problema registrando el pago, devuelve un error
        return jsonify({"error": "No se pudo registrar el pago completo"}), 500

@app.route('/api/obtener_pago', methods=['GET', 'POST'])
def obtener_pago():
    data = request.json

    nombre_cliente = data['person']

    cadena_texto_respuesta = obtener_pagoClienteTexto(db_session, nombre_cliente)

    return jsonify({"respuesta": cadena_texto_respuesta}), 200


########### Termina API ###########


@app.route('/pruebita', methods=['GET', 'POST'])
@cross_origin()
def pruebita():

    if request.method == 'GET':
        return jsonify({"message": "API is working"}), 200
    else:
        return jsonify({"message": "API is notworking"}), 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
