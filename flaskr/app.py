import datetime
from flaskr import create_app
from flaskr.modelos.modelos import FallaMicro
from .modelos import db, ReglaMonitoreo, ReglaMonitoreoSchema
from flask_restful import Api
from .vistas import VistaReglaMonitoreo
from SQS_Processor.micro_processor import process_message
import boto3
from flask import Flask
from threading import Thread
from flask_cors import CORS
from random import randrange

sqs = boto3.resource("sqs", region_name="us-east-1",
                            aws_access_key_id="AKIA6QD43RTCWNJOXMKG",
                            aws_secret_access_key="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")
queue = sqs.get_queue_by_name(QueueName="https://sqs.us-east-1.amazonaws.com/996694265029/ColaMonitoreo")

def start_message_consumer():
    while(True): 
        messages = queue.receive_messages(MessageAttributeNames=['All'])
        for message in messages:
            idMensaje = process_message(message)
            print("id mensaje = "+idMensaje+ " fecha = "+ str(datetime.datetime.now))
            generate_response(idMensaje)
            message.delete()


def send_message_to_queue(message, message_attributes):
    print("Enviando mensaje: "+message)
    print("Atributos: "+str(message_attributes))
    sqs_client = boto3.client("sqs", region_name="us-east-1", 
    aws_access_key_id="AKIA6QD43RTC5J4ZSLPW", aws_secret_access_key="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"
    )
    response = sqs_client.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/996694265029/ColaMonitoreo",
        MessageBody = message,
        MessageAttributes = message_attributes
    )
    print("Respuesta cola: "+str(response))
    pass

def generate_response(idmensaje):

    estatus
    if(randrange(10)%2 == 0):
        estatus = 'OK'
    else:
        estatus = 'NOT OK'

    print('status: '+ estatus)
    if(estatus == 'OK'):
        message_attributes={
                'Fuente': {
                    'DataType': 'String',
                    'StringValue': 'MICRO-1'
                },
                'ID_Message': {
                    'DataType': 'String',
                    'StringValue': idmensaje
                }
            }
        send_message_to_queue("OK", message_attributes)
    else:  
        nueva_falla_servicio = FallaMicro(
                fecha = datetime.datetime.now,
                status = estatus,
                idMensaje = idmensaje
            )
        db.session.add(nueva_falla_servicio)
        db.session.commit()

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
