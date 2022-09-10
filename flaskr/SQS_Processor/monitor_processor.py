from random import random
from random import randrange

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