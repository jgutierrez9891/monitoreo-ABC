from flaskr.vistas.vistas import VistaMicroAccedidoSchema
from .modelos import db, ReglaMonitoreo
import datetime
from flaskr import create_app
from flask_restful import Api
import boto3
from flask import Flask
from threading import Thread
from flask_cors import CORS
from random import randrange
import requests

app = create_app('default')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "super-secret"

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

# cors = CORS(app)

api = Api(app)
api.add_resource(VistaMicroAccedidoSchema, '/micro')
