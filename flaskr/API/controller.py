from flask import request
from flask_restful import Resource
from ..modelos import  db, FallaMicro
import datetime


class RecursoEstado(Resource):
    def get(self, id_estado):
        print("Almacenamiento de falla en request: "+str(id_estado))
        nueva_falla_servicio = FallaMicro(
            fecha = datetime.datetime.now(),
            idMensaje = id_estado
        )
        db.session.add(nueva_falla_servicio)
        db.session.commit()

