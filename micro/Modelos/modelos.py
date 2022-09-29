from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


class Publicacion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column( db.String(50) )
    contenido = db.Column( db.String(255) )

class FallaMicro(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.DateTime)

class EstadoMicro(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.DateTime)
    id_micro = db.Column(db.String(50))
    estado = db.Column(db.String(50))
    
class Publicacion_Schema(ma.Schema):
    class Meta:
        fields = ("id", "titulo", "contenido")

class FallaMicro_Schema(ma.Schema):
    class Meta:
        fields = ("id", "fecha")

class EstadoMicro_Schema(ma.Schema):
    class Meta:
        fields = ("id", "fecha", "id_micro", "estado")