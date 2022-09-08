from flask import request
from flask_restful import Resource
from Modelos.modelos import db, Publicacion, Publicacion_Schema

post_schema = Publicacion_Schema
posts_schema = Publicacion_Schema(many = True)

class RecursoListarPublicaciones(Resource):
    def get(self):
        publicaciones = Publicacion.query.all()
        return posts_schema.dump(publicaciones)
    
    def post(self):
            nueva_publicacion = Publicacion(
                titulo = request.json['titulo'],
                contenido=request.json['contenido']
            )
            db.session.add(nueva_publicacion)
            db.session.commit()
            return post_schema.dump(nueva_publicacion)
     
class RecursoUnaPublicacion(Resource):
    def get(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        return post_schema.dump(publicacion)
    
    def put(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)

        if 'titulo' in request.json:
            publicacion.titulo = request.json['titulo']
        if 'contenido' in request.json:
            publicacion.contenido = request.json['contenido']

        db.session.commit()
        return post_schema.dump(publicacion)

    def delete(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        db.session.delete(publicacion)
        db.session.commit()
        return '', 204

    