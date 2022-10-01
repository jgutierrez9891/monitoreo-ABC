import datetime
from datetime import date
from flask_restful import Resource
from ..modelos import db, ReglaMonitoreo, MicroAccedido, MicroAccedidoSchema
from flask_jwt_extended import create_access_token, jwt_required
from flask import request


microAccedidoSchema = MicroAccedidoSchema()

class VistaMicroAccedidoSchema(Resource):
    @jwt_required()
    def post(self):
        print('inside micro post')
        nuevoAcceso = MicroAccedido(
            fecha= datetime.datetime.combine(date.today(), datetime.datetime.min.time()),
            idMensaje= request.json['idMensaje']
                                    )
        db.session.add(nuevoAcceso)
        db.session.commit()
        return microAccedidoSchema.dump(nuevoAcceso)
