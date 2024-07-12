from models.clientes import *
from models.contratos import *
from models.constantes import *
from models.pagos import *
from db import *
from utils import *
from num2words import num2words



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
    

    # Obtener ID del cliente por nombre
    id_cliente = obtenerIdClientePorNombre(db_session, nombre_cliente)

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
    saldo_pendiente = num2words(datos_cliente['saldo_pendiente'][3], lang='es')

    #Extraer datos necesarios del ultimo pago
    cifra_ultimo_pago = num2words(ultimo_pago[0][8], lang='es')
    fecha_ultimo_pago = ultimo_pago[0][3]
    fecha_ultimo_pago_letras = ultimo_pago[0][15]

    str_pago = f"el último pago que tengo registrado es el {fecha_ultimo_pago} osea en la {fecha_ultimo_pago_letras} con un monto de {cifra_ultimo_pago} dólares"
    




    # Determinar el estado del pago y construir la respuesta
    if datos_cliente['estado_pago_corte'] == 1:
        estado_pago = "está al día con sus pagos"
    else:
        estado_pago = "no va al día"

    # Determinar si el cliente tiene saldo pendiente
    if datos_cliente['saldo_pendiente'][3] == 0:
        saldo_pendiente = "no tiene saldo pendiente"
    else:
        saldo_pendiente = f"tiene un saldo de {saldo_pendiente} dólares"

    respuesta_cadena_texto = f"A la {quincena_actual}, el cliente {nombres} {apellidos} {estado_pago} de hecho, {str_pago}  y  {saldo_pendiente}."

    # Imprimir la respuesta (opcional)
    print(respuesta_cadena_texto)

    return respuesta_cadena_texto






respuesta_cliente = crear_cadena_respuesta(db_session, "juan ramon")



