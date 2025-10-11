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