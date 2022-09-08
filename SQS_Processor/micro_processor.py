from random import random
import boto3
import datetime
from random import randrange
from Modelos.modelos import db, FallaMicro

sqs_report = boto3.resource("sqs", region_name="us-east-1",
                            aws_access_key_id="AKIA6QD43RTCVK6T5IIY",
                            aws_secret_access_key="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")
queue_report = sqs_report.get_queue_by_name(QueueName="ColaRespuestasMonitoreo")

def process_message(message):
    print(f"Procesando mensaje: {message.body}")
    if(mensaje_desde_monitor(message)):
        estado_servicio = validar_servicio()
        if(estado_servicio == "OK"):
            message_to_queue(estado_servicio)
    pass

def mensaje_desde_monitor(message):
    atributos = message.message_attributes
    for atributo in atributos:
        if(atributo == "Fuente"):
            elementos = atributos[atributo].items()
            for elemento in elementos:
                if(elemento[0] == "StringValue" and elemento[1] == "MONITOR"):
                    return True
    return False

def validar_servicio():
    ## Si es par falla
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
    
    pass