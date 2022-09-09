from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


class EstadoMicro(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.DateTime)
    id_micro = db.Column(db.String(50))
    estado = db.Column(db.String(50))
    
class EstadoMicro_Schema(ma.Schema):
    class Meta:
        fields = ("id", "fecha", "id_micro", "estado")