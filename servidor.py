from abc import ABC, abstractmethod


class InterfazCorreo(ABC):
    """
    Interfaz abstracta para el servidor de correo.

    Define los métodos necesarios para que cualquier implementación de servidor de correo debe cumplir:

    - enviar_mensaje: Entregar un mensaje a un destinatario
    - recibir_mensajes: Obtener un mensaje recibido por un usuario
    - listar_mensaje: Lista los asuntos de los mensajes de un usuario
    - buscar_mensaje: Busca un mensaje recursivamente del usuario dado
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

    @abstractmethod
    def buscar_mensaje(self, email_usuario, termino_busqueda, campo=None):
        """
        Busca un mensaje recursivamente en todas las carpetas del usuario dado.

        :param email_usuario: Correo del usuario que realiza la búsqueda
        :param termino_busqueda: String a buscar en los mensajes
        :param campo: Campo de búsqueda ('asunto' o 'remitente'). Si es None busca en ambos
        :return: Lista de instancias de Mensaje que contienen el término
        """
        pass


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
        self.__usuarios[usuario.correo] = usuario

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

    def buscar_mensaje(self, email_usuario, termino_busqueda, campo=None):
        """
        Delega la búsqueda recursiva de mensajes al usuario, asegurando que esté registrado.

        :param email_usuario: Correo del usuario que realiza la búsqueda
        :param termino_busqueda: String a bsucar en los mensajes
        :param campo: Campo de búsqueda ('asunto' o 'remitente'). Si es None busca en ambos
        :return: Lista de instancias de Mensaje que contienen el término
        """
        if email_usuario not in self.__usuarios:
            raise ValueError('Usuario no encontrado')

        usuario = self.__usuarios[email_usuario]

        return usuario.buscar_mensaje(termino_busqueda, campo)
