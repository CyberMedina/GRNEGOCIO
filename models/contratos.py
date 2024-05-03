from db import *
from utils import *
from models.constantes import *
from datetime import datetime, timedelta
from decimal import Decimal
import timeit

def listar_datosClienteContratoCompleto(db_session, id_cliente):
    try:
        query = text("""
        SELECT cl.id_cliente, p.id_persona, p.nombres, p.apellidos, p.cedula, p.fecha_nacimiento, p.genero,
d.direccion_escrita, d.direccion_mapa, d.nombre_direccion,
c.nombre_compania, t.nombre_telefono, t.numero_telefono,
cl.imagenCliente, cl.imagenCedula, cl.estado
FROM cliente cl
JOIN persona p ON cl.id_persona = p.id_persona
JOIN persona_direccion pd ON pd.id_persona = p.id_persona
JOIN direccion d ON d.id_direccion = pd.id_direccion
JOIN direccion_telefono dt ON dt.id_direccion = d.id_direccion
JOIN telefono t ON t.id_telefono = dt.id_telefono
JOIN companias_telefonicas c ON c.id_compania = t.id_compania
WHERE
cl.id_cliente = :id_cliente;
                     """)
        result = db_session.execute(
            query, {"id_cliente": id_cliente}).fetchone()

        return result
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def listarDatosContratoID_contrato(db_session, id_contrato):
    try:
        query = text("""
        SELECT c.id_contrato_fiador, c.id_cliente, c.estado_civil, c.nombre_delegacion, c.dptoArea_trabajo, c.ftoColillaINSS,
c.monto_solicitado, c.tipo_monedaMonto_solicitado, c.tasa_interes,
c.fechaPrestamo, c.fechaPago, c.montoPrimerPago
FROM contrato c
WHERE id_contrato = :id_contrato;
                     """)
        result = db_session.execute(
            query, {"id_contrato": id_contrato}).fetchone()

        return result
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()

def listarDatosFiadorContratoID_contratoFiador(db_session, id_contrato_fiador):
    try:
        query = text("""
SELECT cf.id_contrato_fiador, cf.id_cliente, cf.estado_civil, cf.nombre_delegacion,
cf.dptoArea_trabajo, cf.ftoColillaINSS, cf.estado
FROM contrato_fiador cf
WHERE cf.id_contrato_fiador = :id_contrato_fiador;""")
        result = db_session.execute(
            query, {"id_contrato_fiador": id_contrato_fiador}).fetchone()

        return result
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()

