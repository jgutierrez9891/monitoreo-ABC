from flaskr import create_app
from .modelos import db, ReglaMonitoreo, ReglaMonitoreoSchema
from flask_restful import Api
from .vistas import VistaReglaMonitoreo
from SQS_Processor.micro_processor import process_message
import boto3
from flask import Flask
from threading import Thread
from flask_cors import CORS

sqs = boto3.resource("sqs", region_name="us-east-1",
                            aws_access_key_id="AKIA6QD43RTCWNJOXMKG",
                            aws_secret_access_key="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")
queue = sqs.get_queue_by_name(QueueName="https://sqs.us-east-1.amazonaws.com/996694265029/ColaMonitoreo")

def start_message_consumer():
    while(True): 
        messages = queue.receive_messages(MessageAttributeNames=['All'])
        for message in messages:
            process_message(message)
            #send response more similar to start_monitoreo
            message.delete()


def send_message_to_queue(message, message_attributes):
    print("Enviando mensaje: "+message)
    print("Atributos: "+str(message_attributes))
    sqs_client = boto3.client("sqs", region_name="us-east-1", aws_access_key_id="AKIA6QD43RTCWNJOXMKG", aws_secret_access_key= "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")
    response = sqs_client.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/996694265029/ColaMonitoreo",
        MessageBody = message,
        MessageAttributes = message_attributes
    )
    print("Respuesta cola: "+str(response))
    pass

def receive_messages_from_queue():
    print("Recibir mensajes de la cola")

    sqs = boto3.resource("sqs", region_name="us-east-1", aws_access_key_id="AKIA6QD43RTCWNJOXMKG", aws_secret_access_key="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")
    queue = sqs.get_queue_by_name(QueueName="ColaMonitoreo")
    messages = queue.receive_messages(MessageAttributeNames=['All'])

    return messages

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
api.add_resource(VistaReglaMonitoreo, '/reglasmonitoreo')
