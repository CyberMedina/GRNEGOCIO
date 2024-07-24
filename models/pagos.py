from flask import Flask, request, jsonify, Blueprint
from db import *
from utils import *
from models.constantes import *
from models.contratos import *
from datetime import datetime, timedelta
from decimal import Decimal
import timeit


def listar_cliesntesPagos(db_session):
    try:
        query = text("""SELECT cl.id_cliente, cl.id_tipoCliente, p.nombres, p.apellidos, c.id_contrato, c.pagoMensual, c.pagoQuincenal, cl.estado, c.estado
FROM cliente cl
JOIN persona p ON cl.id_persona = p.id_persona
JOIN contrato c ON cl.id_cliente = c.id_cliente
WHERE cl.estado = '1' 
AND c.estado = '1' 
AND (cl.id_tipoCliente = '2' OR cl.id_tipoCliente = '3');"""
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
    cl.id_cliente = :id_cliente
    AND
    c.estado = '1';
                     """)
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
    cl.id_cliente = :id_cliente
    AND 
    c.estado = :estado;"""

                     )
        result = db_session.execute(
            query, {'id_cliente': id_cliente, 'estado' : activo}).fetchall()

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


def calcular_pago_diario(pago_mensual, cantidad_dias):
    try:
        pago_diario = pago_mensual / cantidad_dias
        return pago_diario
    except ZeroDivisionError as e:
        print(f"Error: {e}")
        return None


def calcular_cifra_pago_quincenal(pago_diario, fecha_prestamo):
    try:
        if fecha_prestamo.day <= 15:
            cantidad_días = 15 - fecha_prestamo.day
            primer_pago = pago_diario * cantidad_días
        else:
            cantidad_días = mes_comercial - fecha_prestamo.day
            primer_pago = pago_diario * cantidad_días

        return primer_pago

    except Exception as e:
        print(f"Error: {e}")
        return None


def calcular_primerPago_quincenal(pago_mensual, fecha_prestamo):
    try:
        pago_diario = calcular_pago_diario(pago_mensual, mes_comercial)
        primer_pago = calcular_cifra_pago_quincenal(
            pago_diario, fecha_prestamo)
        return primer_pago
    except Exception as e:
        print(f"Error: {e}")
        return None





def comprobar_primerPago(db_session, id_cliente):
    try:
        query = text("""
        SELECT COUNT(*) 
FROM pagos p
JOIN contrato c ON p.id_contrato = c.id_contrato
        WHERE c.id_cliente = :id_cliente AND c.estado = :estado;""")
        result = db_session.execute(
            query, {'id_cliente': id_cliente, 'estado' :activo}).fetchall()
        print(result)
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
        db_session.execute(query, {'id_pagos': id_pagos, 'id_contrato': id_contrato, 'id_cliente': id_cliente,
                           'observacion': observacion, 'evidencia_pago': evidencia_pago, 'fecha_pago': fecha_pago, 'estado': estado})
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
        id_detalle_pagos = ObtenerIDTabla(
            db_session, "id_detalle_pagos", "detalle_pagos")

        # Insertar el pago
        query = text("""
                     INSERT INTO detalle_pagos (id_detalle_pagos, id_pagos, id_moneda, cifraPago, tasa_conversion, estado)
                        VALUES (:id_detalle_pagos, :id_pagos, :id_moneda, :cifraPago, :tasa_conversion, :estado);
                        """
                     )
        db_session.execute(query, {'id_detalle_pagos': id_detalle_pagos, 'id_pagos': id_pagos,
                           'id_moneda': id_moneda, 'cifraPago': cifraPago, 'tasa_conversion': tasa_conversion, 'estado': estado})
        db_session.commit()
        return id_detalle_pagos

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


# def pagos_por_contrato(db_session, id_cliente, añoInicio, añoFin, estado_contrato, estado_detalle_pago):
    
#     try:
#         query = text(""" SELECT 
#     p.id_pagos,
#     p.observacion, 
#     p.evidencia_pago, 
#     p.fecha_pago, 
#     p.fecha_realizacion_pago,
#     p.estado AS estado_pago, 
#     m.codigoMoneda, 
#     m.nombreMoneda, 
#     dp.cifraPago, 
#     dp.tasa_conversion,
#     dp.estado AS estado_detalle_pago,
#     CASE 
#         WHEN DAY(p.fecha_pago) <= 15 THEN CONCAT('Primera quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
#         ELSE CONCAT('Segunda quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
#     END AS descripcion_quincena,
#     MONTH(p.fecha_pago) AS id_mes, -- Agregando la columna id_mes
#     c.estado
# FROM 
#     pagos p
# JOIN 
#     detalle_pagos dp ON p.id_pagos = dp.id_pagos
# JOIN 
#     moneda m ON dp.id_moneda = m.id_moneda
# JOIN 
#     contrato c ON p.id_contrato = c.id_contrato
# WHERE 
#     p.id_cliente = :id_cliente 
#     AND p.fecha_pago BETWEEN :añoInicio AND :añoFin 
#     AND c.estado = :estado_contrato 
#     AND dp.estado = :estado_detalle_pago
# ORDER BY 
#     p.fecha_pago, p.id_pagos ASC;
# """)

#         result = db_session.execute(query, {'id_cliente': id_cliente, 'añoInicio': añoInicio, 'añoFin': añoFin,
#                                     'estado_contrato': estado_contrato, "estado_detalle_pago": estado_detalle_pago}).fetchall()
#         return result

#     except SQLAlchemyError as e:
#         db_session.rollback()
#         print(f"Error: {e}")
#         return None
#     finally:
#         db_session.close()

def pagos_por_contrato(db_session, id_cliente, añoInicio, añoFin, estado_contrato, estado_detalle_pago):
    try:
        query = text(""" 
        SELECT
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
            c.id_contrato,
            c.monto_solicitado,
            c.fechaPrestamo,
            c.estado as estado_contrato,
            
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
            p.id_cliente = :id_cliente 
            AND p.fecha_pago BETWEEN :añoInicio AND :añoFin 
            AND dp.estado = :estado_detalle_pago
        ORDER BY 
            p.fecha_pago, p.id_pagos ASC;
        """)

        result = db_session.execute(query, {'id_cliente': id_cliente, 'añoInicio': añoInicio, 'añoFin': añoFin,
                                            "estado_detalle_pago": estado_detalle_pago}).fetchall()
        
        new_result = []
        last_id_contrato = None
        for row in result:
            row_tuple = tuple(row)
            if row_tuple[0] != last_id_contrato:
                new_row = row_tuple + (1,)
                last_id_contrato = row_tuple[0]
            else:
                new_row = row_tuple + (None,)
            new_result.append(new_row)
        return result


    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def ultimo_pago_contrato(db_session, id_cliente):
    try:
        query = text(""" 
        SELECT
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
            c.id_contrato,
            c.monto_solicitado,
            c.fechaPrestamo,
            c.estado as estado_contrato,
            
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
            p.id_cliente = :id_cliente 
            AND p.estado = :estado_detalle_pago1 OR p.estado = :estado_detalle_pago2
        ORDER BY 
            p.fecha_pago DESC
        LIMIT 1;
        """)

        result = db_session.execute(query, {'id_cliente': id_cliente, "estado_detalle_pago1": pago_completo, 'estado_detalle_pago2': pago_incompleto}).fetchall()
        
        new_result = []
        last_id_contrato = None
        for row in result:
            row_tuple = tuple(row)
            if row_tuple[0] != last_id_contrato:
                new_row = row_tuple + (1,)
                last_id_contrato = row_tuple[0]
            else:
                new_row = row_tuple + (None,)
            new_result.append(new_row)
        return result


    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()



def transacciones_saldo_contrato(db_session, id_cliente, añoInicio, añoFin, estado_contrato, estado_detalle_pago, tipo_consulta, suma_saldo):
    try:
        query = text("""
                     SELECT ts.id_moneda, ts.monto, ts.tipo_transaccion, ts.fecha_transaccion, p.fecha_pago,
    CASE 
        WHEN DAY(p.fecha_pago) <= 15 THEN CONCAT('Primera quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
        ELSE CONCAT('Segunda quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
    END AS descripcion_quincena,
    MONTH(p.fecha_pago) AS id_mes -- Se eliminó la coma aquí
FROM transacciones_saldos ts
INNER JOIN detalle_pagos dp ON ts.id_pagos = dp.id_pagos
INNER JOIN pagos p ON dp.id_pagos = p.id_pagos
INNER JOIN contrato c ON p.id_contrato = c.id_contrato
WHERE p.id_cliente = :id_cliente
AND p.fecha_pago BETWEEN :añoInicio AND :añoFin
AND c.estado = :estado_contrato
AND dp.estado = :estado_detalle_pago;
""")
        result = db_session.execute(query, {'id_cliente': id_cliente, 'añoInicio': añoInicio, 'añoFin': añoFin,
                                    'estado_contrato': estado_contrato, 'estado_detalle_pago': estado_detalle_pago}).fetchall()
        
        if tipo_consulta == consulta_normal:

            result_list = []
            cifra_anterior = 0
            total_cifra = 0
            primer_elemento = True


            for row in result:
                if primer_elemento:
                    print("primero entro acá")
                    total_cifra = row[1] - abs(suma_saldo)
                    cifra_anterior = total_cifra
                    print(f"{row[1]} - {abs(suma_saldo)} = {total_cifra}")
                    primer_elemento = False
                else:
                    print("En el segundo registro entró acá")
                    if row[2] == Aumento:
                        total_cifra = cifra_anterior + abs(row[1])
                        print(f"{cifra_anterior} + {abs(row[1])}  ")
                        cifra_anterior = total_cifra
                        print(f"La NUEVA cifra anterior es: {cifra_anterior}")

                    else:
                        total_cifra = cifra_anterior - abs(row[1])
                        print(f"{cifra_anterior} - {abs(row[1])} = {total_cifra}")
                        cifra_anterior = total_cifra
                        print(f"La NUEVA cifra anterior es: {cifra_anterior}")
                result_dict = {
                    'id_moneda': row[0],
                    'monto': row[1],
                    'tipo_transaccion': row[2],
                    'fecha_transaccion': row[3],
                    'fecha_pago': row[4],
                    'descripcion_quincena': row[5],
                    'id_mes': row[6],
                    'sumatoria': total_cifra,
                }
              
                result_list.append(result_dict)




            return result_list
        elif tipo_consulta == consulta_sumatoria_total:
            cifra_anterior = 0
            total_cifra = 0
            primer_elemento = True

            for row in result:
                if primer_elemento:
                    print("primero entro acá")
                    cifra_anterior = row[1]
                    print(cifra_anterior)
                    primer_elemento = False
                else:
                    print("En el segundo registro entró acá")
                    if row[2] == Aumento:
                        total_cifra = cifra_anterior + abs(row[1])
                        print(f"{cifra_anterior} + {abs(row[1])}  ")
                        cifra_anterior = total_cifra
                        print(f"La NUEVA cifra anterior es: {cifra_anterior}")

                    else:
                        total_cifra = cifra_anterior - abs(row[1])
                        print(f"{cifra_anterior} - {abs(row[1])} = {total_cifra}")
                        cifra_anterior = total_cifra
                        print(f"La NUEVA cifra anterior es: {cifra_anterior}")




            print(f"La suma total es: {total_cifra}")
            return total_cifra




        



    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


# def obtener_años_pagos(db_session, id_cliente, estado):
#     try:
#         query = text("""SELECT YEAR(p.fecha_pago) AS años 
#                      FROM pagos p
#                      JOIN contrato c ON p.id_contrato = c.id_contrato 
#                      WHERE p.id_cliente = :id_cliente AND c.estado = :estado
# GROUP BY YEAR(fecha_pago)
# ORDER BY YEAR(fecha_pago) DESC;""")
#         result = db_session.execute(
#             query, {'id_cliente': id_cliente, 'estado': estado}).fetchall()

#         return result

#     except SQLAlchemyError as e:
#         db_session.rollback()
#         print(f"Error: {e}")
#         return None
#     finally:
#         db_session.close()

def obtener_años_pagos(db_session, id_cliente, estado):
    try:
        query = text("""SELECT YEAR(p.fecha_pago) AS años 
                     FROM pagos p
                     JOIN contrato c ON p.id_contrato = c.id_contrato 
                     WHERE p.id_cliente = :id_cliente
GROUP BY YEAR(fecha_pago)
ORDER BY YEAR(fecha_pago) DESC;""")
        result = db_session.execute(
            query, {'id_cliente': id_cliente}).fetchall()

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
    else:  # Si el día del mes es mayor que 15, es la segunda quincena
        # Obtener el último día del mes
        ultimo_dia_mes = fecha_actual.replace(
            day=1, month=fecha_actual.month+1) - timedelta(days=1)
        inicio_quincena = fecha_actual.replace(day=16)
        fin_quincena = ultimo_dia_mes

    inicio_quincena_str = inicio_quincena.strftime('%Y-%m-%d')
    fin_quincena_str = fin_quincena.strftime('%Y-%m-%d')

    return inicio_quincena_str, fin_quincena_str


def validacion_fechaPago_quincena(db_session, id_contrato, fechaPagoQuincena_inicio, fechaPagoQuincena_final, estadoMoneda):
    try:
        query = text("""
                     SELECT SUM(cifraPago) 
FROM detalle_pagos dp 
JOIN pagos p ON dp.id_pagos = p.id_pagos 
WHERE id_contrato = :id_contrato 
AND fecha_pago BETWEEN :fechaPagoQuincena_inicio AND :fechaPagoQuincena_final 
AND dp.estado = :estadoMoneda
AND (p.estado = :estadoPago1 OR p.estado = :estadoPago2 OR p.estado = :estadoPago3);""")

        result = db_session.execute(query, {'id_contrato': id_contrato, 'fechaPagoQuincena_inicio': fechaPagoQuincena_inicio,
                                    'fechaPagoQuincena_final': fechaPagoQuincena_final, 'estadoMoneda': estadoMoneda, 'estadoPago1': pago_completo, 'estadoPago2': pago_incompleto, 'estadoPago3': pago_de_mas}).fetchone()
        return result[0]

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()

# Esta función es utilizada para verificar si el cliente ha pagado el monto total de la quincena en el caso que sea el primer pago


def validacion_primer_pago_quincena(db_session, id_contrato, fechaPagoQuincena_inicio, fechaPagoQuincena_final, estadoMoneda):
    try:
        query = text("""
                     SELECT *
FROM detalle_pagos dp 
JOIN pagos p ON dp.id_pagos = p.id_pagos 
WHERE id_contrato = :id_contrato 
AND fecha_pago BETWEEN :fechaPagoQuincena_inicio AND :fechaPagoQuincena_final 
AND dp.estado = :estadoMoneda
AND p.estado = :estadoPago1;""")

        result = db_session.execute(query, {'id_contrato': id_contrato, 'fechaPagoQuincena_inicio': fechaPagoQuincena_inicio,
                                    'fechaPagoQuincena_final': fechaPagoQuincena_final, 'estadoMoneda': estadoMoneda, 'estadoPago1': primer_pago_del_prestamo}).fetchone()
        if result is None:
            return None
        else:
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
    p.id_cliente, 
    p.id_pagos,
    p.observacion, 
    p.evidencia_pago, 
    p.fecha_pago, 
    p.fecha_realizacion_pago,
    p.estado AS 'estado_pagos', 
    m.codigoMoneda, 
    m.nombreMoneda, 
    dp.cifraPago, 
    dp.tasa_conversion, 
    dp.estado AS 'estado_detallePagos',
    CASE 
        WHEN DAY(p.fecha_pago) <= 15 THEN CONCAT('Primera quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
        ELSE CONCAT('Segunda quincena de ', MONTHNAME(p.fecha_pago), ' de ', YEAR(p.fecha_pago))
    END AS descripcion_quincena,
    MONTH(p.fecha_pago) AS id_mes, -- Agregando la columna id_mes
    c.estado AS 'estado_contrato'
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

        if len(result) == 1:
            print("Solo hay un registro")
            # Solo hay un registro
            row = result[0]
            result_list = {
                'id_cliente': row[0],
                'id_pagos': row[1],
                'observacion': row[2],
                'evidencia_pago': row[3],
                'fecha_pago': row[4],
                'fecha_realizacion_pago': row[5],
                'estado_pagos': row[6],
                'codigoMoneda': row[7],
                'nombreMoneda': row[8],
                'cifraPago': row[9],
                'tasa_conversion': row[10],
                'estado_detallePagos': row[11],
                'descripcion_quincena': row[12],
                'id_mes': row[13],
                'estado_contrato': row[14],
            }
        elif len(result) == 2:
            # Hay dos registros
            row1 = result[0]
            row2 = result[1]
            result_list = {
                'id_cliente': row1[0],
                'id_pagos': row1[1],
                'observacion': row1[2],
                'evidencia_pago': row1[3],
                'fecha_pago': row1[4],
                'fecha_realizacion_pago': row1[5],
                'estado_pagos': row1[6],
                'codigoMoneda': row1[7],
                'nombreMoneda': row1[8],
                'cifraPago$': row1[9],
                'cifraPagoC$': row2[9],
                'tasa_conversion': row2[10],
            }

        return result_list

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def obtener_estado_pago(db_session, id_pagos):
    try:
        query = text(
            """SELECT estado FROM pagos WHERE id_pagos = :id_pagos;""")
        result = db_session.execute(query, {'id_pagos': id_pagos}).fetchone()
        return result[0]
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def obtener_saldo_con_id_cliente(db_session, id_cliente):
    try:
        query = text("""SELECT m.nombreMoneda, m.codigoMoneda, sp.cifraSaldo
FROM saldos_pagos sp
JOIN moneda m ON m.id_moneda = sp.id_moneda
JOIN cliente c ON c.id_cliente = sp.id_cliente
WHERE c.id_cliente = :id_cliente;""")
        result = db_session.execute(
            query, {'id_cliente': id_cliente}).fetchone()
        return result
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def obtener_tipo_saldo(db_session, id_cliente):
    try:
        query = text(
            """SELECT id_tipoSaldos_pagos FROM saldos_pagos WHERE id_cliente = :id_cliente;""")
        result = db_session.execute(
            query, {'id_cliente': id_cliente}).fetchone()
        return result[0]
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def obtener_saldos_pagos(db_session, id_cliente):
    try:
        query = text(
            """SELECT * from saldos_pagos WHERE id_cliente = :id_cliente;""")
        result = db_session.execute(
            query, {'id_cliente': id_cliente}).fetchall()
        if result:
            return result
        return None
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def obtener_cifraSaldo_anterior(db_session, id_pagos, id_cliente):
    try:

        query = text("""SELECT ts.monto, ts.tipo_transaccion 
FROM transacciones_saldos ts
JOIN saldos_pagos sp ON sp.id_saldos_pagos = ts.id_saldos_pagos
JOIN pagos p ON p.id_cliente = sp.id_cliente
WHERE p.id_pagos = :id_pagos
ORDER BY ts.fecha_transaccion DESC  -- Suponiendo que tienes una columna fecha_transaccion
LIMIT 1;
""")
        ultima_transaccion_saldo = db_session.execute(
            query, {'id_pagos': id_pagos}).fetchone()
        print(f"La ultima transaccion es" + str(ultima_transaccion_saldo))

        if ultima_transaccion_saldo:
            saldo_actual = obtener_saldo_con_id_cliente(db_session, id_cliente)

            if "Aumento" in ultima_transaccion_saldo[1]:
                monto_anterior = saldo_actual[2] - ultima_transaccion_saldo[0]
            elif "Disminucion" in ultima_transaccion_saldo[1]:
                if saldo_actual[2] < 0:
                    monto_anterior = abs(
                        saldo_actual[2]) + ultima_transaccion_saldo[0]
                    if monto_anterior > 0:
                        monto_anterior = -monto_anterior
                else:
                    monto_anterior = saldo_actual[2] + \
                        abs(ultima_transaccion_saldo[0])

            # Validando que no sean negativos los saldos
            # if monto_anterior < 0:
            #     monto_anterior = 0.00
        else:
            monto_anterior = 0.00

        return monto_anterior

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def buscar_id_cliente_con_id_pagos(db_session, id_pagos):
    try:
        query = text(
            """SELECT id_cliente FROM pagos WHERE id_pagos = :id_pagos;""")
        result = db_session.execute(query, {'id_pagos': id_pagos}).fetchone()
        return result[0]
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def eliminar_pago_idPagos(db_session, id_pagos, estado_pago):
    try:

        # Si el estado del pago es "No hay pago", se debe eliminar el registro de la tabla transacciones_saldos
        # y actualizar el saldo en contra

        if estado_pago == no_hay_pago or estado_pago == pago_de_mas or estado_pago == primer_pago_del_prestamo:


            eliminar_con_saldo = True

            if estado_pago == primer_pago_del_prestamo:

                eliminar_con_saldo = False

                id_contrato = seleccionar_idContrato_con_idPago(db_session, id_pagos)

                primer_pago_contrato = obtener_primerPago(db_session, id_contrato)[0]

                resultado_buscar_detalle_pago_idPagos = buscar_detalle_pago_idPagos(db_session, id_pagos)
                if "cifraPago$" in resultado_buscar_detalle_pago_idPagos:
                    cifra_primer_pago_seleccionado = resultado_buscar_detalle_pago_idPagos["cifraPago$"]
                elif "cifraPago" in resultado_buscar_detalle_pago_idPagos:
                    cifra_primer_pago_seleccionado = resultado_buscar_detalle_pago_idPagos["cifraPago"]
                else:
                    cifra_primer_pago_seleccionado = None  # o algún valor por defecto

                if cifra_primer_pago_seleccionado > primer_pago_contrato:
                    print("Entró en la eliminación primer pago porque es pago de más!")
                    eliminar_con_saldo = True

            if eliminar_con_saldo == True:
                id_cliente = buscar_id_cliente_con_id_pagos(db_session, id_pagos)
                print(f"el id del cliente es" + str(id_cliente))

                cifra_anterior = obtener_cifraSaldo_anterior(
                    db_session, id_pagos, id_cliente)
                print(f"la cifra anterior es" + str(cifra_anterior))

                actualizar_saldo(db_session, id_cliente, cifra_anterior, activo)

                query = text(
                    """DELETE FROM transacciones_saldos WHERE id_pagos = :id_pagos;""")
                db_session.execute(query, {'id_pagos': id_pagos})
                db_session.commit()

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


def validar_que_tipo_salo_es(db_session, id_cliente):
    try:
        query = text("""SELECT id_tipoSaldos_pagos
FROM saldos_pagos
WHERE id_cliente = :id_cliente
  AND cifraSaldo > 0;
""")
        result = db_session.execute(
            query, {'id_cliente': id_cliente}).fetchone()
        if result is None:
            return None
        return result
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()

# Esta función recupera el saldo en contra de un cliente


def validar_saldo_pendiente_en_contra(db_sesssion, id_cliente):

    result_saldo = validar_que_tipo_salo_es(db_sesssion, id_cliente)

    if result_saldo:
        id_tipoSaldos_pagos = result_saldo[1]
        print("existe un saldo")
        if id_tipoSaldos_pagos == saldo_en_contra:
            estado = saldo_en_contra
            print("el saldo es en contra")
        elif id_tipoSaldos_pagos == saldo_a_favor:
            print("el saldo es a favor")
            estado = saldo_a_favor

        try:
            query = text("""SELECT sp.id_saldos_pagos, m.nombreMoneda, m.codigoMoneda, sp.cifraSaldo, sp.estado
FROM saldos_pagos sp
JOIN moneda m ON m.id_moneda = sp.id_moneda
JOIN cliente c ON c.id_cliente = sp.id_cliente
WHERE id_tipoSaldos_pagos = :estado AND c.id_cliente = :id_cliente;""")
            result = db_sesssion.execute(
                query, {'id_cliente': id_cliente, 'estado': estado}).fetchone()
            return result
        except SQLAlchemyError as e:
            db_sesssion.rollback()
            print(f"Error: {e}")
            return None
        finally:
            db_sesssion.close()
    else:
        return None


# Esta función recupera el saldo en contra de un cliente
def validar_existencia_saldo_frontEnd(db_sesssion, id_cliente):

    try:
        query = text("""SELECT sp.id_saldos_pagos, m.nombreMoneda, m.codigoMoneda, ABS(sp.cifraSaldo) as cifraSaldo,
CASE 
    WHEN sp.cifraSaldo >= 0 THEN 1
    ELSE 2
END as estado
FROM saldos_pagos sp
JOIN moneda m ON m.id_moneda = sp.id_moneda
JOIN cliente c ON c.id_cliente = sp.id_cliente
WHERE c.id_cliente = :id_cliente;""")

        result = db_sesssion.execute(
            query, {'id_cliente': id_cliente}).fetchone()
        if result:
            return result
        else:
            return None
    except SQLAlchemyError as e:
        db_sesssion.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_sesssion.close()

# Esta función recupera el saldo en contra de un cliente


def validar_existencia_saldo(db_sesssion, id_cliente):

    try:
        query = text("""SELECT sp.id_saldos_pagos, m.nombreMoneda, m.codigoMoneda, sp.cifraSaldo, sp.estado
FROM saldos_pagos sp
JOIN moneda m ON m.id_moneda = sp.id_moneda
JOIN cliente c ON c.id_cliente = sp.id_cliente
WHERE c.id_cliente = :id_cliente;""")
        result = db_sesssion.execute(
            query, {'id_cliente': id_cliente}).fetchone()
        if result:
            return result
        else:
            return None
    except SQLAlchemyError as e:
        db_sesssion.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_sesssion.close()


# Esta función recupera el saldo a favor de un cliente
def validar_saldo_pendiente_a_favor(db_sesssion, id_cliente):
    try:
        query = text("""SELECT sp.id_saldos_pagos, m.nombreMoneda, m.codigoMoneda, sp.cifraSaldo 
FROM saldos_pagos sp
JOIN moneda m ON m.id_moneda = sp.id_moneda
JOIN cliente c ON c.id_cliente = sp.id_cliente
WHERE id_tipoSaldos_pagos = :estado AND c.id_cliente = :id_cliente;""")
        result = db_sesssion.execute(
            query, {'id_cliente': id_cliente, 'estado': saldo_a_favor}).fetchone()
        if result is None:
            return None
        return result
    except SQLAlchemyError as e:
        db_sesssion.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_sesssion.close()


def actualizar_saldo(db_session, id_cliente, cifraSaldo, estado):
    try:
        query = text(
            """UPDATE saldos_pagos SET cifraSaldo = :cifraSaldo, fecha_saldo = NOW(), estado = :estado WHERE id_cliente = :id_cliente;""")
        db_session.execute(query, {
                           'cifraSaldo': cifraSaldo, 'estado': estado, 'id_cliente': id_cliente})
        db_session.commit()
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db_session.close()


def ingreso_saldo(db_session, id_cliente, id_pagos, tipo_saldo, id_moneda, cifraSaldo, estado):

    saldos_pagos = validar_existencia_saldo(db_session, id_cliente)

    if saldos_pagos is None:
        try:
            print("No existe la tabla saldo para este cliente, creando!")
            # Obtener el ID de la tabla persona
            id_saldos_pagos = (ObtenerIDTabla(
                db_session, "id_saldos_pagos", "saldos_pagos"))

            # Insertar el pago
            query = text("""
                        INSERT INTO saldos_pagos (id_saldos_pagos, id_cliente, id_moneda, cifraSaldo, fecha_saldo, estado)
                            VALUES (:id_saldos_pagos, :id_cliente, :id_moneda, :cifraSaldo, NOW(), :estado);
                            """
                         )
            db_session.execute(query, {'id_saldos_pagos': id_saldos_pagos, 'id_cliente': id_cliente,
                               'id_moneda': id_moneda, 'cifraSaldo': cifraSaldo, 'estado': estado})
            db_session.commit()
            return id_saldos_pagos

        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {e}")
            return None
        finally:
            db_session.close()

    elif saldos_pagos[3] == 0.00:
        try:

            actualizar_saldo(
                db_session, id_cliente, cifraSaldo, estado)

            return saldos_pagos[0]
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {e}")
            return None
        finally:
            db_session.close()
    # Procedimiento para incrementar el saldo
    elif tipo_saldo == saldo_en_contra:
        try:
            print("El saldo es en contra")
            cifraSaldoAnterior = Decimal(saldos_pagos[3])
            print(f"La cifra anterior es" + str(cifraSaldoAnterior))
            cifraSaldoNueva = Decimal(cifraSaldoAnterior + Decimal(cifraSaldo))
            print
            print(f"La cifra nueva es" + str(cifraSaldoNueva))

            actualizar_saldo(
                db_session, id_cliente, cifraSaldoNueva, estado)
            return saldos_pagos[0]

        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {e}")
            return None
        finally:
            db_session.close()
    # Procedimiento para reducir el saldo
    elif tipo_saldo == saldo_a_favor:
        try:
            print("Es saldo a favor")
            cifraSaldoAnterior = Decimal(saldos_pagos[3])
            print(f'saldo anterior es' + str(cifraSaldoAnterior))
            cifraSaldoNueva = Decimal(cifraSaldoAnterior + Decimal(cifraSaldo))
            print("El saldo nuevo es" + str(cifraSaldoNueva))
            actualizar_saldo(
                db_session, id_cliente, cifraSaldoNueva, estado)
            return saldos_pagos[0]

        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {e}")
            return None
        finally:
            db_session.close()


# def añadir_saldo_en_contra(db_session, id_cliente, id_tipoSaldos_pagos, id_moneda, cifraSaldo, estado):

#     saldos_pagos = validar_saldo_pendiente_en_contra(db_session, id_cliente)

#     if saldos_pagos is None:
#         try:
#             # Obtener el ID de la tabla persona
#             id_saldos_pagos = (ObtenerIDTabla(
#                 db_session, "id_saldos_pagos", "saldos_pagos"))

#             # Insertar el pago
#             query = text("""
#                         INSERT INTO saldos_pagos (id_saldos_pagos, id_cliente, id_tipoSaldos_pagos, id_moneda, cifraSaldo, fecha_saldo, estado)
#                             VALUES (:id_saldos_pagos, :id_cliente, :id_tipoSaldos_pagos, :id_moneda, :cifraSaldo, NOW(), :estado);
#                             """
#                          )
#             db_session.execute(query, {'id_saldos_pagos': id_saldos_pagos, 'id_cliente': id_cliente, 'id_tipoSaldos_pagos': id_tipoSaldos_pagos,
#                                'id_moneda': id_moneda, 'cifraSaldo': cifraSaldo, 'estado': estado})
#             db_session.commit()
#             return id_saldos_pagos

#         except SQLAlchemyError as e:
#             db_session.rollback()
#             print(f"Error: {e}")
#             return None
#         finally:
#             db_session.close()

#     elif saldos_pagos[3] == 0.00:
#         try:

#             actualizar_saldo(
#                 db_session, id_cliente, id_tipoSaldos_pagos, cifraSaldo, estado)

#             return saldos_pagos[0]
#         except SQLAlchemyError as e:
#             db_session.rollback()
#             print(f"Error: {e}")
#             return None
#         finally:
#             db_session.close()
#     # Procedimiento para incrementar el saldo
#     else:
#         try:
#             cifraSaldoAnterior = Decimal(saldos_pagos[3])
#             cifraSaldoNueva = Decimal(cifraSaldoAnterior + Decimal(cifraSaldo))
#             actualizar_saldo(
#                 db_session, id_cliente, id_tipoSaldos_pagos, cifraSaldoNueva, estado)
#             return saldos_pagos[0]

#         except SQLAlchemyError as e:
#             db_session.rollback()
#             print(f"Error: {e}")
#             return None
#         finally:
#             db_session.close()


# def reducir_saldo_en_contra(db_session, id_cliente, id_pagos, id_tipoSaldos_pagos, id_moneda, diferencia_pago, estado):

#     # Si el id_tipoSadlos_pago es proporcionado, se debe utilizar ese valor
#     # De lo cont

#     print("El id_tipoSaldos_pagos es" + str(id_tipoSaldos_pagos))


#     result_saldos = obtener_saldos_pagos(db_session, id_cliente)
#     print(result_saldos)


#     saldos_pagos = validar_saldo_pendiente_en_contra(db_session, id_cliente)
#     print(saldos_pagos)
#     saldos_a_favor = validar_saldo_pendiente_a_favor(db_session, id_cliente)
#     print(saldos_a_favor)

#     if result_saldos is None:
#         try:

#             estado = id_tipoSaldos_pagos
#             print("Entró cuando no hay saldo")
#             print(estado)
#             # Obtener el ID de la tabla persona
#             id_saldos_pagos = (ObtenerIDTabla(
#                 db_session, "id_saldos_pagos", "saldos_pagos"))

#             # Insertar el pago
#             query = text("""
#                         INSERT INTO saldos_pagos (id_saldos_pagos, id_cliente, id_tipoSaldos_pagos, id_moneda, cifraSaldo, fecha_saldo, estado)
#                             VALUES (:id_saldos_pagos, :id_cliente, :id_tipoSaldos_pagos, :id_moneda, :cifraSaldo, NOW(), :estado);
#                             """
#                          )
#             db_session.execute(query, {'id_saldos_pagos': id_saldos_pagos, 'id_cliente': id_cliente, 'id_tipoSaldos_pagos': id_tipoSaldos_pagos,
#                                'id_moneda': id_moneda, 'cifraSaldo': diferencia_pago, 'estado': activo})
#             db_session.commit()


#         except SQLAlchemyError as e:
#             db_session.rollback()
#             print(f"Error: {e}")
#             return None
#         finally:
#             db_session.close()
#     elif saldos_a_favor:
#         print("Entró cuando hay saldo a favor")
#         print(saldos_a_favor[3])
#         if saldos_a_favor[3] == 0.00:
#             try:


#                 print("diferencia pago" + str(diferencia_pago))
#                 print("id_tipoSaldos_pagos::::::::::: " + str(id_tipoSaldos_pagos))

#                 actualizar_saldo(
#                     db_session, id_cliente, id_tipoSaldos_pagos, diferencia_pago, estado)

#                 id_saldos_pagos = saldos_a_favor[0]


#             except SQLAlchemyError as e:
#                 db_session.rollback()
#                 print(f"Error: {e}")
#                 return None
#             finally:
#                 db_session.close()
#         # Procedimiento para disminuir el saldo en contra
#         elif saldos_a_favor[3] > 0.00:
#             try:
#                 print("Entró por acá")
#                 cifraSaldoAnterior = Decimal(saldos_a_favor[3])
#                 print(cifraSaldoAnterior)
#                 cifraSaldoNueva = Decimal(cifraSaldoAnterior + Decimal(diferencia_pago))
#                 actualizar_saldo(
#                     db_session, id_cliente, id_tipoSaldos_pagos, cifraSaldoNueva, estado)
#                 id_saldos_pagos = saldos_a_favor[0]


#             except SQLAlchemyError as e:
#                 db_session.rollback()
#                 print(f"Error: {e}")
#                 return None
#             finally:
#                 db_session.close()
#     else:
#         try:
#             print("Entró en el peor de los casos")
#             estado = saldo_en_contra
#             cifraSaldoAnterior = Decimal(saldos_pagos[3])
#             cifraSaldoNueva = Decimal(cifraSaldoAnterior - Decimal(diferencia_pago))
#             actualizar_saldo(
#                 db_session, id_cliente, id_tipoSaldos_pagos, cifraSaldoNueva, estado)

#             id_saldos_pagos = saldos_pagos[0]


#         except SQLAlchemyError as e:
#             db_session.rollback()
#             print(f"Error: {e}")
#             return None
#         finally:
#             db_session.close()


#     insertar_transaccion_saldo(db_session, id_saldos_pagos, id_pagos, id_moneda, diferencia_pago, estado)


#     return id_saldos_pagos


def insertar_transaccion_saldo(db_session, id_saldos_pagos, id_pagos, id_moneda, monto, tipo_transaccion):
    try:
        # Obtener el ID de la tabla persona
        id_transaccion_saldo = ObtenerIDTabla(
            db_session, "id_transaccion", "transacciones_saldos")

        # Insertar el pago
        query = text("""
                     INSERT INTO transacciones_saldos (id_transaccion, id_saldos_pagos, id_pagos, id_moneda, monto, tipo_transaccion, fecha_transaccion)
                        VALUES (:id_transaccion_saldo, :id_saldos_pagos, :id_pagos, :id_moneda, :monto, :tipo_transaccion, NOW());
                        """
                     )
        db_session.execute(query, {'id_transaccion_saldo': id_transaccion_saldo, 'id_saldos_pagos': id_saldos_pagos,
                           'id_pagos': id_pagos, 'id_moneda': id_moneda, 'monto': monto, 'tipo_transaccion': tipo_transaccion})
        db_session.commit()
        return id_transaccion_saldo

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def obtener_pagoEspecial(db_session, id_cliente, fecha):

    

    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, '%Y-%m-%d')

    id_contrato = obtener_IdContrato(db_session, id_cliente)

    num_pagos = comprobar_primerPago(db_session, id_contrato)

    pagos_cliente = datos_pagov2(id_cliente, db_session)

    if num_pagos[0] == 0:
        monto_primerPago_consulta = obtener_primerPago(db_session, id_contrato)
        monto_pagoEspecial = monto_primerPago_consulta[0]

        # monto_primerPago = calcular_primerPago_quincenal(monto_primerPago_consulta[9], monto_primerPago_consulta[11])
        monto_pago = {
            'cifra': monto_pagoEspecial,
            'estado': 0,
            'descripcion': 'Primer pago'
        }
    else:
        # si hay más de un pago

        dia_mes = fecha.day

        inicio_quincena, fin_quincena = obtener_quincena_actual(fecha, dia_mes)

        existencia_primer_pago = validacion_primer_pago_quincena(
            db_session, id_contrato, inicio_quincena, fin_quincena, monedaOriginal)

        sumPagosQuincena = validacion_fechaPago_quincena(
            db_session, id_contrato, inicio_quincena, fin_quincena, monedaOriginal)

        quincenaLetras, mesLetras, anioLetras = obtener_quincenaActual_letras(
            fecha)

        # Validamos que el cliente haya pagado el monto total de la quincena en su primer pago
        if existencia_primer_pago:
            monto_pagoEspecial = '0.00'
            monto_pago = {
                'cifra': monto_pagoEspecial,
                'estado': 1,
                'descripcion': f'Ya se ha pagado el monto total de la quincena porque el primer pago del préstamo fue abonado'
            }
        # Si el cliente no ha pagado el monto total de la quincena se musetra la cifra a pagar
        elif sumPagosQuincena:
            if sumPagosQuincena >= pagos_cliente[0]['pagoQuincenal']:
                monto_pagoEspecial = '0.00'
                monto_pago = {
                    'cifra': monto_pagoEspecial,
                    'estado': 3,
                    'descripcion': 'Ya se ha pagado el monto total de la quincena'
                }
            else:
                monto_pagoEspecial = pagos_cliente[0]['pagoQuincenal'] - \
                    sumPagosQuincena
                monto_pago = {
                    'cifra': monto_pagoEspecial,
                    'estado': 1,
                    'descripcion': f'El resto a pagar de la {quincenaLetras} quincena de {mesLetras} de {anioLetras}'
                }
        # Como solo hay 1 un pago, quiere decir que es el pago especial el que está registrado, por ende no se debe de cobrar intereses
        else:
            monto_pagoEspecial = pagos_cliente[0]['pagoQuincenal']
            monto_pago = {
                'cifra': monto_pagoEspecial,
                'estado': 2,
                'descripcion': 'Pago quincenal'
            }

    return monto_pago


def obtener_pagoEspecial(db_session, id_cliente, fecha):

    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
    print(fecha)

    id_contrato = obtener_IdContrato(db_session, id_cliente)

    num_pagos = comprobar_primerPago(db_session, id_cliente)

    pagos_cliente = datos_pagov2(id_cliente, db_session)

    if num_pagos[0] == 0:
        monto_primerPago_consulta = obtener_primerPago(db_session, id_contrato)
        monto_pagoEspecial = monto_primerPago_consulta[0]

        # monto_primerPago = calcular_primerPago_quincenal(monto_primerPago_consulta[9], monto_primerPago_consulta[11])
        monto_pago = {
            'cifra': monto_pagoEspecial,
            'estado': 0,
            'descripcion': 'Primer pago'
        }
    else:
        # si hay más de un pago

        dia_mes = fecha.day

        inicio_quincena, fin_quincena = obtener_quincena_actual(fecha, dia_mes)

        existencia_primer_pago = validacion_primer_pago_quincena(
            db_session, id_contrato, inicio_quincena, fin_quincena, monedaOriginal)

        sumPagosQuincena = validacion_fechaPago_quincena(
            db_session, id_contrato, inicio_quincena, fin_quincena, monedaOriginal)

        quincenaLetras, mesLetras, anioLetras = obtener_quincenaActual_letras(
            fecha)

        # Validamos que el cliente haya pagado el monto total de la quincena en su primer pago
        if existencia_primer_pago:
            monto_pagoEspecial = '0.00'
            monto_pago = {
                'cifra': monto_pagoEspecial,
                'estado': 1,
                'descripcion': f'Ya se ha pagado el monto total de la quincena porque el primer pago del préstamo fue abonado'
            }
        # Si el cliente no ha pagado el monto total de la quincena se musetra la cifra a pagar
        elif sumPagosQuincena:
            if sumPagosQuincena >= pagos_cliente[0]['pagoQuincenal']:
                monto_pagoEspecial = '0.00'
                monto_pago = {
                    'cifra': monto_pagoEspecial,
                    'estado': 3,
                    'descripcion': 'Ya se ha pagado el monto total de la quincena'
                }
            else:
                monto_pagoEspecial = pagos_cliente[0]['pagoQuincenal'] - \
                    sumPagosQuincena
                monto_pago = {
                    'cifra': monto_pagoEspecial,
                    'estado': 1,
                    'descripcion': f'El resto a pagar de la {quincenaLetras} quincena de {mesLetras} de {anioLetras}'
                }
        # Como solo hay 1 un pago, quiere decir que es el pago especial el que está registrado, por ende no se debe de cobrar intereses
        else:
            monto_pagoEspecial = pagos_cliente[0]['pagoQuincenal']
            monto_pago = {
                'cifra': monto_pagoEspecial,
                'estado': 2,
                'descripcion': 'Pago quincenal'
            }

    return monto_pago



def obtener_estadoPagoClienteCorte(db_session, id_cliente, id_contrato, pago_quincenal, pago_mensual, fecha):

    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
    print(fecha)
    print(id_contrato)
    print(id_cliente)
    num_pagos = comprobar_primerPago(db_session, id_cliente)
    print(num_pagos)

    if num_pagos[0] == 0:
        monto_primerPago_consulta = obtener_primerPago(db_session, id_contrato)
        monto_pagoEspecial = monto_primerPago_consulta[0]

        # monto_primerPago = calcular_primerPago_quincenal(monto_primerPago_consulta[9], monto_primerPago_consulta[11])
        estadoPagoCorte = {
            'cifra': monto_pagoEspecial,
            'estado': no_hay_pago,
            'descripcion': 'Primer pago'
        }
    else:
        # si hay más de un pago

        dia_mes = fecha.day

        inicio_quincena, fin_quincena = obtener_quincena_actual(fecha, dia_mes)

        existencia_primer_pago = validacion_primer_pago_quincena(
            db_session, id_contrato, inicio_quincena, fin_quincena, monedaOriginal)

        sumPagosQuincena = validacion_fechaPago_quincena(
            db_session, id_contrato, inicio_quincena, fin_quincena, monedaOriginal)

        quincenaLetras, mesLetras, anioLetras = obtener_quincenaActual_letras(
            fecha)

        # Validamos que el cliente haya pagado el monto total de la quincena en su primer pago
        if existencia_primer_pago:
            monto_pagoEspecial = '0.00'
            estadoPagoCorte = {
                'cifra': monto_pagoEspecial,
                'estado': pago_completo,
                'descripcion': f'Ya se ha pagado el monto total de la quincena porque el primer pago del préstamo fue abonado'
            }
        # Si el cliente no ha pagado el monto total de la quincena se musetra la cifra a pagar
        elif sumPagosQuincena:
            if sumPagosQuincena >= pago_quincenal:
                monto_pagoEspecial = '0.00'
                estadoPagoCorte = {
                    'cifra': monto_pagoEspecial,
                    'estado': pago_completo,
                    'descripcion': 'Ya se ha pagado el monto total de la quincena'
                }
            else:
                monto_pagoEspecial = pago_quincenal - \
                    sumPagosQuincena
                estadoPagoCorte = {
                    'cifra': monto_pagoEspecial,
                    'estado': pago_incompleto,
                    'descripcion': f'El resto a pagar de la {quincenaLetras} quincena de {mesLetras} de {anioLetras}'
                }
        # Como solo hay 1 un pago, quiere decir que es el pago especial el que está registrado, por ende no se debe de cobrar intereses
        else:
            monto_pagoEspecial = pago_quincenal
            estadoPagoCorte = {
                'cifra': monto_pagoEspecial,
                'estado': no_hay_pago,
                'descripcion': 'Pago quincenal'
            }

    return estadoPagoCorte


def obtener_diferencia_a_saldo(cantidadPago, monto_pago_quincenal):

    # Convertir a float si es string
    if isinstance(cantidadPago, str):
        cantidadPago = float(cantidadPago)
    if isinstance(monto_pago_quincenal, str):
        monto_pago_quincenal = float(monto_pago_quincenal)
    elif isinstance(monto_pago_quincenal, Decimal):
        monto_pago_quincenal = float(monto_pago_quincenal)

    if cantidadPago > monto_pago_quincenal:
        diferencia_a_saldo = cantidadPago - monto_pago_quincenal
    else:
        diferencia_a_saldo = None

    return diferencia_a_saldo

def verificar_pago(db_session, id_cliente, id_moneda, cantidadPagarDolares, estadoPago, cantidadPagarCordobas, fechaPago, tipoPagoCompletoForm):
    try:
        datos_cliente = datos_pagov2(id_cliente, db_session)
        verificacion_tipo_pago_insertar = {}

        id_moneda = int(id_moneda)

        if cantidadPagarCordobas:
            cantidadPagarCordobas_conversion = convertir_string_a_decimal(cantidadPagarCordobas)
        else:
            cantidadPagarCordobas_conversion = 0.00

        resultado_pago_fecha = obtener_pagoEspecial(db_session, id_cliente, fechaPago)
        cifra_a_pagar = resultado_pago_fecha['cifra']
        diferencia_pago_a_saldo = obtener_diferencia_a_saldo(cantidadPagarDolares, cifra_a_pagar)
        print(f'la diferencia del pago a saldo es: {diferencia_pago_a_saldo}')

        if estadoPago == 0 or estadoPago == 4:
            cantidadPagarDolaresNegativo = cantidadPagarDolares * -1
        else:
            cantidadPagarDolaresNegativo = 0

        verificacion_tipo_pago_insertar = {
            "nombres_apellidos": f"{datos_cliente[0]['nombres']} {datos_cliente[0]['apellidos']}",
            "cantidadPagarDolares": cantidadPagarDolares,
            "cantidadPagarDolaresNegativo": cantidadPagarDolaresNegativo,
            "estadoPago": estadoPago,
            "id_moneda": id_moneda,
            "cantidadPagarCordobas_conversion": cantidadPagarCordobas_conversion,
        }

        if diferencia_pago_a_saldo is not None and diferencia_pago_a_saldo > 0:
            verificacion_tipo_pago_insertar["cantidadPagarDolares"] = diferencia_pago_a_saldo

        print(verificacion_tipo_pago_insertar)

        return jsonify(verificacion_tipo_pago_insertar), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error al verificar el pago"}), 500
    


                



def proceder_pago(db_session, procesar_todo, id_cliente, id_moneda, cantidadPagarDolares, estadoPago, cantidadPagarCordobas, 
                fechaPago, tipoPagoCompletoForm, observacionPago, evidenciaPago, inputTasaCambioPago, 
                monedaConversion):
    

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
        print("Procesar todo esta en " + str(procesar_todo))
        if procesar_todo == True:
        
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
        
        db_session.commit()

        return jsonify({"message": "Pago realizado exitosamente"}), 200
    

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": "Error en la base de datos"}), 500

    except Exception as e:
        db_session.rollback()
        print(f"Error: {e}")
        return jsonify({"message": "Error en el servidor"}), 500
    

def eliminar_todos_pagos_por_idCliente(db_session, id_cliente):
    try:
        query = text("""
                     DELETE FROM pagos WHERE id_cliente = :id_cliente;
                     """
                     )
        db_session.execute(query, {'id_cliente': id_cliente})
        db_session.commit()
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db_session.close()

def eliminar_todos_detalles_pagos_por_idCliente(db_session, id_cliente):
    try:
        query = text("""
                     DELETE FROM detalle_pagos WHERE id_pagos IN (SELECT id_pagos FROM pagos WHERE id_cliente = :id_cliente);
                     """
                     )
        db_session.execute(query, {'id_cliente': id_cliente})
        db_session.commit()
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db_session.close()

def eliminar_todos_transacciones_saldos_por_idCliente(db_session, id_cliente):
    try:
        query = text("""
                     DELETE FROM transacciones_saldos WHERE id_saldos_pagos IN (SELECT id_saldos_pagos FROM saldos_pagos WHERE id_cliente = :id_cliente);
                     """
                     )
        db_session.execute(query, {'id_cliente': id_cliente})
        db_session.commit()
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db_session.close()

def eliminar_todos_saldos_pagos_por_idCliente(db_session, id_cliente):
    try:
        query = text("""
                     DELETE FROM saldos_pagos WHERE id_cliente = :id_cliente;
                     """
                     )
        db_session.execute(query, {'id_cliente': id_cliente})
        db_session.commit()
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db_session.close()

   
def seleccionar_idContrato_con_idPago(db_session, id_pago):
    try:

        query = text("""
SELECT id_contrato FROM pagos
WHERE id_pagos = :id_pago;""")
        
        result = db_session.execute(query, {'id_pago': id_pago}).fetchone()
        if result:
            return result[0]
        else:
            return None
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()




