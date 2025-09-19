from abc import ABC, abstractmethod


class InterfazCorreo(ABC):
    """
    Interfaz abstracta para el servidor de correo.

    Define los métodos necesarios para que cualquier implementación de servidor de correo debe cumplir:

    - enviar_mensaje: Entregar un mensaje a un destinatario
    - recibir_mensajes: Obtener un mensaje recibido por un usuario
    - listar_mensaje: Lista los asuntos de los mensajes de un usuario
    """
    @abstractmethod
    def enviar_mensaje(self, mensaje, destinatario):
        """
        Se encarga de envíar un mensaje a un destinatario

        :param mensaje: Instancia de Mensaje a envíar
        :param destinatario: Correo del destinatario
        """
        pass

    @abstractmethod
    def recibir_mensajes(self, email_usuario):
        """
        Devuelve los mensajes de la bandeja de entrada de un usuario

        :param email_usuario: Correo del usuario
        :return: Lista de instancias de Mensaje
        """
        pass

    @abstractmethod
    def listar_mensajes(self, usuario):
        """
        Devuelve los asuntos de los mensajes de un usuario

        :param usuario: Correo del usuario
        :return: Lista de strings con los asuntos
        """
        pass


class Usuario:
    """
    Representa un usuario dentro del sistema de correo

    Cada instancia tiene:
    - Nombre de usuario
    - Dirección de correo única
    - Un diccionario con carpetas "inbox" y "sent"
    """

    def __init__(self, nombre_usuario, correo):
        """
        Inicializa un usuario con un diccionario de carpetas por defecto: "inbox" y "sent"

        :param nombre_usuario: Nombre del usuario
        :param correo: Dirección de correo única para cada usuario
        """
        self.__nombre_usuario = nombre_usuario
        self.__correo = correo
        self.__carpetas = {"inbox": Carpeta("inbox"), "sent": Carpeta("sent")}

    def agregar_carpeta(self, nombre_carpeta):
        """
        Agrega una nueva carpeta al usuario

        :param nombre_carpeta: Nombre de la carpeta
        """
        self.__carpetas[nombre_carpeta] = Carpeta(nombre_carpeta)

    def obtener_carpeta(self, nombre_carpeta):
        """
        Devuelve la carpeta por nombre

        :param nombre_carpeta: Nombre de la carpeta
        :return: Instancia de Carpeta
        """
        return self.__carpetas.get(nombre_carpeta)

    @property
    def correo(self):
        """
        Getter para el correo del usuario

        :return: String con correo del usuario
        """
        return self.__correo

    def recibir_mensaje(self, mensaje):
        """
        Guarda un mensaje en la carpeta "inbox" del usuario

        :param mensaje: Instancia de Mensaje a almacenar
        """
        self.__carpetas["inbox"].agregar_mensaje(mensaje)

    def enviar_mensaje(self, mensaje):
        """
        Guarda un mensaje en la carpeta "sent" del usuario

        :param mensaje: Instancia de Mensaje a almacenar
        """
        self.__carpetas["sent"].agregar_mensaje(mensaje)


class Mensaje:
    """
    Representa un mensaje de correo

    Cada instancia de mensaje tiene:
    - Remitente
    - Destinatario
    - Asunto
    - Cuerpo
    """
    def __init__(self, remitente, destinatario, asunto, cuerpo):
        """
        Inicializa un mensaje con remitente, destinatario, asunto, cuerpo

        :param remitente: Dirección de correo del remitente
        :param destinatario: Dirección de correo del destinatario
        :param asunto: Asunto del mensaje
        :param cuerpo: Cuerpo del mensaje
        """
        self.__remitente = remitente
        self.__destinatario = destinatario
        self.__asunto = asunto
        self.__cuerpo = cuerpo

    @property
    def remitente(self):
        """
        Getter de remitente del mensaje

        :return: String con correo del remitente
        """
        return self.__remitente

    @property
    def destinatario(self):
        """
        Getter de destinatario del mensaje

        :return: String con correo del destinatario
        """
        return self.__destinatario

    @property
    def asunto(self):
        """
        Getter del asunto del mensaje

        :return: String con asunto del mensaje
        """
        return self.__asunto

    @property
    def cuerpo(self):
        """
        Getter del cuerpo del mensaje

        :return: String del cuerpo del mensaje
        """
        return self.__cuerpo


class Carpeta:
    """
    Representa una carpeta que almacena mensajes de un usuario
    """
    def __init__(self, nombre):
        """
        Inicializa una carpeta con un nombre y una lista vacía de mensajes

        :param nombre: Nombre de la carpeta
        """
        self.__nombre = nombre
        self.__mensajes = []

    def agregar_mensaje(self, mensaje):
        """
        Agrega un mensaje a la carpeta

        :param mensaje: Instancia de Mensaje
        """
        self.__mensajes.append(mensaje)

    def obtener_mensajes(self):
        """
        Devuelve todos los mensajes almacenados en la carpeta

        :return: Lista de instancias de Mensaje
        """
        return self.__mensajes

    @property
    def nombre(self):
        """
        Getter de nombre de la carpeta

        :return: String con nombre de la carpeta
        """
        return self.__nombre


class ServidorCorreo(InterfazCorreo):
    """
    Representa un servidor de correo

    Funciona como intermediario entre los usuarios
    - Gestiona el registro de usuarios
    - Se encarga de entregar mensajes a los destinatarios
    - Almacena copias en las carpetas correspondientes
    """

    def __init__(self):
        """
        Inicializa el servidor con un diccionario vacío de usuarios

        Key: Correo del usuario
        Value: Instancia de Usuario
        """
        self.__usuarios = {}

    @property
    def usuarios(self):
        """
        Getter de todos los usuarios registrados en el servidor

        :return: Diccionario {email: Usuario}
        """
        return self.__usuarios

    def registrar_usuario(self, usuario):
        """
        Registra un nuevo usuario en el diccionario del servidor

        :param usuario: Instancia de Usuario a registrar
        :raises ValueError: Si el usuario está registrado
        """
        if usuario in self.__usuarios:
            raise ValueError('Este usuario ya se encuentra registrado')
        self.__usuarios[usuario.traer_correo] = usuario

    def enviar_mensaje(self, mensaje, email_destinatario):
        """
        Envía un mensaje al destinatario y guarda una copia en "sent" del remitente

        :param mensaje: Instancia de Mensaje
        :param email_destinatario: Correo del destinatario
        :raises ValueError: Si el destinatario o remitente no están registrados
        """
        if email_destinatario not in self.__usuarios:
            raise ValueError('Destinatario no encontrado')

        destinatario = self.__usuarios[email_destinatario]
        destinatario.recibir_mensaje(mensaje)

        if mensaje.remitente not in self.__usuarios:
            raise ValueError('Remitente no encontrado')

        remitente = self.__usuarios[mensaje.remitente]
        remitente.enviar_mensaje(mensaje)

    def recibir_mensajes(self, email_usuario):
        """
        Devuelve los mensajes en la carpeta "inbox" de un usuario

        :param email_usuario: Correo del usuario
        :return: Lista de strings con los asuntos de los mensajes
        """
        usuario = self.__usuarios[email_usuario]
        return usuario.obtener_carpeta('inbox').obtener_mensajes()

    def listar_mensajes(self, usuario):
        """
        Devuelve los asuntos de los mensajes de un usuario

        :param usuario: Correo del usuario
        :return: Lista de strings con los asuntos de los mensajes
        """
        mensajes = self.recibir_mensajes(usuario)
        return [mensaje.asunto for mensaje in mensajes]
