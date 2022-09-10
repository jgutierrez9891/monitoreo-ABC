from random import random
from random import randrange
from Modelos.modelos import EstadoMicro, db

def process_message(message):
    if(mensaje_desde_micro(message)):
        id_micro = id_micro_mensaje(message)
        id_mensaje_micro = id_mensaje_micro(message)
        if(id_micro is not None and id_mensaje_micro is not None):
            registro_estado_micro = EstadoMicro.query.filter(EstadoMicro.id_micro == id_micro, EstadoMicro.id == id_mensaje_micro).first()
            if(registro_estado_micro is not None):
                registro_estado_micro.estado = "OK"
                db.session.commit()


def mensaje_desde_micro(message):
    atributos = message.message_attributes
    for atributo in atributos:
        if(atributo == "Fuente"):
            elementos = atributos[atributo].items()
            for elemento in elementos:
                if(elemento[0] == "StringValue" and ("MICRO" in elemento[1])):
                    return True
    return False

def id_micro_mensaje(message):
    atributos = message.message_attributes
    for atributo in atributos:
        if(atributo == "Fuente"):
            elementos = atributos[atributo].items()
            for elemento in elementos:
                if(elemento[0] == "StringValue" and ("MICRO" in elemento[1])):
                    return elemento[1].split("-")[1]
    return None

def id_mensaje_micro(message):
    atributos = message.message_attributes
    for atributo in atributos:
        if(atributo == "ID_Mensaje"):
            elementos = atributos[atributo].items()
            for elemento in elementos:
                if(elemento[0] == "StringValue"):
                    return elemento[1]
    return None