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

    def __init__(self, nombre_usuario, correo):
        self.__nombre_usuario = nombre_usuario
        self.__correo = correo
        self.__carpetas = {"inbox": Carpeta("inbox"), "sent": Carpeta("sent")}

    def agregar_carpeta(self, nombre_carpeta):
        self.__carpetas[nombre_carpeta] = Carpeta(nombre_carpeta)

    def obtener_carpeta(self, nombre_carpeta):
        return self.__carpetas.get(nombre_carpeta)
    
    def traer_correo(self):
        return self.__correo
    
    def recibir_mensaje(self):
        pass

class Mensaje:
    pass


class Carpeta:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__mensajes = []

    def agregar_mensaje(self, mensaje):
        self.__mensajes.append(mensaje)

    def obtener_mensajes(self):
        return self.__mensajes
    
    def traer_nombre(self):
        return self.__nombre


class ServidorCorreo(InterfazCorreo):

    def __init__(self):
        pass

    def enviar_mensaje(self, mensaje, destinatario):
        pass

    def recibir_mensajes(self):
        pass

    def listar_mensajes(self):
        pass
