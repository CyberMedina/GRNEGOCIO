from sqlalchemy import inspect, text
from sqlalchemy.schema import DropTable
import tempfile
import requests
import os
import time
import json
from multiprocessing import Process

def drop_all_tables(update_progress_callback=None):
    """Elimina tablas una por una reportando progreso."""
    metadata.reflect(bind=engine)
    inspector = inspect(engine)
    
    # Obtener tablas en orden inverso de dependencia
    ordered_tables = []
    for table_name in inspector.get_table_names():
        ordered_tables.append(metadata.tables[table_name])
    
    total_tables = len(ordered_tables)
    
    for i, table in enumerate(reversed(ordered_tables), 1):
        try:
            progress = int((i / total_tables) * 100) if total_tables > 0 else 0
            if update_progress_callback:
                update_progress_callback(progress, f"Eliminando tabla: {table.name}")
                
            with engine.begin() as conn:
                conn.execute(DropTable(table, if_exists=True))
                
        except Exception as e:
            raise Exception(f"Error eliminando {table.name}: {str(e)}")

def restore_process(file_url, user_id):
    status_file = os.path.join(tempfile.gettempdir(), f'restore_status_{user_id}.json')
    start_time = time.time()
    TIMEOUT_MINUTES = 10

    def update_status(progress, status, error=False, completed=False):
        with open(status_file, 'w') as f:
            json.dump({
                'progress': progress,
                'status': status,
                'error': error,
                'completed': completed
            }, f)

    def check_timeout():
        if (time.time() - start_time) > (TIMEOUT_MINUTES * 60):
            raise TimeoutError(f"Timeout excedido ({TIMEOUT_MINUTES} minutos)")

    try:
        with app.app_context():
            update_status(0, 'Iniciando proceso...')
            check_timeout()

            # Paso 1: Validación de URL
            if '/restore?file_url=' in file_url:
                file_url = file_url.split('/restore?file_url=')[1]
            
            if 'dl=0' in file_url:
                file_url = file_url.replace('dl=0', 'dl=1')
            elif 'dl=1' not in file_url:
                file_url += '&dl=1' if '?' in file_url else '?dl=1'

            # Paso 2: Descarga del archivo
            update_status(10, 'Descargando backup...')
            response = requests.get(file_url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code != 200:
                raise Exception(f"Error HTTP {response.status_code}")

            # Paso 3: Guardar temporalmente
            with tempfile.NamedTemporaryFile(delete=False, suffix='.sql') as tmp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    tmp_file.write(chunk)
                    check_timeout()
                tmp_path = tmp_file.name

            # Paso 4: Eliminar tablas existentes
            def update_drop_progress(progress, message):
                adjusted_progress = 20 + int(progress * 0.3)  # 20-50% del progreso total
                update_status(adjusted_progress, message)
            
            update_status(20, 'Preparando limpieza...')
            drop_all_tables(update_progress_callback=update_drop_progress)

            # Paso 5: Restauración
            update_status(50, 'Iniciando restauración...')
            with open(tmp_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            statements = [s.strip() for s in sql_content.split(';') if s.strip()]
            total_statements = len(statements)
            
            for idx, stmt in enumerate(statements):
                check_timeout()
                try:
                    db_session.execute(text(stmt))
                    progress = 50 + int((idx / total_statements) * 50)
                    update_status(progress, f"Ejecutando query {idx+1}/{total_statements}")
                except Exception as e:
                    raise Exception(f"Error en query {idx+1}: {str(e)}")
            
            db_session.commit()
            update_status(100, '¡Restauración completada!', completed=True)

    except Exception as e:
        db_session.rollback()
        update_status(0, f"Error: {str(e)}", error=True)
    except TimeoutError as e:
        update_status(0, str(e), error=True)
    finally:
        try:
            os.remove(tmp_path)
        except:
            pass
        db_session.close()