from db import *
from utils import *

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