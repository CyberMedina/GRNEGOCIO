from db import *
from utils import *


############## INICIA PROCESO DE INSERTAR UN CLIENTE ##############
def insertar_tipo_cliente(db_session, nombre_tipoCliente, estado):
    try:
        # Obtener el ID de la tabla tipo_cliente
        id_tipoCliente = ObtenerIDTabla(
            db_session, "id_tipoCliente", "tipo_cliente")

        # Insertar los datos en la tabla tipo_cliente
        query = text("""
        INSERT INTO tipo_cliente (id_tipoCliente, nombre_tipoCliente, estado)
        VALUES (:id_tipoCliente, :nombre_tipoCliente, :estado);
        """)

        db_session.execute(query, {"id_tipoCliente": id_tipoCliente,
                           "nombre_tipoCliente": nombre_tipoCliente, "estado": estado})
        db_session.commit()

        return id_tipoCliente

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False

    finally:
        db_session.close()


def obtener_companias_telefonicas(db_session):
    # El estado 1 quiere decir que esa compañia esta activa

    try:
        query = text("""
        SELECT id_compania, nombre_compania FROM companias_telefonicas WHERE estado = '1';
        """)

        result = db_session.execute(query).fetchall()
        return result

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None

    finally:
        db_session.close()


def insertar_persona(db_session, nombres, apellidos, genero, cedula, fecha_nacimiento, estado):
    try:
        # Obtener el ID de la tabla persona
        id_persona = ObtenerIDTabla(db_session, "id_persona", "persona")

        # Insertar los datos en la tabla persona
        query = text("""
        INSERT INTO persona (id_persona, nombres, apellidos, genero, cedula, fecha_nacimiento, estado)
        VALUES (:id_persona, :nombres, :apellidos, :genero, :cedula, :fecha_nacimiento, :estado);
        """)

        db_session.execute(query, {"id_persona": id_persona, "nombres": nombres, "apellidos": apellidos,
                           "genero": genero, "cedula": cedula, "fecha_nacimiento": fecha_nacimiento, "estado": estado})
        db_session.commit()

        return id_persona

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False

    finally:
        db_session.close()


def insertar_direccion(db_session, nombre_direccion, direccion_escrita, direccion_mapa, estado):
    try:
        # Obtener el ID de la tabla direccion
        id_direccion = ObtenerIDTabla(db_session, "id_direccion", "direccion")

        # Insertar los datos en la tabla direccion
        query = text("""
        INSERT INTO direccion (id_direccion, nombre_direccion, direccion_escrita, direccion_mapa, estado)
        VALUES (:id_direccion, :nombre_direccion, :direccion_escrita, :direccion_mapa, :estado);
        """)

        db_session.execute(query, {"id_direccion": id_direccion, "nombre_direccion": nombre_direccion,
                           "direccion_escrita": direccion_escrita, "direccion_mapa": direccion_mapa, "estado": estado})
        db_session.commit()

        return id_direccion

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False

    finally:
        db_session.close()


def insertar_telefono(db_session, id_compania, nombre_telefono, numero_telefono, estado):
    try:
        # Obtener el ID de la tabla telefono
        id_telefono = ObtenerIDTabla(db_session, "id_telefono", "telefono")

        # Insertar los datos en la tabla telefono
        query = text("""
        INSERT INTO telefono (id_telefono, id_compania, nombre_telefono, numero_telefono, estado)
        VALUES (:id_telefono, :id_compania, :nombre_telefono, :numero_telefono, :estado);
        """)

        db_session.execute(query, {"id_telefono": id_telefono, "id_compania": id_compania,
                           "nombre_telefono": nombre_telefono, "numero_telefono": numero_telefono, "estado": estado})
        db_session.commit()

        return id_telefono

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False

    finally:
        db_session.close()


def insertar_persona_direccion(db_session, id_persona, id_direccion, estado):
    try:
        # Insertar los datos en la tabla persona_direccion
        query = text("""
        INSERT INTO persona_direccion (id_persona, id_direccion, estado)
        VALUES (:id_persona, :id_direccion, :estado);
        """)

        db_session.execute(
            query, {"id_persona": id_persona, "id_direccion": id_direccion, "estado": estado})
        db_session.commit()

        return True

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False

    finally:
        db_session.close()


def insertar_direccion_telelfono(db_session, id_direccion, id_telefono, estado):
    try:
        # Insertar los datos en la tabla direccion_telefono
        query = text("""
        INSERT INTO direccion_telefono (id_direccion, id_telefono, estado)
        VALUES (:id_direccion, :id_telefono, :estado);
        """)

        db_session.execute(query, {
                           "id_direccion": id_direccion, "id_telefono": id_telefono, "estado": estado})
        db_session.commit()

        return True

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False

    finally:
        db_session.close()


def insertar_cliente(db_session, id_persona, id_tipoCliente, imagenCliente, imagenCedula, estado):
    try:
        # Obtener el ID de la tabla cliente
        id_cliente = ObtenerIDTabla(db_session, "id_cliente", "cliente")

        # Insertar los datos en la tabla cliente
        query = text("""
        INSERT INTO cliente (id_cliente, id_persona, id_tipoCliente, imagenCliente, imagenCedula, estado)
        VALUES (:id_cliente, :id_persona, :id_tipoCliente, :imagenCliente, :imagenCedula, :estado);
        """)

        db_session.execute(query, {"id_cliente": id_cliente, "id_persona": id_persona, "id_tipoCliente": id_tipoCliente,
                           "imagenCliente": imagenCliente, "imagenCedula": imagenCedula, "estado": estado})
        db_session.commit()

        return id_cliente

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return False

    finally:
        db_session.close()

def listar_clientes(db_session, estado):
    try:
        estado = estado[0]
        query_no_definidos = text("""
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
cl.estado = '0'
                     """)
        
        query_activos =  text("""
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
cl.estado = '1'
                     """)

        if estado == '0':
            return db_session.execute(query_no_definidos)
        elif estado == '1':
            return db_session.execute(query_activos)

    
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()

def listar_clientes_activos(db_session):
    try:
        query = text("""
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
cl.estado = '1'
                     """)

         
        return db_session.execute(query)
    
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def ordenar_por_listadoClientes(db_session, numero_seleccionado):
    acciones = {
        '0': listar_clientes_no_definidos,
        '1': listar_clientes_activos,
    }
    print(numero_seleccionado)
    funcion = acciones.get(numero_seleccionado, lambda: "Invalido")
    funcion(db_session)  # Call the function with the db_session argument



############## TERMINA PROCESO DE INSERTAR UN CLIENTE ##############
