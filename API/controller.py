from flask import request
from flask_restful import Resource
from Modelos.modelos import EstadoMicro_Schema, db, EstadoMicro
import datetime

estadoMicro_schema = EstadoMicro_Schema()

class RecursoEstadoMicro(Resource):
    def post(self):
        print("Ingresa a crear registro")
        nuevo_EstadoMicro = EstadoMicro(
                    fecha = datetime.datetime.now(),
                    id_micro = "1"
                )
        db.session.add(nuevo_EstadoMicro)
        db.session.commit()
        print("Finaliza creación registro")
        return estadoMicro_schema.dump(nuevo_EstadoMicro)

class RecursoEstadoMicroAct(Resource):
    def put(self, id_estado):
        print("Va a actualizar id_estado: "+str(id_estado))
        estadoMicro = EstadoMicro.query.get_or_404(id_estado)
        estadoMicro.estado = "OK"
        db.session.commit()
        return estadoMicro_schema.dump(estadoMicro)