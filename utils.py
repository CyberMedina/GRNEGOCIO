from db import *

def ObtenerIDTabla(db_session, id_tabla, tabla):
    query = text(f'SELECT MAX({id_tabla}) AS id FROM {tabla}')
    result = db_session.execute(query)

    # Intentar obtener el ID
    id_obtenido = result.fetchone()[0]  # Se extrae el valor del resultado

    if id_obtenido is not None:
        # Si se encontró un ID, sumar uno al valor existente
        id_nuevo = id_obtenido + 1
    else:
        # Si no se encontró ningún ID, asignar 1 como valor inicial
        id_nuevo = 1

    return id_nuevo

    # Crea la funcion obtner_index_columna
def obtener_index_columna(cursor, nombre_columna):
    columnas = list(cursor.keys())
    index = columnas.index(nombre_columna)
    return index

    # Crea una función para retornar la cantidad de resultados de una tabla x con x estado
def contar_resultados(db_session, tabla, estado):
    query = text(f'SELECT COUNT(*) FROM {tabla} WHERE estado = :estado')
    result = db_session.execute(query, {"estado": estado})
    return result.fetchone()[0]
