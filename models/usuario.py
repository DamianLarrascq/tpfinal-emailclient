from carpeta import Carpeta

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
        self.__raiz_carpetas = Carpeta('raiz')
        self.__inbox = Carpeta('inbox', padre=self.__raiz_carpetas)
        self.__sent = Carpeta('sent', padre=self.__raiz_carpetas)
        self.__papelera = Carpeta('papelera', self.__raiz_carpetas)
        self.__raiz_carpetas.agregar_subcarpeta(self.__inbox)
        self.__raiz_carpetas.agregar_subcarpeta(self.__sent)
        self.__raiz_carpetas.agregar_subcarpeta(self.__papelera)
        self.__filtros = []

    @property
    def correo(self):
        """
        Getter para el correo del usuario

        :return: String con correo del usuario
        """
        return self.__correo

    @property
    def nombre(self):
        return self.__nombre_usuario

    @property
    def inbox(self):
        return self.__inbox

    @property
    def sent(self):
        return self.__sent

    @property
    def raiz(self):
        return self.__raiz_carpetas

    @property
    def filtros(self):
        return self.__filtros

    def recibir_mensaje(self, mensaje):
        """
        Guarda un mensaje en la carpeta "inbox" del usuario

        :param mensaje: Instancia de Mensaje a almacenar
        """
        self.__inbox.agregar_mensaje(mensaje)

    def enviar_mensaje(self, mensaje):
        """
        Guarda un mensaje en la carpeta "sent" del usuario

        :param mensaje: Instancia de Mensaje a almacenar
        """
        self.__sent.agregar_mensaje(mensaje)

    def agregar_filtro(self, filtro_config):
        self.__filtros.append(filtro_config)