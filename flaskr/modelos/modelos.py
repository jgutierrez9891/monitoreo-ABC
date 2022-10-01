from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

db = SQLAlchemy()

class ReglaMonitoreo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombreUbicacion = db.Column(db.String(128))
    numerosTelefonoArray = db.Column(db.String(128))
    notificarNumerosTelefono = db.Column(db.Boolean)
    notificarPropietario = db.Column(db.Boolean)
    notificarPolicia= db.Column(db.Boolean)
    notificarBomberos = db.Column(db.Boolean)
    notificarPrimerosAuxilios = db.Column(db.Boolean)

    def __repr__(self):
        return "{}-{}-{}-{}-{}-{}".format(self.nombreUbicacion, self.numerosTelefonoArray, self.notificarPropietario, self.notificarPolicia, self.notificarBomberos, self.notificarPrimerosAuxilios)


class MicroAccedido(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.DateTime)
    idMensaje = db.Column(db.String(5))


class MicroAccedidoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MicroAccedido
        load_instance = True
