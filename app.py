import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from num2words import num2words

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
    return render_template('index.html')


def busqueda_capital(nombres):
    print(nombres)
    query = text("""
    SELECT p.nombres, c.monto_capital
    FROM persona p
    JOIN capital c ON p.id_persona = c.id_persona
    WHERE p.nombres ILIKE :nombres;
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
        result = busqueda_capital(nombres)

        

        if result:
            montoCapital_Texto = f"{num2words(result.monto_capital, lang='es')} cordobas" 
            return jsonify({"nombres": result.nombres, "monto_capital": montoCapital_Texto}), 200
        else:
            return jsonify({"message": "No se encontro el nombre"}), 404
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
