from random import random
import boto3
import datetime
from random import randrange
from ..modelos import db, FallaMicro

def process_message(message):
    print(f"Procesando mensaje: {message.body}")
    esMonitor = mensaje_desde_monitor(message)
    # print("es monitor")
    # print(str(esMonitor))
    if(esMonitor):
        idMensaje = get_id_mensaje_micro(message)
        print("id mensaje")
        print(str(idMensaje))
        return str(idMensaje)
    else:
        return None


def get_id_mensaje_micro(message):
    atributos = message.message_attributes
    retorno = None
    for atributo in atributos:
        if(atributo == "ID_Mensaje"):
            elementos = atributos[atributo].items()
            for elemento in elementos:
                if(elemento[0] == "StringValue"):
                    retorno = int(elemento[1])
    return retorno

def mensaje_desde_monitor(message):
    atributos = message.message_attributes
    retorno = False
    for atributo in atributos:
        if(atributo == "Fuente"):
            elementos = atributos[atributo].items()
            for elemento in elementos:
                if(elemento[0] == "StringValue" and ("MONITOR" in elemento[1])):
                    retorno = True
    return retorno

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
