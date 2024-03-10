import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, session, url_for, redirect
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from num2words import num2words
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS, cross_origin
from datetime import datetime
from babel.dates import format_date


# Importando desde archivos locales
from db import *
from utils import *
from models.clientes import *
from models.constantes import *
from models.prestamos import *
from models.pagos import *

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"
CORS(app)

# Si no hay un número seleccionado en sesión, simplemente se asigna 1 
@app.before_request
def before_request():
    if "numero_seleccionado_ordenar_clientes" not in session:
        session["numero_seleccionado_ordenar_clientes"] = '1'

    if "numero_seleccionado_ordenar_prestamos" not in session:
        session["numero_seleccionado_ordenar_prestamos"] = '5'

    if "numero_seleccionado_ordenar_clientesPrestamos" not in session:
        session["numero_seleccionado_ordenar_clientesPrestamos"] = '0'
    


@app.route('/')
def index():
    return render_template('index.html')

######## Rutas para guardar en sesión el número seleccionado en diferentes templates ########
##### Clientes#########
@app.route("/guardar_en_sesion_ordenar_clientes", methods=["POST"])
def guardar_en_sesion_ordenar_clientes():
    data = request.get_json()  # Obtener datos enviados desde el frontend
    selected_value = data.get("selectedValue")
    
    # Guardar el valor en la sesión
    session["numero_seleccionado_ordenar_clientes"] = selected_value
    print(session)
    print(session.get("numero_seleccionado_ordenar_clientes"))

    return jsonify({"message": "Número guardado en sesión correctamente"})


@app.route("/convertir_numeros_a_letras", methods=["POST"])
def convertir_numeros_a_letras():
    data = request.get_json()
    monto = data.get("monto")
    monto_letras = num2words(monto, lang='es')
    return jsonify({"monto_letras": monto_letras})

@app.route("/convertir_fechas_a_letras", methods=["POST"])
def convertir_fechas_a_letras():
    data = request.get_json()
    fecha_str = data.get("fecha")  # Obtener la fecha como cadena de texto

    # Convertir la cadena de texto a un objeto de fecha
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")  # Suponiendo que la cadena de texto está en formato 'YYYY-MM-DD'



    dia = num2words(fecha.day, lang='es')
    mes = format_date(fecha, format='MMMM', locale='es_ES')
    año = num2words(fecha.year, lang='es')

    texto_fecha = f"a los {dia} días del mes de {mes} del año {año}"
    print(texto_fecha)  # 'nueve de febrero del año dosmil veinticuatro'



    return jsonify({"fecha_letras": texto_fecha})



##### Prestamos ########
@app.route("/guardar_en_sesion_ordenar_prestamos", methods=["POST"])
def guardar_en_sesion_ordenar_prestamos():
    data = request.get_json()  # Obtener datos enviados desde el frontend
    selected_value = data.get("selectedValue")
    
    # Guardar el valor en la sesión
    session["numero_seleccionado_ordenar_prestamos"] = selected_value
    print(session)
    print(session.get("numero_seleccionado_ordenar_prestamos"))

    return jsonify({"message": "Número guardado en sesión correctamente"})


###### Pagos #########
@app.route("/guardar_en_sesion_ordenar_clientesPrestamos", methods=["POST"])
def guardar_en_sesion_ordenar_clientesPrestamos():
    data = request.get_json()
    selected_value = data.get("selectedValue")

    session["numero_seleccionado_ordenar_clientesPrestamos"] = selected_value
    print(session)
    print(session.get("numero_seleccionado_ordenar_clientesPrestamos"))

    return jsonify({"message": "Número guardado en sesión correctamente"})

########### Empieza el modulo de clientes ###########
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():

    print(session.get("numero_seleccionado_ordenar_clientes"))
    # Obtenemos la lista de clientes cruda sin procesar

    
    cursor = listar_clientes(db_session, [session.get("numero_seleccionado_ordenar_clientes")])
    cantidad_clientes = contar_resultados(db_session, "cliente", [session.get("numero_seleccionado_ordenar_clientes")])
    print(cursor)

    


    # Procesamos la lista de clientes para mostrarla en el formulario
    formulario_clientes = {
        "companias_telefonicas": obtener_companias_telefonicas(db_session),
        "listar_clientes_data": cursor.fetchall(),
        "listar_clientes_columns": cursor.keys(),
        "cantidad_clientes": cantidad_clientes,
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

        db_session.begin()

        try:
            id_persona = insertar_persona(db_session, nombres, apellidos, genero, cedula, fechaNac, activo)
            id_direccion = insertar_direccion(db_session, nombreDireccion, direccion, direccionMaps, activo)
            id_telefono = insertar_telefono(db_session, idCompaniTelefonica, nombreTelefono, telefono, activo)
            id_persona_direccion = insertar_persona_direccion(db_session, id_persona, id_direccion, activo)
            id_direccion_telefono = insertar_direccion_telelfono(db_session, id_direccion, id_telefono, activo)
            id_insertar_cliente = insertar_cliente(db_session, id_persona, cliente_en_proceso, fotoCliente, foto_cedula, cliente_en_proceso)

            db_session.commit()

        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {str(e)}")
            return render_template('clientes/clientes.html', **formulario_clientes, error="Error en la base de datos")
        
        except Exception as e:
            db_session.rollback()
            print(f"Unexpected error: {str(e)}")
            return render_template('error.html', error="Unexpected error occurred"), 500
        
        finally:
            db_session.close()




        return redirect(url_for('clientes'))



    return render_template('clientes/clientes.html', **formulario_clientes)


@app.route('/datos_cliente', methods=['GET', 'POST'])
def datos_cliente():
    return render_template('datos_cliente.html')



########### Empieza el modulo de prestamos ###########
@app.route('/prestamos', methods=['GET', 'POST'])
def prestamos():

    print("PRESTMOAS")
    print(session.get("numero_seleccionado_ordenar_prestamos"))
    # Obtenemos la lista de clientes cruda sin procesar

    
    cursor = listar_prestamos(db_session, [session.get("numero_seleccionado_ordenar_prestamos")])
    cantidad_clientes = contar_resultados(db_session, "cliente", [session.get("numero_seleccionado_ordenar_prestamos")])
    print(cursor)

    


    # Procesamos la lista de clientes para mostrarla en el formulario
    formulario_clientes = {
        "companias_telefonicas": obtener_companias_telefonicas(db_session),
        "listar_clientes_data": cursor.fetchall(),
        "listar_clientes_columns": cursor.keys(),
        "cantidad_clientes": cantidad_clientes,
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

        db_session.begin()

        try:
            id_persona = insertar_persona(db_session, nombres, apellidos, genero, cedula, fechaNac, activo)
            id_direccion = insertar_direccion(db_session, nombreDireccion, direccion, direccionMaps, activo)
            id_telefono = insertar_telefono(db_session, idCompaniTelefonica, nombreTelefono, telefono, activo)
            id_persona_direccion = insertar_persona_direccion(db_session, id_persona, id_direccion, activo)
            id_direccion_telefono = insertar_direccion_telelfono(db_session, id_direccion, id_telefono, activo)
            id_insertar_cliente = insertar_cliente(db_session, id_persona, cliente_en_proceso, fotoCliente, foto_cedula, inactivo)

            db_session.commit()

        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {str(e)}")
            return render_template('clientes/clientes.html', **formulario_clientes, error="Error en la base de datos")
        
        except Exception as e:
            db_session.rollback()
            print(f"Unexpected error: {str(e)}")
            return render_template('error.html', error="Unexpected error occurred"), 500
        
        finally:
            db_session.close()

    return render_template('prestamos/prestamos.html', **formulario_clientes)


@app.route('/anadir_prestamo/<int:id_cliente>', methods=['GET', 'POST'])
def anadir_prestamo(id_cliente):
    print(id_cliente)

    datos_cliente = listar_datosClientes_porID(db_session, id_cliente)



    print(datos_cliente)

    datos_formulario_anadir_prestamo = {
        "companias_telefonicas": obtener_companias_telefonicas(db_session),
        "tipos_monedas" : obtener_tipos_monedas(db_session),
        "datos_cliente": datos_cliente
    }

    if request.method == 'POST':

        ## Step-1 form ###
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

        ### Step-2 form ###
        estadoCivil = request.form['estadoCivil']
        nombreDelegacion = request.form['nombreDelegacion']
        dptoArea = request.form['dptoArea']
        ftoColillaINSS = request.files['fotoCopiaColillaInss']
        tipoClienteString = request.form['tipoCliente']
        tipoCliente = int(tipoClienteString)
        montoSolicitado = request.form['montoSolicitado']
        tipoMonedaMontoSolictado = request.form['tipoMonedaMontoSolicitado']
        tasaInteres = request.form['tasaInteres']
        pagoMensual = request.form['pagoMensual']
        pagoQuincenal = request.form['pagoQuincenal']
        fechaPrestamo = request.form['fechaPrestamo']
        fechaPago = request.form['fechaPago']
        intervalo_tiempoPago = request.form['IntervaloPagoClienteEspecial'] # Solo para clientes especiales
        montoPrimerPago = request.form['montoPrimerPago']
        





        #### Step-3 form ####
        nombresFiador = request.form['nombresFiador']
        apellidosFiador = request.form['apellidosFiador']
        cedulaFiador = request.form['cedulaFiador']
        fechaNacFiador = request.form['fechaNacFiador']
        generoFiador = request.form['generoFiador']
        estadoCivilFiador = request.form['estadoCivilFiador']
        nombreDelegacionFiador = request.form['nombreDelegacionFiador']
        dptoAreaFiador = request.form['dptoAreaFiador']
        direccionFiador = request.form['direccionFiador']
        direccionMapsFiador = request.form['direccionMapsFiador']
        nombreDireccionFiador = request.form['nombreDireccionFiador']
        idCompaniTelefonicaFiador = request.form['idCompaniTelefonicaFiador']
        telefonoFiador = request.form['telefonoFiador']
        nombreTelefonoFiador = request.form['nombreTelefonoFiador']
        fotoFiador = request.files['fotoFiador']
        foto_cedulaFiador = request.files['foto_cedulaFiador']
        fotoCopiaColillaInssFiador = request.files['fotoCopiaColillaInssFiador']

        db_session.begin()

        try:

            ## Step-1 form ###

            #### Actualizar datos del cliente ####
            actualizar_persona(db_session, datos_cliente.id_persona, nombres, apellidos, genero, cedula, fechaNac, activo) #Actualizar datos del cliente y cambiar activo

            id_direccionYtelefono = obtenerID_direccionYtelefono(db_session, datos_cliente.id_persona)
            actualizar_direccion(db_session, id_direccionYtelefono.id_direccion, nombreDireccion, direccion, direccionMaps, activo)
            actualizar_telefono(db_session, id_direccionYtelefono.id_telefono, idCompaniTelefonica, nombreTelefono, telefono, activo)
            actualizar_cliente(db_session, id_cliente, datos_cliente.id_persona, tipoCliente, fotoCliente, foto_cedula, activo) #Actualizar datos del cliente y cambiar activo

            #### Terminar de actualizar datos del cliente ####

            ## Step-2 form ###

            
            #### Insertamos al fiador ####

            # Si el checbox se encuentra en el formulario quiere decir que no hay deudor
            if 'chckbxNoDeudor' in request.form:
                id_persona = insertar_persona(db_session, sin_especificar, sin_especificar, sin_especificar, sin_especificar, sin_especificar, activo)
                id_direccion = insertar_direccion(db_session, sin_especificar, sin_especificar, sin_especificar, activo)
                id_telefono = insertar_telefono(db_session, sin_especificar, sin_especificar, sin_especificar, activo)
                id_persona_direccion = insertar_persona_direccion(db_session, sin_especificar, sin_especificar, activo)
                id_direccion_telefono = insertar_direccion_telelfono(db_session, sin_especificar, sin_especificar, activo)
                id_insertar_clienteFiador = insertar_cliente(db_session, id_persona, fiador, sin_especificar, sin_especificar, activo)
            else:
                id_persona = insertar_persona(db_session, nombresFiador, apellidosFiador, generoFiador, cedulaFiador, fechaNacFiador, activo)
                id_direccion = insertar_direccion(db_session, nombreDireccionFiador, direccionFiador, direccionMapsFiador, activo)
                id_telefono = insertar_telefono(db_session, idCompaniTelefonicaFiador, nombreTelefonoFiador, telefonoFiador, activo)
                id_persona_direccion = insertar_persona_direccion(db_session, id_persona, id_direccion, activo)
                id_direccion_telefono = insertar_direccion_telelfono(db_session, id_direccion, id_telefono, activo)
                id_insertar_clienteFiador = insertar_cliente(db_session, id_persona, fiador, fotoFiador, foto_cedulaFiador, activo)




            #### Terminamos de insertar al fiador ####


            ##### Insertamos el contrato especificamente datos del fiador #######

            # Si el checbox se encuentra en el formulario quiere decir que no hay deudor
            if 'chckbxNoDeudor' in request.form:
                checkbox_no_deudor = request.form['chckbxNoDeudor'] ## Revisar si el fiador es no deudor se recibirá un valor de 5 en el checkbox
                id_contrato_fiador = insertar_contrato_fiador(db_session, id_insertar_clienteFiador, estadoCivilFiador, nombreDelegacionFiador, dptoAreaFiador,fotoCopiaColillaInssFiador , no_fiador)
            
            else:
                id_contrato_fiador = insertar_contrato_fiador(db_session, id_cliente, estadoCivilFiador, nombreDelegacionFiador, dptoAreaFiador, fotoCopiaColillaInssFiador, activo)


            print(tipoCliente)
            print("debería haber validaciones aquí")
            if tipoCliente == cliente_normal:

                print("Cliente normal")

                id_contrato = insertar_contrato(db_session, id_cliente, estadoCivil, nombreDelegacion, dptoArea, ftoColillaINSS, 
                      montoSolicitado, tipoMonedaMontoSolictado, tasaInteres, pagoMensual, pagoQuincenal, fechaPrestamo, 
                      fechaPago, prestamo_cliente_normal, montoPrimerPago, activo)
                
                print(id_contrato)

            elif tipoCliente == cliente_especial:

                print("Cliente especial")
                
                id_contrato = insertar_contrato(db_session, id_cliente, estadoCivil, nombreDelegacion, dptoArea, ftoColillaINSS, 
                      montoSolicitado, tipoMonedaMontoSolictado, tasaInteres, pagoMensual, pagoQuincenal, fechaPrestamo, 
                      fechaPago, intervalo_tiempoPago, montoPrimerPago, activo)
                
                print(id_contrato)


            db_session.commit()


            
            
            
            
            

        
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error: {str(e)}")
            return redirect(url_for('prestamos', error="Error en la base de datos"))
        
        except Exception as e:
            db_session.rollback()
            print(f"Unexpected error: {str(e)}")
            return render_template('error.html', error="Unexpected error occurred"), 500
        
        finally:
            db_session.close()





        return redirect(url_for('prestamos'))


    return render_template('prestamos/anadir_prestamo.html', **datos_formulario_anadir_prestamo)


########### Empieza el modulo de pagos ############

@app.route('/listado_clientes_pagos', methods=['GET', 'POST'])
def listado_clientes_pagos():

    print(session.get("numero_seleccionado_ordenar_clientesPrestamos"))
    # Obtenemos la lista de clientes 




    formulario_clientes_pagos = {
        "listado_clientes_pagos": listar_cliesntesPagos(db_session),
    }

    return render_template('pagos/listado_clientes_pagos.html', **formulario_clientes_pagos)






@app.route('/prueba_extraer_plata', methods=['GET', 'POST'])
def prueba_extraer_plata():

    dolar = obtener_tasa_cambio()
    print(dolar)


    return 'Si entró!'

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
