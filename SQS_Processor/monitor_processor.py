from random import random
from random import randrange
import requests

def process_message(message):
    print("Va a evaluar el mensaje")
    if(mensaje_desde_micro(message)):
        print("Se procesa mensaje desde el micro")
        id_micro = get_id_micro_mensaje(message)
        id_mensaje_micro = get_id_mensaje_micro(message)
        if(id_micro is not None and id_mensaje_micro is not None):
            api_url = "http://127.0.0.1:5000/EstadoMicroAct/"+str(id_mensaje_micro)
            estadoMicroAct = {
                'id_estado': id_mensaje_micro,
                'estado': "OK"
            }
            response = requests.put(api_url, estadoMicroAct)
            print("response: "+str(response))
    pass


def mensaje_desde_micro(message):
    atributos = message.message_attributes
    retorno = False
    for atributo in atributos:
        if(atributo == "Fuente"):
            elementos = atributos[atributo].items()
            for elemento in elementos:
                if(elemento[0] == "StringValue" and ("MICRO" in elemento[1])):
                    retorno = True
    return retorno

def get_id_micro_mensaje(message):
    atributos = message.message_attributes
    retorno = None
    for atributo in atributos:
        if(atributo == "Fuente"):
            elementos = atributos[atributo].items()
            for elemento in elementos:
                if(elemento[0] == "StringValue" and ("MICRO" in elemento[1])):
                    retorno = elemento[1].split("-")[1]
    return retorno

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