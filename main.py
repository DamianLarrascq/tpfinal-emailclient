from abc import ABC, abstractmethod


class InterfazCorreo(ABC):

    @abstractmethod
    def enviar_mensaje(self, mensaje, destinatario):
        pass

    @abstractmethod
    def recibir_mensajes(self, email_usuario):
        pass

    @abstractmethod
    def listar_mensajes(self, usuario):
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

    @property
    def traer_correo(self):
        return self.__correo

    def recibir_mensaje(self, mensaje):
        self.__carpetas["inbox"].agregar_mensaje(mensaje)

    def enviar_mensaje(self, mensaje):
        self.__carpetas["sent"].agregar_mensaje(mensaje)


class Mensaje:
    def __init__(self, remitente, destinatario, asunto, cuerpo):
        self.__remitente = remitente
        self.__destinatario = destinatario
        self.__asunto = asunto
        self.__cuerpo = cuerpo

    @property
    def remitente(self):
        return self.__remitente

    @property
    def destinatario(self):
        return self.__destinatario

    @property
    def asunto(self):
        return self.__asunto

    @property
    def cuerpo(self):
        return self.__cuerpo


class Carpeta:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__mensajes = []

    def agregar_mensaje(self, mensaje):
        self.__mensajes.append(mensaje)

    def obtener_mensajes(self):
        return self.__mensajes

    @property
    def traer_nombre(self):
        return self.__nombre


class ServidorCorreo(InterfazCorreo):

    def __init__(self):
        self.__usuarios = {}

    @property
    def traer_usuarios(self):
        return self.__usuarios

    def registrar_usuario(self, usuario):
        if usuario in self.__usuarios:
            raise ValueError('Este usuario ya se encuentra registrado')
        self.__usuarios[usuario.traer_correo] = usuario

    def enviar_mensaje(self, mensaje, email_destinatario):
        if email_destinatario not in self.__usuarios:
            raise ValueError('Destinatario no encontrado')

        destinatario = self.__usuarios[email_destinatario]
        destinatario.recibir_mensaje(mensaje)

        if mensaje.remitente not in self.__usuarios:
            raise ValueError('Remitente no encontrado')

        remitente = self.__usuarios[mensaje.remitente]
        remitente.enviar_mensaje(mensaje)

    def recibir_mensajes(self, email_usuario):
        usuario = self.__usuarios[email_usuario]
        return usuario.obtener_carpeta('inbox').obtener_mensajes()

    def listar_mensajes(self, usuario):
        mensajes = self.recibir_mensajes(usuario)
        return [mensaje.asunto for mensaje in mensajes]
