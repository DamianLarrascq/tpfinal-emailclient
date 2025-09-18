from abc import ABC, abstractmethod


class InterfazCorreo(ABC):

    @abstractmethod
    def enviar_mensaje(self, mensaje, destinatario):
        pass

    @abstractmethod
    def recibir_mensajes(self):
        pass

    @abstractmethod
    def listar_mensajes(self):
        pass


class Usuario:

    pass

class Mensaje:
    pass


class Carpeta:
    pass


class ServidorCorreo(InterfazCorreo):

    def __init__(self):
        pass

    def enviar_mensaje(self, mensaje, destinatario):
        pass

    def recibir_mensajes(self):
        pass

    def listar_mensajes(self):
        pass
