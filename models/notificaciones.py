from database_connection import *
from helpers import *

def insertarNotificacionPagoCliente(db_session, id_imagen, id_cliente, descripcion, monto_sugerido, estado):
    
    try:
        # Obtener el ID de la tabla persona
        id_notificacionesClientesPagos = (ObtenerIDTabla(db_session, "id_notificacionesClientesPagos", "notificacionesclientespagos"))
        
        query = text("""INSERT INTO notificacionesclientespagos(id_notificacionesClientesPagos, id_imagen, id_cliente, descripcion, monto_sugerido, fechaCreacionNotificacion, estado)
        VALUES (:id_notificacionesClientesPagos, :id_imagen, :id_cliente, :descripcion, :monto_sugerido, NOW(), :estado); """)
        
        db_session.execute(query, {
                                    "id_notificacionesClientesPagos": id_notificacionesClientesPagos,
                                    "id_imagen": id_imagen,
                                      "id_cliente": id_cliente,
                                        "descripcion": descripcion,
                                        "monto_sugerido": monto_sugerido,
                                           "estado": estado})
        
        
        return True
    
    except Exception as e:
        print(e)
        db_session.rollback()
        raise
    

def obtenerClientesChatNotificaciones(db_session):
    try:
        query = text(""" SELECT 
    ncp.id_notificacionesClientesPagos,
    ncp.fechaCreacionNotificacion,
    ncp.descripcion,
    ncp.monto_sugerido,
    p.nombres,
    p.apellidos,
    c.id_cliente,
    CASE
        WHEN TIMESTAMPDIFF(SECOND, ncp.fechaCreacionNotificacion, NOW()) < 60 
            THEN CONCAT(TIMESTAMPDIFF(SECOND, ncp.fechaCreacionNotificacion, NOW()), ' segundos')
        WHEN TIMESTAMPDIFF(MINUTE, ncp.fechaCreacionNotificacion, NOW()) < 60 
            THEN CONCAT(TIMESTAMPDIFF(MINUTE, ncp.fechaCreacionNotificacion, NOW()), ' minutos')
        WHEN TIMESTAMPDIFF(HOUR, ncp.fechaCreacionNotificacion, NOW()) < 24 
            THEN CONCAT(TIMESTAMPDIFF(HOUR, ncp.fechaCreacionNotificacion, NOW()), ' horas')
        WHEN TIMESTAMPDIFF(DAY, ncp.fechaCreacionNotificacion, NOW()) = 1 
            THEN '1 día'
        WHEN TIMESTAMPDIFF(DAY, ncp.fechaCreacionNotificacion, NOW()) < 7 
            THEN CONCAT(TIMESTAMPDIFF(DAY, ncp.fechaCreacionNotificacion, NOW()), ' días')
        WHEN TIMESTAMPDIFF(WEEK, ncp.fechaCreacionNotificacion, NOW()) = 1
            THEN '1 semana'
        WHEN TIMESTAMPDIFF(WEEK, ncp.fechaCreacionNotificacion, NOW()) < 4
            THEN CONCAT(TIMESTAMPDIFF(WEEK, ncp.fechaCreacionNotificacion, NOW()), ' semanas')
        WHEN TIMESTAMPDIFF(MONTH, ncp.fechaCreacionNotificacion, NOW()) = 1
            THEN '1 mes'
        WHEN TIMESTAMPDIFF(MONTH, ncp.fechaCreacionNotificacion, NOW()) < 12
            THEN CONCAT(TIMESTAMPDIFF(MONTH, ncp.fechaCreacionNotificacion, NOW()), ' meses')
        WHEN TIMESTAMPDIFF(YEAR, ncp.fechaCreacionNotificacion, NOW()) = 1
            THEN '1 año'
        ELSE 
            CONCAT(TIMESTAMPDIFF(YEAR, ncp.fechaCreacionNotificacion, NOW()), ' años')
    END AS tiempoTranscurrido
FROM notificacionesclientespagos AS ncp
INNER JOIN cliente AS c ON ncp.id_cliente = c.id_cliente
INNER JOIN persona AS p ON c.id_persona = p.id_persona
INNER JOIN (
    SELECT 
        id_cliente,
        MAX(fechaCreacionNotificacion) AS max_fecha
    FROM notificacionesclientespagos
    GROUP BY id_cliente
) AS ultimos ON ncp.id_cliente = ultimos.id_cliente
             AND ncp.fechaCreacionNotificacion = ultimos.max_fecha;""")
        
        return db_session.execute(query).fetchall()
    
    except Exception as e:
        print(e)
        db_session.rollback()
        raise
    

def obtener_todas_las_imagenes_de_un_cliente(db_session, id_cliente):
    try:
        query = text("""
SELECT 
    ncp.id_notificacionesClientesPagos,
    ncp.id_imagen,
    ncp.fechaCreacionNotificacion,
    ncp.descripcion,
    ncp.monto_sugerido,
    img.url_imagen,
    img.public_id,
    p.nombres,
    p.apellidos,
    CASE
        WHEN TIMESTAMPDIFF(SECOND, ncp.fechaCreacionNotificacion, NOW()) < 60 
            THEN CONCAT(TIMESTAMPDIFF(SECOND, ncp.fechaCreacionNotificacion, NOW()), ' segundos')
        WHEN TIMESTAMPDIFF(MINUTE, ncp.fechaCreacionNotificacion, NOW()) < 60 
            THEN CONCAT(TIMESTAMPDIFF(MINUTE, ncp.fechaCreacionNotificacion, NOW()), ' minutos')
        WHEN TIMESTAMPDIFF(HOUR, ncp.fechaCreacionNotificacion, NOW()) < 24 
            THEN CONCAT(TIMESTAMPDIFF(HOUR, ncp.fechaCreacionNotificacion, NOW()), ' horas')
        WHEN TIMESTAMPDIFF(DAY, ncp.fechaCreacionNotificacion, NOW()) = 1 
            THEN '1 día'
        WHEN TIMESTAMPDIFF(DAY, ncp.fechaCreacionNotificacion, NOW()) < 7 
            THEN CONCAT(TIMESTAMPDIFF(DAY, ncp.fechaCreacionNotificacion, NOW()), ' días')
        WHEN TIMESTAMPDIFF(WEEK, ncp.fechaCreacionNotificacion, NOW()) = 1
            THEN '1 semana'
        WHEN TIMESTAMPDIFF(WEEK, ncp.fechaCreacionNotificacion, NOW()) < 4
            THEN CONCAT(TIMESTAMPDIFF(WEEK, ncp.fechaCreacionNotificacion, NOW()), ' semanas')
        WHEN TIMESTAMPDIFF(MONTH, ncp.fechaCreacionNotificacion, NOW()) = 1
            THEN '1 mes'
        WHEN TIMESTAMPDIFF(MONTH, ncp.fechaCreacionNotificacion, NOW()) < 12
            THEN CONCAT(TIMESTAMPDIFF(MONTH, ncp.fechaCreacionNotificacion, NOW()), ' meses')
        WHEN TIMESTAMPDIFF(YEAR, ncp.fechaCreacionNotificacion, NOW()) = 1
            THEN '1 año'
        ELSE 
            CONCAT(TIMESTAMPDIFF(YEAR, ncp.fechaCreacionNotificacion, NOW()), ' años')
    END AS tiempoTranscurrido
FROM notificacionesclientespagos ncp
INNER JOIN imagenes img ON ncp.id_imagen = img.id_imagen
INNER JOIN cliente c ON ncp.id_cliente = c.id_cliente
INNER JOIN persona p ON c.id_persona = p.id_persona
WHERE c.id_cliente = :id_cliente """)
        
        result = db_session.execute(query, {"id_cliente": id_cliente}).fetchall()
        
        if result:
            # Crear una nueva lista para almacenar los resultados formateados
            formatted_result = []
            for row in result:
                formatted_result.append({
                    "id_notificacionesClientesPagos": row[0],
                    "id_imagen" : row[1],
                    "fechaCreacionNotificacion": row[2],
                    "fechaCreacionNotificacion_formateada": convertir_fecha_a_string_con_hora(row[2]),
                    "descripcion": row[3],  
                    "monto_sugerido": row[4],
                    "monto_sugerido_formateado": convertir_monto_a_string(row[4]),
                    "url_imagen": row[5],
                    "public_id": row[6],
                    "nombres": row[7],
                    "apellidos": row[8],
                    "tiempoTranscurrido": row[9]
                })
            return formatted_result
        else:
            return None

    except Exception as e:
        print(e)
        db_session.rollback()
        raise e


def eliminar_notificacionesClientesPagos(db_session, id_notificacionesClientesPagos):
    try:
        query = text("""
        DELETE FROM notificacionesclientespagos WHERE id_notificacionesClientesPagos = :id_notificacionesClientesPagos;
        """)
        db_session.execute(query, {"id_notificacionesClientesPagos": id_notificacionesClientesPagos})
        return True
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    

  

