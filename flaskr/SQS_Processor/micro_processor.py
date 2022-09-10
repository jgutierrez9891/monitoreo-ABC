from random import random
import boto3
import datetime
from random import randrange
from Modelos.modelos import db, FallaMicro

sqs_report = boto3.resource("sqs", region_name="us-east-1",
                            aws_access_key_id="",
                            aws_secret_access_key="")
queue_report = sqs_report.get_queue_by_name(QueueName="")

def process_message(message):
    print(f"Procesando mensaje: {message.body}")
    if(mensaje_desde_monitor(message)):
        estado_servicio = validar_servicio()
        if(estado_servicio == "OK"):
            print("Se envía mensaje de estado")
            message_to_queue(estado_servicio)
    pass

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

def message_to_queue(message):
    print(f"Enviando mensaje: {message}")
    response = queue_report.send_message(MessageBody = 'monitorear',
                    MessageAttributes={
                        'Fuente':{
                            'StringValue': 'MICRO',
                            'DataType': 'String'
                        }
                    })
    print(response.get('MessageId'))