from flask import Flask, request, jsonify, Blueprint
from db import *
from utils import *


def datos_persona(id_persona):

    try:
        query = text('SELECT nombres, apellidos FROM persona WHERE id_persona = :id_persona')

        result = db_session.execute(query, {'id_persona': id_persona}).fetchall()

        nombres = result[0][0]
        apellidos = result[0][1]



        return nombres, apellidos
    
    except Exception as e:
        print(e)
        return None
    
    finally:
        db_session.close()


def datos_rol(id_rol):

    try:
        query = text('SELECT rolname FROM rol WHERE id_rol = :id_rol')

        result = db_session.execute(query, {'id_rol': id_rol}).fetchall()

        rolname = result[0][0]

        return rolname
    
    except Exception as e:
        print(e)
        return None
    
    finally:
        db_session.close()
    



