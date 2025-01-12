from db import *
from utils import *

def insertarNotificacionPagoCliente(db_session, id_imagen, id_cliente, descripcion, monto_sugerido, estado):
    
    try:
        # Obtener el ID de la tabla persona
        id_notificacionesClientesPagos = (ObtenerIDTabla(db_session, "id_notificacionesClientesPagos", "notificacionesClientesPagos"))
        
        query = text("""INSERT INTO notificacionesClientesPagos(id_notificacionesClientesPagos, id_imagen, id_cliente, descripcion, monto_sugerido, fechaCreacionNotificacion, estado)
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