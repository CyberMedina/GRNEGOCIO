from flask import jsonify, render_template
from models.clientes import *
from models.contratos import *
from models.constantes import *
from models.pagos import *
from database_connection import *
from helpers import *
from num2words import num2words
from rapidfuzz import process, fuzz
import unidecode
import math




def obtenerIdClientePorNombre(db_session, nombre):
    try:
        query = text("""
SELECT c.id_cliente
FROM cliente c
JOIN persona p ON c.id_persona = p.id_persona
WHERE CONCAT(p.nombres, ' ', p.apellidos) LIKE CONCAT('%', :cadena, '%')
LIMIT 1;


        """)
        result = db_session.execute(query, {"cadena": nombre}).fetchone()
        return result[0]
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()

def seleccionar_clientes_activos(db_session, search_term):
    try:
        query = text(""" 
        SELECT 
            c.id_cliente, 
            p.nombres, 
            p.apellidos
        FROM 
            cliente c
        INNER JOIN 
            persona p ON c.id_persona = p.id_persona
        WHERE 
            c.id_tipoCliente BETWEEN :estado1 AND :estado2;
        """)
        result = db_session.execute(query, {"estado1": cliente_normal, "estado2": cliente_especial}).fetchall()
        
        # Convertir los resultados a una lista de diccionarios
        results = [dict(row._mapping) for row in result]
        
        # Normalizar los nombres y el término de búsqueda
        search_term_normalized = unidecode.unidecode(search_term.lower())
        names = []
        name_to_person = {}
        for person in results:
            full_name = f"{person['nombres']} {person['apellidos']}".lower()
            full_name_normalized = unidecode.unidecode(full_name)
            names.append(full_name_normalized)
            name_to_person[full_name_normalized] = person
        
        # Buscar coincidencias difusas
        matches = process.extract(search_term_normalized, names, limit=3, scorer=fuzz.token_set_ratio)
        print(matches)
    
        # Filtrar resultados para encontrar la mejor coincidencia
        best_match = None
        highest_score = 0
        for match in matches:
            if match[1] > highest_score and match[1] > 50:  # Ajusta el umbral según sea necesario
                best_match = match[0]
                highest_score = match[1]
    
        if best_match:
            return name_to_person[best_match]['id_cliente']  # Retorna el id_cliente que coincide
        else:
            return None  # No se encontró una coincidencia adecuada
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def obtenerDatosClienteporID(db_session, id_cliente):

    id_contrato = obtener_IdContrato(db_session, id_cliente)

    num_pagos = comprobar_primerPago(db_session, id_contrato)

    pagos_cliente = datos_pagov2(id_cliente, db_session)

    # saldo_pendiente = validar_saldo_pendiente_en_contra(db_session, id_cliente)
    # Definimos la cifra pago especial
    monto_pagoEspecial = 0.00

    fecha_actual = datetime.datetime.now()

    monto_pagoEspecial = obtener_pagoEspecial(
        db_session, id_cliente, fecha_actual)

    # Procesos para las sesiones de los filtros de los pagos
    años_pagos = obtener_años_pagos(db_session, id_cliente, activo)

    pagos = []

    if años_pagos:

        fecha_formateadaInicio, fecha_formateadaFin = obtener_fechaIncioYFin_con_año(
                años_pagos[0][0])
        pagos = pagos_por_contrato(db_session, id_cliente, añoInicio=fecha_formateadaInicio,
                                       añoFin=fecha_formateadaFin, estado_contrato=activo, estado_detalle_pago=monedaOriginal)
    else:
        pagos = []



    formulario_añadir_pago = {
        "datos_cliente": pagos_cliente,
        "monto_pagoEspecial": monto_pagoEspecial,
        "pagos": pagos,
        "años_pagos": años_pagos,
        "saldo_pendiente": validar_existencia_saldo_frontEnd(db_session, id_cliente),
        "estado_pago_corte" : obtener_estadoPagoClienteCorte(db_session, id_cliente, id_contrato, pagos_cliente[0]["pagoQuincenal"], pagos_cliente[0]["pagoMensual"], datetime.datetime.now()),
    }


    return formulario_añadir_pago

def crear_cadena_respuesta_estado_cliente(db_session, nombre_cliente):

    print("Creando cadena de respuesta...")
    print(nombre_cliente)
    

    # Obtener ID del cliente por nombre
    id_cliente = seleccionar_clientes_activos(db_session, nombre_cliente)

    # Obtener datos del cliente por ID
    datos_cliente = obtenerDatosClienteporID(db_session, id_cliente)

    # Obtenemos los datos del contrato y del cliente meidante el ID del cliente
    id_contratoActual = obtener_IdContrato(db_session, id_cliente)

    # Obtener datos del ultimo pago
    ultimo_pago = ultimo_pago_contrato(db_session, id_contratoActual)


    # Obtener la quincena actual
    quincena, mes, anio = obtener_quincenaActual_letras(datetime.datetime.now())
    quincena_actual = f"{quincena} quincena de {mes} de {anio}"

    # Extraer datos necesarios del cliente
    nombres = datos_cliente['datos_cliente'][0]['nombres']
    apellidos = datos_cliente['datos_cliente'][0]['apellidos']

    if ultimo_pago:
    #Extraer datos necesarios del ultimo pago
        cifra_ultimo_pago_letras = num2words(ultimo_pago[0][8], lang='es')
        cifra_ultimo_pago = ultimo_pago[0][8]
        fecha_ultimo_pago = ultimo_pago[0][3]
        fecha_ultimo_pago_letras = ultimo_pago[0][15]

        str_pago = f"el último pago que tengo registrado es el {fecha_ultimo_pago}, osea en la {fecha_ultimo_pago_letras}, con un monto de {cifra_ultimo_pago_letras} dólares"
    else:
        str_pago = "no tengo registrado ningún pago"
    


    print(datos_cliente['estado_pago_corte'])

    # Determinar el estado del pago y construir la respuesta
    if datos_cliente['estado_pago_corte']['estado'] == 1:
        estado_pago = "está al día con sus pagos"
    else:
        estado_pago = "no va al día"

    # Determinar si el cliente tiene saldo pendiente
    if datos_cliente['saldo_pendiente'] is not None and datos_cliente['saldo_pendiente'][3] is not None:
        saldo_pendiente_letras = num2words(datos_cliente['saldo_pendiente'][3], lang='es')
        saldo_pendiente_letras = f"tiene un saldo de {saldo_pendiente_letras} dólares"
        saldo_numerico = datos_cliente['saldo_pendiente'][3]
        
    else:
        saldo_pendiente_letras = "no tiene saldo pendiente"
        saldo_numerico = 0


    respuesta_cadena_texto = f"A la {quincena_actual}, el cliente {nombres} {apellidos} {estado_pago}, de hecho {str_pago}  y,  {saldo_pendiente_letras}."


    respuesta ={
        "alexa_speak": respuesta_cadena_texto,
        "alexa_display": {
            "nombre_cliente": f"{nombres} {apellidos}",
            "estado_pago": estado_pago,
            "fecha_ultimo_pago": fecha_ultimo_pago_letras,
            "monto_ultimo_pago": cifra_ultimo_pago,
            "saldo_pendiente": saldo_numerico,
        }
    }

        
    dataPagos_cliente = datos_pagov2(id_cliente, db_session)

    if dataPagos_cliente[0]["id_tipoCliente"] == cliente_especial:
            id_contrato = obtener_IdContrato(db_session, id_cliente)
            total_pagos = Decimal(sumatoria_de_pagos_Cliente_especial(db_session, id_contrato))
            capital = Decimal(dataPagos_cliente[0]["monto_solicitado"])
            capital_a_la_fecha = capital - total_pagos
            capital_a_la_fecha_letras = num2words(capital_a_la_fecha, lang='es')

            respuesta['alexa_speak'] += f"El capital a la fecha es de {capital_a_la_fecha_letras} dólares."
            respuesta['alexa_display']['capital_a_la_fecha'] = capital_a_la_fecha




    return respuesta




def imprimirPagoAlexa(db_session, id_cliente, fecha_inicio, fecha_fin, correo_electronico):
    try:
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

        return jsonify({"mensaje": "Correo enviado exitosamente"}), 200


    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error al imprimir el pago"}), 500
    finally:
        db_session.close()
        print("Conexión cerrada")


def obtener_pagoClienteTexto(db_session, nombre_cliente):


    # Obtener ID del cliente por nombre
    id_cliente = obtenerIdClientePorNombre(db_session, nombre_cliente)

    monto_pagoEspecial = obtener_pagoEspecial(db_session, id_cliente, datetime.datetime.now())
    print(monto_pagoEspecial)

    tasa_cambio = obtener_tasa_cambio_local()
    print(tasa_cambio)

    cifra_dolares = monto_pagoEspecial['cifra']

    cifra_cordobas = cifra_dolares * tasa_cambio['cifraTasaCambio']

    cadena_texto_respuesta = f"El cliente {nombre_cliente} tiene que pagar la cifra de {cifra_dolares} dólares, que al cambio serían {cifra_cordobas} córdobas."

    return cadena_texto_respuesta

### estado 3 = Ya se ha pagado el monto total de la quincena
### estado 2 = Pago quincenal
### estado 1  = El resto a pagar de la Primera quincena de julio de 2024




def crear_cadena_respuesta_cantidad_pago_cliente(db_session, nombre_cliente):

    print("Creando cadena de respuesta...")
    print(nombre_cliente)
    

    # Obtener ID del cliente por nombre
    id_cliente = seleccionar_clientes_activos(db_session, nombre_cliente)

    print(id_cliente)

    # Obtenemos los datos del contrato y del cliente meidante el ID del cliente
    id_contratoActual = obtener_IdContrato(db_session, id_cliente)

    datos_cliente = listar_datosClienteContratoCompleto(db_session, id_cliente)
    datos_contratoCliente = listarDatosContratoID_contrato(db_session, id_contratoActual)

    # 
    nombre_cliente = f"{datos_cliente[2]} {datos_cliente[3]}"

    pago_quincenal_dolares = datos_contratoCliente[10]
    pago_mensual_dolares = datos_contratoCliente[9]

    tasa_de_cambio = obtener_tasa_cambio_local()

    pago_quincenal_cordobas = pago_quincenal_dolares * tasa_de_cambio['cifraTasaCambio']
    pago_mensual_cordobas = pago_mensual_dolares * tasa_de_cambio['cifraTasaCambio']
    ### pago_quincena_cordobas haz que se aplique redondeo siempre que se encuentre decimales
    pago_quincenal_cordobas = math.ceil(pago_quincenal_cordobas)
    pago_mensual_cordobas = math.ceil(pago_mensual_cordobas)

    cadena_texto_respuesta = f"""{nombre_cliente} paga a la quincena {pago_quincenal_dolares} dólares, 
    que son unos {pago_quincenal_cordobas} córdobas, al mes, son {pago_mensual_dolares} dólares, 
    que en cordobas son {pago_mensual_cordobas}"""

    return cadena_texto_respuesta


def crear_cadena_respuesta_cantidad_de_clientes_pagados(db_session):
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
        PagosEstadosCortes = obtener_estadoPagoClienteCorte_real(db_session, listado[0], listado[4], listado[6], listado[5], datetime.datetime.now())
        clientePagoDict.update(PagosEstadosCortes)
        listado_clientesPagosDict.append(clientePagoDict)

    # Obtenemos la lista de clientes
    print(listado_clientesPagosDict)

    clientes_pagados = []

    for cliente in listado_clientesPagosDict:
        if cliente['estado'] == 1 or cliente['estado'] == 2:
            clientes_pagados.append(cliente)




    cantidad_clientes_pagados = len(clientes_pagados)
    nombre_clientes_pagados = [f"{cliente['nombres']} {cliente['apellidos']}" for cliente in clientes_pagados]

    if cantidad_clientes_pagados == 0:
        cadenena_texto_respuesta = "Según mis registros, no hay clientes que hayan pagado"
        return cadenena_texto_respuesta
    elif cantidad_clientes_pagados == 1:
        cadenena_texto_respuesta = f"""Segun mis registros es de {cantidad_clientes_pagados} cliente, el cual es: {nombre_clientes_pagados[0]}"""
        return cadenena_texto_respuesta
    elif cantidad_clientes_pagados > 1:
        cadenena_texto_respuesta = f"""Segun mis registros es de {cantidad_clientes_pagados} clientes,
        los cuales son: {nombre_clientes_pagados}"""
        return cadenena_texto_respuesta

    return cadenena_texto_respuesta



def crear_cadena_respuesta_cantidad_total_dinero_quincenal_clientes(db_session):
    listado_clientesPagosDict = []

    listado_clientesPagos = listar_cliesntesPagos(db_session)
    clientes_total = len(listado_clientesPagos)

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
        PagosEstadosCortes = obtener_estadoPagoClienteCorte_real(db_session, listado[0], listado[4], listado[6], listado[5], datetime.datetime.now())
        clientePagoDict.update(PagosEstadosCortes)
        listado_clientesPagosDict.append(clientePagoDict)



    clientes_pagados = []

    for cliente in listado_clientesPagosDict:
        if cliente['estado'] == 1 or cliente['estado'] == 2:
            # Obtenemos los datos del contrato y del cliente mediante el ID del cliente
            id_contratoActual = obtener_IdContrato(db_session, cliente['id_cliente'])

            # Obtener datos del ultimo pago
            ultimo_pago = ultimo_pago_contrato(db_session, id_contratoActual)

            cifra_pago_cliente = ultimo_pago[0][8]

            clientes_pagados.append({
                "nombres": cliente['nombres'],
                "apellidos": cliente['apellidos'],
                "Pago": cifra_pago_cliente,
            })

    print(clientes_pagados)

    cantidad_clientes_pagados = len(clientes_pagados)

    lista_clientes_con_pagos = [f"{i+1}. {cliente['nombres']} con {cliente['Pago']} dólares" for i, cliente in enumerate(clientes_pagados)]
    

    if cantidad_clientes_pagados == 0:
        cadenena_texto_respuesta = "No hay clientes que hayan pagado"
    elif cantidad_clientes_pagados == 1:

        suma_total_dinero_quincenal_dolares = sum([cliente['Pago'] for cliente in clientes_pagados])
        suma_total_dinero_quincenal_cordobas = math.ceil(suma_total_dinero_quincenal_dolares * obtener_tasa_cambio_local()['cifraTasaCambio'])


        cadenena_texto_respuesta = f""" Ha pagado solamente uno de {clientes_total} clientes. Con un total de {suma_total_dinero_quincenal_cordobas} córdobas. en dólares {suma_total_dinero_quincenal_dolares} dólares. """
    elif cantidad_clientes_pagados > 1:

        suma_total_dinero_quincenal_dolares = sum([cliente['Pago'] for cliente in clientes_pagados])
        suma_total_dinero_quincenal_cordobas = math.ceil(suma_total_dinero_quincenal_dolares * obtener_tasa_cambio_local()['cifraTasaCambio'])


        cadenena_texto_respuesta = f"""
        Han pagado {cantidad_clientes_pagados} de {clientes_total} clientes. que suman {suma_total_dinero_quincenal_cordobas} córdobas. en dólares {suma_total_dinero_quincenal_dolares} dólares."""

    return cadenena_texto_respuesta


def crear_cadena_respuesta_clientes_pagados(db_session):
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
            "pagoQuincenal": listado[6],
        }
        PagosEstadosCortes = obtener_estadoPagoClienteCorte_real(
            db_session,
            listado[0],
            listado[4],
            listado[6],
            listado[5],
            datetime.datetime.now(),
        )
        clientePagoDict.update(PagosEstadosCortes)
        listado_clientesPagosDict.append(clientePagoDict)

    print(listado_clientesPagosDict)

    clientes_pagados = [
        cliente
        for cliente in listado_clientesPagosDict
        if cliente["estado"] == 1 or cliente["estado"] == 2
    ]

    cantidad_clientes_pagados = len(clientes_pagados)
    nombre_clientes_pagados = [
        f"{cliente['nombres']} {cliente['apellidos']}" for cliente in clientes_pagados
    ]

    if cantidad_clientes_pagados == 0:
        cadena_texto_respuesta = "Según mis registros, no hay clientes que hayan pagado"
    elif cantidad_clientes_pagados == 1:
        cadena_texto_respuesta = (
            f"Según mis registros hay {cantidad_clientes_pagados} cliente, "
            f"el cual es: {nombre_clientes_pagados[0]}"
        )
    else:
        cadena_texto_respuesta = (
            f"Según mis registros hay {cantidad_clientes_pagados} clientes, "
            f"los cuales son: {', '.join(nombre_clientes_pagados)}"
        )

    respuesta = {
        "alexa_speak": cadena_texto_respuesta,
        "alexa_display": nombre_clientes_pagados,
    }
    return respuesta


def crear_cadena_respuesta_cantidad_total_dinero_quincenal_clientes(db_session):
    listado_clientesPagosDict = []

    listado_clientesPagos = listar_cliesntesPagos(db_session)
    clientes_total = len(listado_clientesPagos)

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
        PagosEstadosCortes = obtener_estadoPagoClienteCorte_real(db_session, listado[0], listado[4], listado[6], listado[5], datetime.datetime.now())
        clientePagoDict.update(PagosEstadosCortes)
        listado_clientesPagosDict.append(clientePagoDict)



    clientes_pagados = []

    for cliente in listado_clientesPagosDict:
        if cliente['estado'] == 1 or cliente['estado'] == 2:
            # Obtenemos los datos del contrato y del cliente mediante el ID del cliente
            id_contratoActual = obtener_IdContrato(db_session, cliente['id_cliente'])

            # Obtener datos del ultimo pago
            ultimo_pago = ultimo_pago_contrato(db_session, id_contratoActual)

            cifra_pago_cliente = ultimo_pago[0][8]

            clientes_pagados.append({
                "nombres": cliente['nombres'],
                "apellidos": cliente['apellidos'],
                "Pago": cifra_pago_cliente,
            })

    print(clientes_pagados)

    cantidad_clientes_pagados = len(clientes_pagados)

    lista_clientes_con_pagos = [f"{i+1}. {cliente['nombres']} con {cliente['Pago']} dólares" for i, cliente in enumerate(clientes_pagados)]
    

    if cantidad_clientes_pagados == 0:
        cadenena_texto_respuesta = "No hay clientes que hayan pagado"
    elif cantidad_clientes_pagados == 1:

        suma_total_dinero_quincenal_dolares = sum([cliente['Pago'] for cliente in clientes_pagados])
        suma_total_dinero_quincenal_cordobas = math.ceil(suma_total_dinero_quincenal_dolares * obtener_tasa_cambio_local()['cifraTasaCambio'])


        cadenena_texto_respuesta = f""" Ha pagado solamente uno de {clientes_total} clientes. Con un total de {suma_total_dinero_quincenal_cordobas} córdobas. en dólares {suma_total_dinero_quincenal_dolares} dólares. """
    elif cantidad_clientes_pagados > 1:

        suma_total_dinero_quincenal_dolares = sum([cliente['Pago'] for cliente in clientes_pagados])
        suma_total_dinero_quincenal_cordobas = math.ceil(suma_total_dinero_quincenal_dolares * obtener_tasa_cambio_local()['cifraTasaCambio'])


        cadenena_texto_respuesta = f"""
        Han pagado {cantidad_clientes_pagados} de {clientes_total} clientes. que suman {suma_total_dinero_quincenal_cordobas} córdobas. en dólares {suma_total_dinero_quincenal_dolares} dólares."""

    return cadenena_texto_respuesta




def crear_cadena_respuesta_obtener_pago_normal(db_session, nombre_cliente):

    print("Creando cadena de respuesta...")
    print(nombre_cliente)
    
    # Obtener ID del cliente por nombre
    id_cliente = seleccionar_clientes_activos(db_session, nombre_cliente)
    datos_cliente = seleccionar_datos_cliente(db_session, id_cliente)
    pago = obtener_pagoEspecial(db_session, id_cliente, datetime.datetime.now())

    if pago['estado'] == 2:
        nombres_apellidos_cliente = f"{datos_cliente[1]} {datos_cliente[2]}"
        pago['nombres_apellidos_cliente'] = nombres_apellidos_cliente
        pago['id_cliente'] = id_cliente
        pago['cifra_cordobas'] = pago['cifra'] * obtener_tasa_cambio_local()['cifraTasaCambio']
        pago['tasa_cambio'] = obtener_tasa_cambio_local()['cifraTasaCambio']
        # Additional processing for estado == 2

    # Convertir todos los Decimals a float
    for key, value in pago.items():
        if isinstance(value, Decimal):
            pago[key] = float(value)
            if key == 'cifra_cordobas':
                pago[key] = math.ceil(pago[key])

    print(pago)
    return pago