from database_connection import *
from helpers import *

def crear_reespaldoBD(db_session, ruta_archivo):
    try:

        nombre_archivo = os.path.basename(ruta_archivo)

        # Obtener el ID de la tabla tipo_cliente
        id_backupsBD = ObtenerIDTabla(
        db_session, "id_backupsBD", "backupsBD")

        query = text("""INSERT INTO backupsBD (id_backupsBD, nombre_backup, ruta_backup, fechaHora)
                     VALUES (:id_backupsBD, :nombre_backup, :ruta_backup, NOW());
                      """)
        
        db_session.execute(query, {"id_backupsBD": id_backupsBD, "nombre_backup": nombre_archivo, "ruta_backup": ruta_archivo})

        db_session.commit()

        return id_backupsBD
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()



def seleccionar_ultimo_backup(db_session):
    try:
        query = text("""SELECT *
FROM backupsBD
ORDER BY fechaHora DESC
LIMIT 1;
                        """)
        result = db_session.execute(query).fetchone()
        fechaHoraFormateada = result[3].strftime("%A %d de %B del %Y a las %I:%M:%S %p")
        fechaHoraFormateada = fechaHoraFormateada.encode('latin1').decode('utf8')


    
        jsonresult = {
                "id_backupsBD": result[0],
                "nombre_backup": result[1],
                "ruta_backup": result[2],
                "fechaHora": fechaHoraFormateada
            }
    
        return jsonresult
    
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error: {e}")
        return None
    finally:
        db_session.close()


def obtener_backups_bd(db_session):
    """
    Obtiene los backups desde la tabla backupsbd y los formatea para la vista
    """
    try:
        query = text("""
            SELECT id_backupsBD, nombre_backup, ruta_backup, fechaHora 
            FROM backupsbd
            ORDER BY fechaHora DESC
        """)
        
        result = db_session.execute(query).fetchall()
        
        backups_files = []
        
        for backup in result:
            response = {
                "filename": backup.nombre_backup,
                "fileDate": backup.fechaHora.strftime("%Y-%m-%d %H:%M:%S"),
                "import_link": f"/restore?file_url={backup.ruta_backup}",
                "download_link": backup.ruta_backup,
                "delete_link": f"/delete_backup/{backup.id_backupsBD}"
            }
            backups_files.append(response)
            
        return backups_files
        
    except Exception as e:
        print(f"Error al obtener backups: {str(e)}")
        return []