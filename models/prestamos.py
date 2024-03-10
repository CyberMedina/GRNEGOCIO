from db import *
from utils import *



def obtener_tipos_monedas(db_session):
    try:
        query = text("""SELECT id_moneda, nombreMoneda, codigoMoneda FROM moneda;""")
        result = db_session.execute(query)
        print(result)
        return result
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()

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
cl.estado = '5';
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


def insertar_contrato(db_session, id_cliente, estado_civil, nombre_delegacion, dptoArea_trabajo, ftoColillaINSS, 
                      monto_solicitado, tipo_monedaMonto_solicitado, tasa_interes, pagoMensual, pagoQuincenal, fechaPrestamo, 
                      fechaPago, intervalo_tiempoPago, montoPrimerPago, estado):
    try:

        # Obtener el ID de la tabla tipo_cliente
        id_contrato = ObtenerIDTabla(
        db_session, "id_contrato", "contrato")

        query = text("""
        INSERT INTO contrato (id_contrato, id_cliente, id_contrato_fiador, estado_civil, nombre_delegacion, dptoArea_trabajo,
                      ftoColillaINSS, monto_solicitado, tipo_monedaMonto_solicitado, tasa_interes, pagoMensual, pagoQuincenal, 
                     fechaPrestamo, fechaPago, intervalo_tiempoPago, montoPrimerPago, fechaCreacionContrato, estado)
        VALUES (:id_contrato, :id_cliente, :id_contrato, :estado_civil, :nombre_delegacion, :dptoArea_trabajo,
                     :ftoColillaINSS, :monto_solicitado, :tipo_monedaMonto_solicitado, :tasa_interes, :pagoMensual, :pagoQuincenal,
                    :fechaPrestamo, :fechaPago, :intervalo_tiempoPago, :montoPrimerPago, NOW(), :estado);
                     """)
        
        db_session.execute(query, {"id_contrato": id_contrato, "id_cliente": id_cliente, "id_contrato": id_contrato, "estado_civil": estado_civil,
            "nombre_delegacion": nombre_delegacion, "dptoArea_trabajo": dptoArea_trabajo, "ftoColillaINSS":ftoColillaINSS,
            "monto_solicitado": monto_solicitado, "tipo_monedaMonto_solicitado": tipo_monedaMonto_solicitado, "tasa_interes": tasa_interes,
            "pagoMensual": pagoMensual, "pagoQuincenal": pagoQuincenal, "fechaPrestamo": fechaPrestamo, "fechaPago": fechaPago,
            "intervalo_tiempoPago": intervalo_tiempoPago, "montoPrimerPago": montoPrimerPago, "estado": estado})
        



        return id_contrato

    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None
    

def insertar_contrato_fiador(db_session, id_cliente, estado_civil, nombre_delegacion, dptoArea_trabajo, ftoColillaINSS, estado):
    try:

        # Obtener el ID de la tabla tipo_cliente
        id_contrato_fiador = ObtenerIDTabla(
        db_session, "id_contrato_fiador", "contrato_fiador")

        query = text("""
        INSERT INTO contrato_fiador (id_contrato_fiador, id_cliente, estado_civil, nombre_delegacion, dptoArea_trabajo, ftoColillaINSS,  estado)
        VALUES (:id_contrato_fiador, :id_cliente, :estado_civil, :nombre_delegacion, :dptoArea_trabajo, :ftoColillaINSS, :estado);
                     """)

        db_session.execute(query, {"id_contrato_fiador": id_contrato_fiador, "id_cliente": id_cliente, "estado_civil": estado_civil,
                                     "nombre_delegacion": nombre_delegacion, "dptoArea_trabajo": dptoArea_trabajo, "ftoColillaINSS":ftoColillaINSS, "estado": estado})

        db_session.commit()

        return id_contrato_fiador

    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None
