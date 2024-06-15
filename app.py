from logging import getLogger
import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, session, url_for, redirect, Response, send_file
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit
from io import BytesIO
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from num2words import num2words
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS, cross_origin
from datetime import datetime
from babel.dates import format_date
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
from models.base_de_datos import *
from flask_cors import CORS
from serverEmail import mail

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"
socketio = SocketIO(app, cors_allowed_origins='*')
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


@socketio.on('cliente_conectado')
def handle_message():
    print('Cliente conectado')


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
def datos_cliente():
    return render_template('datos_cliente.html')


########### Empieza el modulo de prestamos ###########
@app.route('/prestamos', methods=['GET', 'POST'])
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


########### Empieza el modulo de pagos ############

@app.route('/listado_clientes_pagos', methods=['GET', 'POST'])
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





@app.route('/añadir_pago/<int:id_cliente>', methods=['GET', 'POST'])
def añadir_pago(id_cliente):

    if request.method == 'POST':

        id_moneda = request.form['tipoMonedaPago']
        cantidadPagarDolares = request.form['cantidadPagar$']
        cantidadPagarCordobas = request.form.get('cantidadPagoCordobas')
        inputTasaCambioPago = request.form['inputTasaCambioPago']
        fechaPago = request.form['fechaPago']
        observacionPago = request.form['observacionPago']
        evidenciaPago = request.files['evidenciaPago']
        tipoPagoCompletoForm = int(request.form['tipoPagoCompleto'])

        cantidadPagarDolares = convertir_string_a_decimal(cantidadPagarDolares)

        # Verifica si el checkbox de no pago está marcado
        if 'checkBoxNoPago' in request.form:
            estadoPago = no_hay_pago  # Establece el estado de pago como no pagado

        elif 'checkBoxPrimerPago' in request.form:
            # Establece el estado de pago como primer pago
            estadoPago = primer_pago_del_prestamo
        else:
            estadoPago = tipoPagoCompletoForm  # Utiliza el estado de pago completo

        id_moneda = int(id_moneda)

        if cantidadPagarCordobas:
            cantidadPagarCordobas_conversion = convertir_string_a_decimal(
                cantidadPagarCordobas)

        else:
            cantidadPagarCordobas_conversion = 0.00

        resultado_pago_fecha = obtener_pagoEspecial(
            db_session, id_cliente, fechaPago)
        # saldo_pendiente = validar_existencia_saldo(db_session, id_cliente)
        # saldo_a_favor = validar_saldo_pendiente_a_favor(db_session, id_cliente)
        cifra_a_pagar = resultado_pago_fecha['cifra']
        print(cifra_a_pagar)

        db_session.begin()

        try:
            id_contrato = obtener_IdContrato(db_session, id_cliente)

            num_pagos = comprobar_primerPago(db_session, id_contrato)

            id_pagos = insertarPago(
                db_session, id_contrato, id_cliente, observacionPago, evidenciaPago, fechaPago, estadoPago)
            insertar_detalle_pagos(
                db_session, id_pagos, dolares, cantidadPagarDolares, None, monedaOriginal)

            if id_moneda is not dolares:

                insertar_detalle_pagos(db_session, id_pagos, id_moneda,
                                       cantidadPagarCordobas_conversion, inputTasaCambioPago, monedaConversion)

            diferencia_pago_a_saldo = obtener_diferencia_a_saldo(
                cantidadPagarDolares, cifra_a_pagar)
            print(
                f'la diferencia del pago a saldo es: {diferencia_pago_a_saldo}')
            
            # Si se obtiene una diferencia de pago a saldo menor a lo que se debe de pagar se deberá de aumentar el saldo (restar)
            if estadoPago == 0:
                cantidadPagarDolaresNegativo = cantidadPagarDolares - \
                    (cantidadPagarDolares * 2)
                id_saldos_pagos = ingreso_saldo(db_session, id_cliente, id_pagos, saldo_en_contra, id_moneda,
                                                cantidadPagarDolaresNegativo, activo)
                insertar_transaccion_saldo(
                    db_session, id_saldos_pagos, id_pagos, id_moneda, cantidadPagarDolaresNegativo, Disminucion)

            # Si se obtiene una diferencia de pago a saldo mayor a lo que se debe de pagar se deberá restar el saldo (sumar)
            elif diferencia_pago_a_saldo:
                id_saldos_pagos = ingreso_saldo(db_session, id_cliente, id_pagos, saldo_a_favor, id_moneda,
                                                diferencia_pago_a_saldo, activo)
                insertar_transaccion_saldo(
                    db_session, id_saldos_pagos, id_pagos, id_moneda, diferencia_pago_a_saldo, Aumento)



        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {e}")
            return redirect(url_for('añadir_pago', id_cliente=id_cliente, error="Error en la base de datos"))

        except Exception as e:
            db_session.rollback()
            print(f"Error: {e}")
            return redirect(url_for('añadir_pago', id_cliente=id_cliente, error="Error en la base de datos"))

        db_session.commit()

        # Emite un evento personalizado a los clientes conectados
        socketio.emit('pago_realizado', {'cliente_id': id_cliente})

        return redirect(url_for('añadir_pago', id_cliente=id_cliente))

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

    db_session.begin()

    try:
        # Obtener el estado del pago para saber si el pago está pagado o no
        estado_pago = int(obtener_estado_pago(db_session, id_pagos))

        # Eliminamos el pago mediante un proceso de eliminación en la función
        eliminar_pago_idPagos(db_session, id_pagos, estado_pago)
        db_session.commit()
        # Emite un evento personalizado a los clientes conectados
        socketio.emit('Se eliminó un pago', {'id_pago': id_pagos})
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
def visualizar_contrato(id_cliente):


    id_contratoActual = obtener_IdContrato(db_session, id_cliente)
    datos_cliente = listar_datosClienteContratoCompleto(db_session, id_cliente)
    datos_contratoCliente = listarDatosContratoID_contrato(db_session, id_contratoActual)

    datos_contratoFiador = listarDatosFiadorContratoID_contratoFiador(db_session, datos_contratoCliente[0])
    datos_fiador = listar_datosClienteContratoCompleto(db_session, datos_contratoFiador[1])






    
    print(datos_cliente)

    datos_formulario_anadir_prestamo = {
        "companias_telefonicas": obtener_companias_telefonicas(db_session),
        "tipos_monedas": obtener_tipos_monedas(db_session),
        "datos_cliente": datos_cliente,
        "datos_contratoCliente": datos_contratoCliente,
        "datos_contratoFiador": datos_contratoFiador,
        "datos_fiador" : datos_fiador,
    }

    return render_template('contrato/visualizar_contrato.html', **datos_formulario_anadir_prestamo)




########### Empieza el modulo de capital ###########

########### EMPIZA MODOULO DE CONFIGURACION ###########

########### EMPIZA MODULO DE BASE DE DATOS ###########
@app.route('/base_de_datos', methods=['GET', 'POST'])
def base_de_datos():


    return render_template('base_de_datos/base_de_datos.html')

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



# Obtener metadatos
metadata = MetaData()
metadata.reflect(bind=engine)

def generate_insert_statements(table):
    """Genera sentencias INSERT para todos los datos de una tabla."""
    insert_statements = []
    with engine.connect() as connection:
        result = connection.execute(table.select())
        for row in result:
            columns = ', '.join(table.columns.keys())
            values = ', '.join("'{}'".format(str(value).replace("'", "\\'")) if value is not None else 'NULL' for value in row)
            insert_statement = "INSERT INTO {} ({}) VALUES ({});".format(table.name, columns, values)
            insert_statements.append(insert_statement)
    return insert_statements


@app.route('/backup')
def backup_database_to_insert_statements():
    """Genera un backup de la base de datos en forma de sentencias INSERT y lo guarda en un archivo."""
    backup_statements = []
    for table_name, table in metadata.tables.items():
        backup_statements.extend(generate_insert_statements(table))
    
    with open('backup.sql', 'w') as backup_file:
        backup_file.write('\n'.join(backup_statements))
    
    return "Backup completed", 200


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


@app.route('/pruebita', methods=['GET', 'POST'])
@cross_origin()
def pruebita():

    if request.method == 'GET':
        return jsonify({"message": "API is working"}), 200
    else:
        return jsonify({"message": "API is notworking"}), 400


if __name__ == '__main__':
    socketio.run(app)
    app.run(host='127.0.0.1', port=8000, debug=True)
