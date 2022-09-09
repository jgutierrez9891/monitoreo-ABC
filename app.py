from threading import Thread
from flask_cors import CORS
from flask import Flask
from Modelos.modelos import db
from API.api import RecursoListarPublicaciones, RecursoUnaPublicacion
from flask_restful import Api
from SQS_Processor.micro_processor import process_message
import boto3

sqs = boto3.resource("sqs", region_name="us-east-1",
                            aws_access_key_id="",
                            aws_secret_access_key="")
queue = sqs.get_queue_by_name(QueueName="")

def start_message_consumer():
    while(True): 
        messages = queue.receive_messages(MessageAttributeNames=['All'])
        for message in messages:
            process_message(message)
            message.delete()

app = Flask(__name__)
t = Thread(target=start_message_consumer)
t.daemon = True
t.start()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(RecursoListarPublicaciones, '/publicaciones')     
api.add_resource(RecursoUnaPublicacion, '/publicaciones/<int:id_publicacion>')