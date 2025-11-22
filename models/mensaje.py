from datetime import datetime

class Mensaje:
    """
    Representa un mensaje de correo

    Cada instancia de mensaje tiene:
    - Remitente
    - Destinatario
    - Asunto
    - Cuerpo
    """
    def __init__(self, remitente, destinatario, asunto, cuerpo, prioridad = 2):
        """
        Inicializa un mensaje con remitente, destinatario, asunto, cuerpo

        :param remitente: Dirección de correo del remitente
        :param destinatario: Dirección de correo del destinatario
        :param asunto: Asunto del mensaje
        :param cuerpo: Cuerpo del mensaje
        :param prioridad=2: Nivel de prioridad del mensaje: 1 (alta) y 2 (normal)
        """
        self.__remitente = remitente
        self.__destinatario = destinatario
        self.__asunto = asunto
        self.__cuerpo = cuerpo
        self.__fecha = datetime.now()
        self.__prioridad = prioridad
        self.__leido = False
        self.__etiquetas = []

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

    @property
    def fecha(self):
        return self.__fecha

    @property
    def prioridad(self):
        return self.__prioridad

    @property
    def leido(self):
        return self.__leido

    def marcar_como_leido(self):
        self.__leido = True

    def agregar_etiqueta(self, etiqueta):
        if etiqueta not in self.__etiquetas:
            self.__etiquetas.append(etiqueta)

    def cambiar_prioridad(self, nueva_prioridad):
        self.__prioridad = nueva_prioridad

    def __lt__(self, other):
        """
        Compara prioridad de mensajes en la Cola
        """
        return self.prioridad < other.prioridad