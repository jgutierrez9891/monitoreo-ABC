from threading import Thread
from flask_cors import CORS
from flask import Flask
from Modelos.modelos import db
from API.api import RecursoListarPublicaciones, RecursoUnaPublicacion
from flask_restful import Api
from SQS_Processor.monitor_processor import process_message
import boto3
import time

sqs = boto3.resource("sqs", region_name="us-east-1",
                            aws_access_key_id="AKIA6QD43RTCVK6T5IIY",
                            aws_secret_access_key="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")
queue = sqs.get_queue_by_name(QueueName="ColaMonitoreo")

def start_message_publisher():
    while(True):
        time.sleep(30) 
        #Guarda en BD los registros de mensajes (1 solo micro)
        #Publica mensaje en la cola
        time.sleep(30)
        messages = queue.receive_messages(MessageAttributeNames=['All'])
        for message in messages:
            process_message(message)
            message.delete()
        

app = Flask(__name__)
t = Thread(target=start_message_publisher)
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