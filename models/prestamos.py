from db import *
from utils import *


def listar_prestamos(db_session, estado):
    try:
        estado = estado[0]
        print(f'El número de estado a consultar es: {estado}')
        query_listar_clientes = text("""
                     SELECT cl.id_cliente, CONCAT(p.nombres, ' ', p.apellidos) AS 'Nombre',
d.direccion_escrita AS 'Dirección',
CONCAT(c.nombre_compania, ' ', t.numero_telefono) AS 'Teléfono',
  cl.estado AS 'Estado'
FROM cliente cl
JOIN persona p ON cl.id_persona = p.id_persona
JOIN persona_direccion pd ON pd.id_persona = p.id_persona
JOIN direccion d ON d.id_direccion = pd.id_direccion
JOIN direccion_telefono dt ON dt.id_direccion = d.id_direccion
JOIN telefono t ON t.id_telefono = dt.id_telefono
JOIN companias_telefonicas c ON c.id_compania = t.id_compania
WHERE
cl.estado = :estado;
                     """)

        result = db_session.execute(query_listar_clientes, {"estado": estado})
        return result

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def cantidad_clientes(db_session, estado):
    try:
        estado = estado[0]
        query_cantidad_clientes = text("""
        SELECT COUNT(*) AS 'Cantidad'
        FROM cliente
        WHERE estado = :estado;
        """)

        result = db_session.execute(
            query_cantidad_clientes, {"estado": estado})
        return result

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def listar_datosClientes_porID(db_session, id_cliente):
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
cl.id_cliente = :id_cliente
AND
cl.estado = '0';
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


def insertar_contrato(id_contrato, id_cliente, estado_civil, nombre_delegacion, dptoArea_trabajo, monto_solicitado, plazo_solicitado, estado):
    try:

        # Obtener el ID de la tabla tipo_cliente
        id_contrato = ObtenerIDTabla(
        db_session, "id_contrato", "contrato")

        query = text("""
        INSERT INTO contrato (id_contrato, id_cliente, id_contrato, estado_civil, nombre_delegacion, dptoArea_trabajo, monto_solicitado, plazo_solicitado, estado)
        VALUES (:id_contrato, :id_cliente, :id_contrato, :estado_civil, :nombre_delegacion, :dptoArea_trabajo, :monto_solicitado, :plazo_solicitado, :estado);
                     """)

        db_session.execute(query, {"id_contrato": id_contrato, "id_cliente": id_cliente, "id_contrato": id_contrato, "estado_civil": estado_civil,
                           "nombre_delegacion": nombre_delegacion, "dptoArea_trabajo": dptoArea_trabajo, "monto_solicitado": monto_solicitado, "plazo_solicitado": plazo_solicitado, "estado": estado})

        db_session.commit()

        return id_contrato

    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None
