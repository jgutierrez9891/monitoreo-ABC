from flask import Flask
def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ubicaciones.db'
    app.config['SQLACHEMY_TRACK_MODIFICAIONTS'] = False
    return app