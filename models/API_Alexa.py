from flask import jsonify, render_template
from models.clientes import *
from models.contratos import *
from models.constantes import *
from models.pagos import *
from db import *
from utils import *
from num2words import num2words
from fuzzywuzzy  import process, fuzz



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

        # Crear una lista de nombres completos y sus respectivos clientes
        names = [f"{person['nombres']} {person['apellidos']}".lower() for person in results]
        print(names)
        name_to_person = {f"{person['nombres']} {person['apellidos']}".lower(): person for person in results}
        
        # Buscar coincidencias difusas
        matches = process.extract(search_term.lower(), names, limit=3, scorer=fuzz.token_set_ratio)
        print(matches)

        # Filtrar resultados para encontrar la mejor coincidencia
        best_match = None
        highest_score = 0
        for match in matches:
            if match[1] > highest_score and match[1] > 60:  # 60 es el umbral para la coincidencia difusa
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
    

def obtenerDatosClienteporID(db_session, id_cliente):

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
        "estado_pago_corte" : obtener_estadoPagoClienteCorte(db_session, id_cliente, id_contrato, pagos_cliente[0]["pagoQuincenal"], pagos_cliente[0]["pagoMensual"], datetime.now()),
    }


    return formulario_añadir_pago

def crear_cadena_respuesta(db_session, nombre_cliente):

    print("Creando cadena de respuesta...")
    print(nombre_cliente)
    

    # Obtener ID del cliente por nombre
    id_cliente = seleccionar_clientes_activos(db_session, nombre_cliente)

    # Obtener datos del cliente por ID
    datos_cliente = obtenerDatosClienteporID(db_session, id_cliente)

    # Obtener datos del ultimo pago
    ultimo_pago = ultimo_pago_contrato(db_session, id_cliente)


    # Obtener la quincena actual
    quincena, mes, anio = obtener_quincenaActual_letras(datetime.now())
    quincena_actual = f"{quincena} quincena de {mes} de {anio}"

    # Extraer datos necesarios del cliente
    nombres = datos_cliente['datos_cliente'][0]['nombres']
    apellidos = datos_cliente['datos_cliente'][0]['apellidos']


    #Extraer datos necesarios del ultimo pago
    cifra_ultimo_pago = num2words(ultimo_pago[0][8], lang='es')
    fecha_ultimo_pago = ultimo_pago[0][3]
    fecha_ultimo_pago_letras = ultimo_pago[0][15]

    str_pago = f"el último pago que tengo registrado es el {fecha_ultimo_pago}, osea en la {fecha_ultimo_pago_letras}, con un monto de {cifra_ultimo_pago} dólares"
    


    print(datos_cliente['estado_pago_corte'])

    # Determinar el estado del pago y construir la respuesta
    if datos_cliente['estado_pago_corte']['estado'] == 1:
        estado_pago = "está al día con sus pagos"
    else:
        estado_pago = "no va al día"

    # Determinar si el cliente tiene saldo pendiente
    if datos_cliente['saldo_pendiente'] is not None and datos_cliente['saldo_pendiente'][3] is not None:
        saldo_pendiente = num2words(datos_cliente['saldo_pendiente'][3], lang='es')
        saldo_pendiente = f"tiene un saldo de {saldo_pendiente} dólares"
        
    else:
        saldo_pendiente = "no tiene saldo pendiente"


    respuesta_cadena_texto = f"A la {quincena_actual}, el cliente {nombres} {apellidos} {estado_pago}, de hecho {str_pago}  y,  {saldo_pendiente}."

    # Imprimir la respuesta (opcional)
    print(respuesta_cadena_texto)

    return respuesta_cadena_texto




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






