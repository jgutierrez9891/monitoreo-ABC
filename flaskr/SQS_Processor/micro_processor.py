from random import random
import boto3
import datetime
from random import randrange
from modelos import db, FallaMicro

sqs_report = boto3.resource("sqs", region_name="us-east-1",
                            aws_access_key_id="",
                            aws_secret_access_key="")
queue_report = sqs_report.get_queue_by_name(QueueName="")

def process_message(message):
    print(f"Procesando mensaje: {message.body}")
    esMonitor = mensaje_desde_monitor(message)
    if(esMonitor):
        idMensaje = id_monitor(message)
        return idMensaje
    return 'N/A'

def id_monitor(message):
    atributos = message.message_attributes
    for atributo in atributos:
        if(atributo == "ID_Message"):
            elementos = atributos[atributo].items()
            for elemento in elementos:
                print(elemento[0])
                print(elemento[1])
                if(elemento[0] == "StringValue"):
                    return elemento[1]
    return False

def mensaje_desde_monitor(message):
    atributos = message.message_attributes
    for atributo in atributos:
        if(atributo == "Fuente"):
            elementos = atributos[atributo].items()
            for elemento in elementos:
                print(elemento[0])
                print(elemento[1])
                if(elemento[0] == "StringValue" and elemento[1] == "MONITOR"):
                    return True
    return False

def validar_servicio():
    ## Si es par falla
    print("Generar falla aleatoria en el microservicio")
    if(randrange(10)%2 == 0):
        nueva_falla_servicio = FallaMicro(
            fecha = datetime.datetime.now
        )
        db.session.add(nueva_falla_servicio)
        db.session.commit()
        return "ERROR"
    else:
        return "OK"

def message_to_queue(ID):
    print(f"Enviando mensaje CON ID: {ID}")
    response = queue_report.send_message(MessageBody = 'monitorear',
                    message_attributes={
                        'Fuente': {
                            'DataType': 'String',
                            'StringValue': 'MICRO-1'
                        },
                        'ID_Message': {
                            'DataType': 'String',
                            'StringValue': str(ID)
                        }
                    })
    print(response.get('MessageId'))