from db import *
from utils import *
from models.constantes import *
from datetime import datetime, timedelta


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


def comprobar_primerPago(db_session, id_contrato, estado):
    try:
        query = text("""
        SELECT COUNT(*) FROM pagos WHERE id_contrato = :id_contrato AND estado = :estado;""")
        result = db_session.execute(
            query, {'id_contrato': id_contrato, 'estado': estado}).fetchall()
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


def insertarPago(db_session, id_contrato, id_cliente, observacion, evidencia_pago, fecha_pago, estado):
    try:
        # Obtener el ID de la tabla persona
        id_pagos = ObtenerIDTabla(db_session, "id_pagos", "pagos")

        # Insertar el pago
        query = text("""
                     INSERT INTO pagos (id_pagos, id_contrato, id_cliente, observacion, evidencia_pago, fecha_pago, fecha_realizacion_pago, estado)
                        VALUES (:id_pagos, :id_contrato, :id_cliente, :observacion, :evidencia_pago, :fecha_pago, NOW(), :estado);
                        """
                        )
        db_session.execute(query, {'id_pagos': id_pagos, 'id_contrato': id_contrato, 'id_cliente':id_cliente, 'observacion': observacion, 'evidencia_pago': evidencia_pago, 'fecha_pago': fecha_pago, 'estado': estado})
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





def pagos_por_contrato(db_session, id_cliente, año, estado_contrato, estado_detalle_pago):
    try:
        query = text(""" SELECT 
    p.id_pagos,
    p.observacion, 
    p.evidencia_pago, 
    p.fecha_pago, 
    p.fecha_realizacion_pago,
    p.estado AS estado_pago, 
    m.codigoMoneda, 
    m.nombreMoneda, 
    dp.cifraPago, 
    dp.tasa_conversion,
    dp.estado AS estado_detalle_pago,
    CASE 
        WHEN DAY(p.fecha_pago) <= 15 THEN CONCAT('Primera quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
        ELSE CONCAT('Segunda quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
    END AS descripcion_quincena,
    MONTH(p.fecha_pago) AS id_mes, -- Agregando la columna id_mes
    c.estado
FROM 
    pagos p
JOIN 
    detalle_pagos dp ON p.id_pagos = dp.id_pagos
JOIN 
    moneda m ON dp.id_moneda = m.id_moneda
JOIN 
    contrato c ON p.id_contrato = c.id_contrato
WHERE 
    p.id_cliente = :id_cliente AND YEAR(p.fecha_pago) = :año AND c.estado = :estado_contrato AND dp.estado = :estado_detalle_pago
ORDER BY 
    p.fecha_pago, p.id_pagos ASC;
""")
        
        result = db_session.execute(query, {'id_cliente': id_cliente, 'año': año, 'estado_contrato':estado_contrato, "estado_detalle_pago": estado_detalle_pago}).fetchall()
        print(result)

        return result
    
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def obtener_años_pagos(db_session, id_cliente, estado):
    try:
        query = text("""SELECT YEAR(p.fecha_pago) AS años 
                     FROM pagos p
                     JOIN contrato c ON p.id_contrato = c.id_contrato 
                     WHERE p.id_cliente = :id_cliente AND c.estado = :estado
GROUP BY YEAR(fecha_pago)
ORDER BY YEAR(fecha_pago) DESC;""")
        result = db_session.execute(query, {'id_cliente': id_cliente, 'estado':estado}).fetchall()

        for años in result:
            print(años[0])

        return result
    
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()



def obtener_quincena_actual(fecha_actual, dia_mes):

    # Si el día del mes es menor o igual a 15, es la primera quincena
    if dia_mes <= 15:
        inicio_quincena = fecha_actual.replace(day=1)
        fin_quincena = fecha_actual.replace(day=15)
    else: # Si el día del mes es mayor que 15, es la segunda quincena
        # Obtener el último día del mes
        ultimo_dia_mes = fecha_actual.replace(day=1, month=fecha_actual.month+1) - timedelta(days=1)
        inicio_quincena = fecha_actual.replace(day=16)
        fin_quincena = ultimo_dia_mes

    inicio_quincena_str = inicio_quincena.strftime('%Y-%m-%d')
    fin_quincena_str = fin_quincena.strftime('%Y-%m-%d')

    return inicio_quincena_str, fin_quincena_str

def validacion_fechaPago_quincena(db_session, id_contrato, fechaPagoQuincena_inicio, fechaPagoQuincena_final, estado):
    try:
        query = text("""
                     SELECT SUM(cifraPago) 
FROM detalle_pagos dp 
JOIN pagos p ON dp.id_pagos = p.id_pagos 
WHERE id_contrato = :id_contrato 
AND fecha_pago BETWEEN :fechaPagoQuincena_inicio AND :fechaPagoQuincena_final 
AND dp.estado = :estado;""")
        
        result = db_session.execute(query, {'id_contrato': id_contrato, 'fechaPagoQuincena_inicio': fechaPagoQuincena_inicio, 'fechaPagoQuincena_final': fechaPagoQuincena_final, 'estado': estado}).fetchone()
        return result[0]
        
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def determinar_quincena(date):
    if date.day <= 15:
        return 1
    else:
        return 2
    

def buscar_detalle_pago_idPagos(db_session, id_pagos):
    try:
        query = text("""SELECT 
    p.id_pagos,
    p.observacion, 
    p.evidencia_pago, 
    p.fecha_pago, 
    p.fecha_realizacion_pago, 
    m.codigoMoneda, 
    m.nombreMoneda, 
    dp.cifraPago, 
    dp.tasa_conversion, 
    dp.estado,
    CASE 
        WHEN DAY(p.fecha_pago) <= 15 THEN CONCAT('Primera quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
        ELSE CONCAT('Segunda quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
    END AS descripcion_quincena,
    MONTH(p.fecha_pago) AS id_mes, -- Agregando la columna id_mes
    c.estado
FROM 
    pagos p
JOIN 
    detalle_pagos dp ON p.id_pagos = dp.id_pagos
JOIN 
    moneda m ON dp.id_moneda = m.id_moneda
JOIN 
    contrato c ON p.id_contrato = c.id_contrato
WHERE 
    p.id_pagos = :id_pagos""")
        
        result = db_session.execute(query, {'id_pagos': id_pagos}).fetchall()

        result_list = []

        for row in result:
            result_dict = {
                'id_pagos': row[0],
                'observacion': row[1],
                'evidencia_pago': row[2],
                'fecha_pago': row[3],
                'fecha_realizacion_pago': row[4],
                'codigoMoneda': row[5],
                'nombreMoneda': row[6],
                'cifraPago': row[7],
                'tasa_conversion': row[8],
                'estado': row[9],
                'descripcion_quincena': row[10],
                'id_mes': row[11],
                'estado_contrato': row[12]
            }
            result_list.append(result_dict)

        return result_list
    
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()

                     

def eliminar_pago_idPagos(db_session, id_pagos):
    try:
        # Eliminar primero los registros de la tabla detalle_pagos relacionados con el pago
        query_detalle = text("""
                            DELETE FROM detalle_pagos WHERE id_pagos = :id_pagos;
                            """
                            )
        db_session.execute(query_detalle, {'id_pagos': id_pagos})
        
        # Luego, eliminar el registro principal de la tabla pagos
        query_pago = text("""
                         DELETE FROM pagos WHERE id_pagos = :id_pagos;
                         """
                         )
        db_session.execute(query_pago, {'id_pagos': id_pagos})
        
        db_session.commit()
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db_session.close()

def añadir_saldo_en_contra(db_session, id_tipoSaldos_pagos, id_moneda, cifraSaldo, fecha_saldo, estado):
    try:
        # Obtener el ID de la tabla persona
        id_saldos_pagos = ObtenerIDTabla(db_session, "id_saldos_pagos", "saldos_pagos")

        # Insertar el pago
        query = text("""
                     INSERT INTO saldos_pagos (id_saldos_pagos, id_tipoSaldos_pagos, id_moneda, cifraSaldo, fecha_saldo, estado)
                        VALUES (:id_saldos_pagos, :id_tipoSaldos_pagos, :id_moneda, :cifraSaldo, :fecha_saldo, :estado);
                        """
                        )
        db_session.execute(query, {'id_saldos_pagos': id_saldos_pagos, 'id_tipoSaldos_pagos': id_tipoSaldos_pagos, 'id_moneda': id_moneda, 'cifraSaldo': cifraSaldo, 'fecha_saldo': fecha_saldo, 'estado': estado})
        db_session.commit()
        return id_saldos_pagos

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()