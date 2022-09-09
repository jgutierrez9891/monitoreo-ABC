from threading import Thread
from flask_cors import CORS
from flask import Flask
from flask_restful import Api
from SQS_Processor.monitor_processor import process_message
from API.controller import RecursoEstadoMicro
from Modelos.modelos import db
import boto3
import time
import requests

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

def crear_registro_EstadoMicro():
    api_url = "http://127.0.0.1:5000/EstadoMicro"
    response = requests.post(api_url)
    return response

def start_monitoreo():
    contador = 0
    while(contador < 2):
        contador += 1
        time.sleep(5) 
        nuevo_EstadoMicro = crear_registro_EstadoMicro()
        print("nuevo_EstadoMicro: "+str(nuevo_EstadoMicro.json()))
        message_attributes={
            'Fuente': {
                'DataType': 'String',
                'StringValue': 'MONITOR'
            },
            'ID_Message': {
                'DataType': 'String',
                'StringValue': str(nuevo_EstadoMicro.json().get("id"))
            }
        }
        send_message_to_queue("Reportar estado de salud", message_attributes)
        time.sleep(5)
        messages = receive_messages_from_queue()
        for message in messages:
            process_message(message)
            message.delete()
        

app = Flask(__name__)
t = Thread(target=start_monitoreo)
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
api.add_resource(RecursoEstadoMicro, '/EstadoMicro')