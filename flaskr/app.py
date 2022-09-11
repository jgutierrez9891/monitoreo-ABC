from .modelos import db, ReglaMonitoreo, ReglaMonitoreoSchema, FallaMicro
import datetime
from flaskr import create_app
from flask_restful import Api
from .vistas import VistaReglaMonitoreo
from .SQS_Processor.micro_processor import process_message
import boto3
from flask import Flask
from threading import Thread
from flask_cors import CORS
from random import randrange
from .API.controller import RecursoEstado
import requests

sqs = boto3.resource("sqs", region_name="us-east-1",
                            aws_access_key_id="AKIA6QD43RTC4JQPPCJK",
                            aws_secret_access_key="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")
queue = sqs.get_queue_by_name(QueueName="ColaMonitoreo")

def start_message_consumer():
    print("queue")
    print(queue)
    while(True): 
        print("inside while")
        messages = queue.receive_messages(MessageAttributeNames=['All'])
        for message in messages:
            print("message ="+ str(message))
            idMensaje = process_message(message)
            print("id mensaje = "+str(idMensaje)+ " fecha = "+ str(datetime.datetime.now))
            if(idMensaje is not None):
                generate_response(idMensaje)
            message.delete()

def send_message_to_queue(message, message_attributes):
    print("Enviando mensaje: "+message)
    print("Atributos: "+str(message_attributes))
    sqs_client = boto3.client("sqs", region_name="us-east-1", 
    aws_access_key_id="AKIA6QD43RTC4JQPPCJK", aws_secret_access_key="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"
    )
    response = sqs_client.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/996694265029/ColaRespuestasMonitoreo",
        MessageBody = message,
        MessageAttributes = message_attributes
    )
    print("Respuesta cola: "+str(response))
    pass

def generate_response(idmensaje):

    estatus =''
    if( randrange(10) % 5 ==0 ):
        estatus = 'NOT OK'
    else:
        estatus = 'OK'

    print('status: '+ estatus)
    if(estatus == 'OK'):
        message_attributes={
                'Fuente': {
                    'DataType': 'String',
                    'StringValue': 'MICRO-1'
                },
                'ID_Mensaje': {
                    'DataType': 'String',
                    'StringValue': idmensaje
                }
            }
        send_message_to_queue("OK", message_attributes)
    else:  
        api_url = "http://127.0.0.1:5000/Falla/"+str(idmensaje)
        print('api_url')
        print(api_url)
        response = requests.get(api_url)
        print("response: "+str(response))


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
api.add_resource(RecursoEstado, '/Falla/<int:id_estado>')
