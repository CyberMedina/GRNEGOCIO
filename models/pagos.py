from db import *
from utils import *
from models.constantes import *


def listar_cliesntesPagos(db_session):
    try:
        query = text("""SELECT cl.id_cliente, cl.id_tipoCliente, p.nombres, p.apellidos
FROM cliente cl
JOIN persona p ON cl.id_persona = p.id_persona
WHERE cl.estado = '1' AND
cl.id_tipoCliente = '2' OR
cl.id_tipoCliente = '3';
                     """
                     )
        result = db_session.execute(query).fetchall()
        return result
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def datos_pagov1(db_session, id_cliente):
    try:
        query = text("""

    SELECT 
    cl.id_cliente, 
    cl.id_tipoCliente, 
    p.nombres, 
    p.apellidos, 
    m.codigoMoneda,
    c.monto_solicitado, 
    c.tasa_interes, 
    c.pagoMensual, 
    c.pagoQuincenal, 
    DATE_FORMAT(c.fechaPrestamo, '%d de %M de %Y') AS fecha_prestamo_formato,
    tp.nombre_tipoCliente,
    CASE 
        WHEN TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()) < 1 THEN CONCAT(TIMESTAMPDIFF(MINUTE, c.fechaPrestamo, NOW()), ' minutos')
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) = 1 THEN 'hace ayer'
        WHEN TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()) < 24 THEN CONCAT(TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()), ' horas')
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) = 2 THEN 'hace 2 días'
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) < 30 THEN CONCAT(TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()), ' días')
        WHEN TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()) = 1 THEN 'hace 1 mes'
        WHEN TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()) < 12 THEN CONCAT(TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()), ' meses')
        WHEN TIMESTAMPDIFF(YEAR, c.fechaPrestamo, NOW()) = 1 THEN 'hace 1 año'
        ELSE CONCAT(TIMESTAMPDIFF(YEAR, c.fechaPrestamo, NOW()), ' años')
    END as fecha_prestamo_desde,
    CASE c.intervalo_tiempoPago
           WHEN 15 THEN 'Quincenal'
           WHEN 30 THEN 'Mensual'
           ELSE 'Desconocido' -- Manejar otros casos si es necesario
       END as tiempo_pago
FROM 
    cliente cl
JOIN 
    contrato c ON cl.id_cliente = c.id_cliente
JOIN 
    persona p ON cl.id_persona = p.id_persona
JOIN 
    moneda m ON c.tipo_monedaMonto_solicitado = m.id_moneda
JOIN
		tipo_cliente tp ON cl.id_tipoCliente = tp.id_tipoCliente
WHERE
    cl.id_cliente = :id_cliente;
                     """
                     )
        result = db_session.execute(
            query, {'id_cliente': id_cliente}).fetchall()

        # Convertir los resultados a una lista de diccionarios
        formatted_results = []
        for row in result:
            formatted_row = {
                'id_cliente': row[0],
                'id_tipoCliente': row[1],
                'nombres': row[2],
                'apellidos': row[3],
                'codigoMoneda': row[4],
                'monto_solicitado': row[5],
                'tasa_interes': row[6],
                'pagoMensual': row[7],
                'pagoQuincenal': row[8],
                'fechaPrestamo': row[9],
                'nombre_tipoCliente': row[10],
                'fecha_prestamo_desde': row[11],
                'tiempo_pago': row[12]
            }
            formatted_results.append(formatted_row)

        return formatted_results

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def datos_pagov2(id_cliente, db_session):

    try:
        query = text("""
SELECT 
    cl.id_cliente, 
    cl.id_tipoCliente,
    tp.nombre_tipoCliente,
    p.nombres, 
    p.apellidos, 
    m.codigoMoneda,
    c.intervalo_tiempoPago,
    c.monto_solicitado, 
    c.tasa_interes, 
    c.pagoMensual, 
    c.pagoQuincenal,
    c.fechaPrestamo,
    CASE 
        WHEN TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()) < 1 THEN CONCAT(TIMESTAMPDIFF(MINUTE, c.fechaPrestamo, NOW()), ' minutos')
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) = 1 THEN 'hace ayer'
        WHEN TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()) < 24 THEN CONCAT(TIMESTAMPDIFF(HOUR, c.fechaPrestamo, NOW()), ' horas')
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) = 2 THEN 'hace 2 días'
        WHEN TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()) < 30 THEN CONCAT(TIMESTAMPDIFF(DAY, c.fechaPrestamo, NOW()), ' días')
        WHEN TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()) = 1 THEN 'hace 1 mes'
        WHEN TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()) < 12 THEN CONCAT(TIMESTAMPDIFF(MONTH, c.fechaPrestamo, NOW()), ' meses')
        WHEN TIMESTAMPDIFF(YEAR, c.fechaPrestamo, NOW()) = 1 THEN 'hace 1 año'
        ELSE CONCAT(TIMESTAMPDIFF(YEAR, c.fechaPrestamo, NOW()), ' años')
    END as fecha_prestamo_desde,
    CASE c.intervalo_tiempoPago
           WHEN 15 THEN 'Quincenal'
           WHEN 30 THEN 'Mensual'
           ELSE 'Desconocido' -- Manejar otros casos si es necesario
       END as tiempo_pago
FROM 
    cliente cl
JOIN 
    contrato c ON cl.id_cliente = c.id_cliente
JOIN 
    persona p ON cl.id_persona = p.id_persona
JOIN 
    moneda m ON c.tipo_monedaMonto_solicitado = m.id_moneda
JOIN
		tipo_cliente tp ON cl.id_tipoCliente = tp.id_tipoCliente
WHERE
    cl.id_cliente = :id_cliente;"""

                     )
        result = db_session.execute(
            query, {'id_cliente': id_cliente}).fetchall()

        # Convertir los resultados a una lista de diccionarios
        formatted_results = []
        for row in result:
            formatted_row = {
                'id_cliente': row[0],
                'id_tipoCliente': row[1],
                'nombre_tipoCliente': row[2],
                'nombres': row[3],
                'apellidos': row[4],
                'codigoMoneda': row[5],
                'intervalo_tiempoPago': row[6],
                'monto_solicitado': row[7],
                'tasa_interes': row[8],
                'pagoMensual': row[9],
                'pagoQuincenal': row[10],
                'fechaPrestamo': row[11],
                'fecha_prestamo_desde': row[12],
                'tiempo_pago': row[13]
            }
            formatted_results.append(formatted_row)

        return formatted_results

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def obtener_IdContrato(db_session, id_cliente):
    try:
        query = text("""
                     SELECT id_contrato FROM contrato WHERE id_cliente = :id_cliente AND estado = :estado;
                     """
                     )
        result = db_session.execute(
            query, {'id_cliente': id_cliente, 'estado': activo}).fetchone()
        return result[0]
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def comprobar_primerPago(db_session, id_contrato):
    try:
        query = text("""
        SELECT COUNT(*) FROM pagos WHERE id_contrato = :id_contrato AND estado = :estado;""")
        result = db_session.execute(
            query, {'id_contrato': id_contrato, 'estado': activo}).fetchall()
        return result[0]

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def obtener_primerPago(db_session, id_contrato):
    try:
        query = text("""
        SELECT montoPrimerPago FROM contrato WHERE id_contrato = :id_contrato;""")
        result = db_session.execute(
            query, {'id_contrato': id_contrato}).fetchone()

        return result

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def insertarPago(db_session, id_contrato, observacion, evidencia_pago, fecha_pago, estado):
    try:
        # Obtener el ID de la tabla persona
        id_pagos = ObtenerIDTabla(db_session, "id_pagos", "pagos")

        # Insertar el pago
        query = text("""
                     INSERT INTO pagos (id_pagos, id_contrato, observacion, evidencia_pago, fecha_pago, fecha_realizacion_pago, estado)
                        VALUES (:id_pagos, :id_contrato, :observacion, :evidencia_pago, :fecha_pago, NOW(), :estado);
                        """
                        )
        db_session.execute(query, {'id_pagos': id_pagos, 'id_contrato': id_contrato, 'observacion': observacion, 'evidencia_pago': evidencia_pago, 'fecha_pago': fecha_pago, 'estado': estado})
        db_session.commit()
        return id_pagos

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()

def insertar_detalle_pagos(db_session, id_pagos, id_moneda, cifraPago, tasa_conversion, estado):
    try:
        # Obtener el ID de la tabla persona
        id_detalle_pagos = ObtenerIDTabla(db_session, "id_detalle_pagos", "detalle_pagos")

        # Insertar el pago
        query = text("""
                     INSERT INTO detalle_pagos (id_detalle_pagos, id_pagos, id_moneda, cifraPago, tasa_conversion, estado)
                        VALUES (:id_detalle_pagos, :id_pagos, :id_moneda, :cifraPago, :tasa_conversion, :estado);
                        """
                        )
        db_session.execute(query, {'id_detalle_pagos': id_detalle_pagos, 'id_pagos': id_pagos, 'id_moneda': id_moneda, 'cifraPago': cifraPago, 'tasa_conversion': tasa_conversion, 'estado': estado})
        db_session.commit()
        return id_detalle_pagos

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()





