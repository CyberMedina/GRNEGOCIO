import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from num2words import num2words
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS, cross_origin


# Importando desde archivos locales
from db import *
from utils import *
from models.clientes import *
from models.constantes import activo, inactivo, no_definido, cliente_normal, cliente_especial, fiador

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/guardar_en_sesion", methods=["POST"])
def guardar_en_sesion():
    data = request.get_json()  # Obtener datos enviados desde el frontend
    selected_value = data.get("selectedValue")

    # Guardar el valor en la sesión
    session["numero_seleccionado"] = selected_value
    print(session)
    print(session.get("numero_seleccionado"))

    return jsonify({"message": "Número guardado en sesión correctamente"})

########### Empieza el modulo de clientes ###########
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():


    # Obtenemos la lista de clientes cruda sin procesar

    
    cursor = listar_clientes(db_session, [session.get("numero_seleccionado")])
    print(cursor)

    


    # Procesamos la lista de clientes para mostrarla en el formulario
    formulario_clientes = {
        "companias_telefonicas": obtener_companias_telefonicas(db_session),
        "listar_clientes_data": cursor.fetchall(),
        "listar_clientes_columns": cursor.keys(),
        "index_estado": obtener_index_columna(cursor, "Estado"),
        "index_id": obtener_index_columna(cursor, "id_cliente")
    }

    print(formulario_clientes)

    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = request.form['cedula']
        fechaNac = request.form['fechaNac']
        genero = request.form['genero']
        direccion = request.form['direccion']
        direccionMaps = request.form['direccionMaps']
        nombreDireccion = request.form['nombreDireccion']
        idCompaniTelefonica = request.form['idCompaniTelefonica']
        telefono = request.form['telefono']
        nombreTelefono = request.form['nombreTelefono']
        fotoCliente = request.files['fotoCliente']
        foto_cedula = request.files['foto_cedula']

        try:
            id_persona = insertar_persona(db_session, nombres, apellidos, genero, cedula, fechaNac, activo)
            id_direccion = insertar_direccion(db_session, nombreDireccion, direccion, direccionMaps, activo)
            id_telefono = insertar_telefono(db_session, idCompaniTelefonica, nombreTelefono, telefono, activo)
            id_persona_direccion = insertar_persona_direccion(db_session, id_persona, id_direccion, activo)
            id_direccion_telefono = insertar_direccion_telelfono(db_session, id_direccion, id_telefono, activo)
            id_insertar_cliente = insertar_cliente(db_session, id_persona, no_definido, fotoCliente, foto_cedula, inactivo)

            db_session.commit()

        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {str(e)}")
            return render_template('clientes/clientes.html', **formulario_clientes, error="Error en la base de datos")
        
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return render_template('error.html', error="Unexpected error occurred"), 500
        
        finally:
            db_session.close()




        return render_template('clientes/clientes.html', **formulario_clientes)



    return render_template('clientes/clientes.html', **formulario_clientes)


@app.route('/datos_cliente', methods=['GET', 'POST'])
def datos_cliente():
    return render_template('datos_cliente.html')



########### Empieza el modulo de prestamos ###########





########### Empieza el modulo de capital ###########

@app.route('/modals', methods=['GET', 'POST'])
def modals():
    return render_template('modals.html')




def busqueda_capital(nombres):
    print(nombres)
    query = text("""
    SELECT p.nombres, c.monto_capital
    FROM persona p
    JOIN capital c ON p.id_persona = c.id_persona
    WHERE UPPER(p.nombres) LIKE UPPER(:nombres);
    """)

    result = db_session.execute(query, {"nombres": nombres}).fetchone()
    print(result)

    return result


@app.route('/api/obtener_capital', methods=['GET', 'POST'])
@cross_origin()
def obtener_capital():
    if request.method == 'POST':
        data = request.json
        print(data)
        nombres = data['person']
        print(nombres)
        
        try:
            result = busqueda_capital(nombres)
            if result:
                montoCapital_Texto = f"{num2words(result.monto_capital, lang='es')} cordobas" 
                return jsonify({"nombres": result.nombres, "monto_capital": montoCapital_Texto}), 200
            else:
                return jsonify({"message": "No se encontro el nombre"}), 404
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {e}")
            return jsonify({"message": "Error en la base de datos"}), 500
    else:
        return jsonify({"message": "Metodo no permitido"}), 400

@app.route('/pruebita', methods=['GET', 'POST'])
@cross_origin()
def pruebita():

    if request.method == 'GET':
        return jsonify({"message": "API is working"}), 200
    else:
        return jsonify({"message": "API is notworking"}), 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
