from flask_restful import Resource
from ..modelos import db, ReglaMonitoreo, ReglaMonitoreoSchema

reglaSchema = ReglaMonitoreoSchema()

class VistaReglaMonitoreo(Resource):

    def get(self):
        return [reglaSchema.dumps(regla) for regla in ReglaMonitoreo.query.all()]