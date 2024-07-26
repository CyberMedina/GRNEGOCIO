from db import *
from utils import *
from models.constantes import *
from datetime import datetime, timedelta
from decimal import Decimal
import timeit


def listarContratos_comboBox(db_session, id_cliente):
    try:
        query = text("""
        SELECT id_contrato, id_cliente
        FROM contrato
        WHERE estado = 1;
        """)
        result = db_session.execute(query).fetchall()

        return result
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def listar_datosClienteContratoCompleto(db_session, id_cliente):
    try:
        query = text("""
        SELECT cl.id_cliente, p.id_persona, p.nombres, p.apellidos, p.cedula, p.fecha_nacimiento, p.genero,
            d.direccion_escrita, d.direccion_mapa, d.nombre_direccion,
            c.nombre_compania, t.nombre_telefono, t.numero_telefono, tc.nombre_tipoCliente,
            cl.imagenCliente, cl.imagenCedula, cl.estado
        FROM cliente cl
            JOIN tipo_cliente tc ON cl.id_tipoCliente = tc.id_tipoCliente
            JOIN persona p ON cl.id_persona = p.id_persona
            JOIN persona_direccion pd ON pd.id_persona = p.id_persona
            JOIN direccion d ON d.id_direccion = pd.id_direccion
            JOIN direccion_telefono dt ON dt.id_direccion = d.id_direccion
            JOIN telefono t ON t.id_telefono = dt.id_telefono
            JOIN companias_telefonicas c ON c.id_compania = t.id_compania
        WHERE cl.id_cliente = :id_cliente;
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
c.monto_solicitado, c.tipo_monedaMonto_solicitado, c.tasa_interes, c.pagoMensual, c.pagoQuincenal,
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


def cambiar_estado_contrato(db_session, id_contrato, estado):
    try:
        query = text("""
        UPDATE contrato
        SET estado = :estado
        WHERE id_contrato = :id_contrato;
        """)
        db_session.execute(query, {"id_contrato": id_contrato, "estado": estado})
        db_session.commit()
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db_session.close()


def cambiar_estado_contrato_fiador(db_session, id_contrato_fiador, estado):
    try:
        query = text("""
        UPDATE contrato_fiador
        SET estado = :estado
        WHERE id_contrato_fiador = :id_contrato_fiador;
        """)
        db_session.execute(query, {"id_contrato_fiador": id_contrato_fiador, "estado": estado})
        db_session.commit()
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db_session.close()

def obtener_IdContrato(db_session, id_cliente):
    try:
        query = text("""
                     SELECT id_contrato
FROM contrato
WHERE id_cliente = :id_cliente
  AND estado IN (:estado1, :estado2)
ORDER BY fechaCreacionContrato DESC
LIMIT 1;"""
                     )
        result = db_session.execute(
            query, {'id_cliente': id_cliente, 'estado1': activo, 'estado2': hijoContratoActivo}).fetchone()
        return result[0]
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def obtener_IdContratoActivo(db_session, id_cliente):
    try:
        query = text("""
                     SELECT id_contrato
FROM contrato
WHERE id_cliente = :id_cliente
AND estado = :estado
LIMIT 1;"""
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




def cambiar_estadoContrato_finalizado(db_session, id_cliente, estado):
    try:
        query = text("""
        UPDATE contrato SET estado = :estado 
        WHERE estado  IN (1, 3) AND id_cliente = :id_cliente;
        """)
        db_session.execute(query, {"id_cliente": id_cliente, "estado": estado})
        db_session.commit()
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db_session.close()
     

def finalizacionContratoDescripcion(db_session, id_contrato, fechaFinalizacion, observacion):

    idFinalizacionContrato = ObtenerIDTabla(db_session, "finalizacionContrato", "idFinalizacionContrato")

    try:
        query = text("""
        INSERT INTO finalizacionContrato (idFinalizacionContrato, id_contrato, fechaFinalizacion, observacion, fechaRealizacionFinalizado)
                     VALUES (:idFinalizacionContrato, :id_contrato, :fechaFinalizacion, :observacion, NOW());
        """)
        db_session.execute(query, {"idFinalizacionContrato": idFinalizacionContrato, "id_contrato": id_contrato, "fechaFinalizacion": fechaFinalizacion, "observacion": observacion})
        db_session.commit()
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db_session.close()

def eliminar_todos_contratos_porIdCliente(db_session, id_cliente):
    try:
        query = text("""
        DELETE FROM contrato
        WHERE id_cliente = :id_cliente;
        """)
        db_session.execute(query, {"id_cliente": id_cliente})
        db_session.commit()
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db_session.close()

def eliminar_todos_contratos_fiador_porIdCliente(db_session, id_cliente):
    print("El id cliente es ", id_cliente)
    try:
        query = text("""
        DELETE FROM contrato_fiador
        WHERE id_cliente = :id_cliente;
        """)
        db_session.execute(query, {"id_cliente": id_cliente})
        db_session.commit()
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        db_session.close()



