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
        self.__inbox = Carpeta('inbox')
        self.__sent = Carpeta('sent')
        self.__raiz_carpetas.agregar_subcarpeta(self.__inbox)
        self.__raiz_carpetas.agregar_subcarpeta(self.__sent)
        self.__filtros = {}

    @property
    def correo(self):
        """
        Getter para el correo del usuario

        :return: String con correo del usuario
        """
        return self.__correo

    # Métodos filtros

    def definir_filtro(self, nombre_filtro, campo, valor, carpeta_destino):

        if campo not in ['remitente', 'asunto']:
            raise ValueError('Campo debe ser "remitente" o "asunto"')

        if not self.obtener_carpeta(carpeta_destino):
            raise ValueError('Carpeta de destino no encontrada')

        self.__filtros[nombre_filtro]= {
            'campo': campo,
            'valor': valor.lower(),
            'destino': carpeta_destino
        }

    def aplicar_filtros(self, mensaje):

        mensaje_movido = False

        for nombre_filtro, regla in self.__filtros.items():

            campo_mensaje = None
            if regla['campo'] == 'remitente':
                campo_mensaje = mensaje.remitente.lower()
            elif regla['campo'] == 'asunto':
                campo_mensaje = mensaje.asunto.lower()

            if campo_mensaje and regla['valor'] in campo_mensaje:

                carpeta_destino = self.obtener_carpeta(regla['destino'])
                carpeta_destino.agregar_mensaje(mensaje)
                mensaje_movido = True

                break

        return mensaje_movido

    # Métodos carpetas

    def agregar_carpeta(self, nombre_carpeta, nombre_carpeta_raiz='raiz'):
        """
        Agrega una neuva carpeta al usuario bajo la carpeta padre especificada.

        :param nombre_carpeta: Nombre de la nueva carpeta
        :param nombre_carpeta_raiz: Nombre de la carpeta padre donde se va a agregar. Por defecto 'raiz'
        :return: Instancia de la nueva Carpeta creada.
        """
        raiz = self.obtener_carpeta(nombre_carpeta_raiz)

        if not raiz:
            raise ValueError('Carpeta raiz no encontrada')

        if raiz.obtener_subcarpeta(nombre_carpeta):
            raise ValueError('Ya existe una carpeta con ese nombre')

        nueva_carpeta = Carpeta(nombre_carpeta)
        raiz.agregar_subcarpeta(nueva_carpeta)
        return nueva_carpeta

    def _obtener_carpeta_recursiva(self, carpeta_actual, nombre_carpeta):
        """
        Método que busca una carpeta por nombre recorriendo el árbol recursivamente.

        :param carpeta_actual: Instancia de Carpeta (nodo actual) desde donde se inicia la búsqueda
        :param nombre_carpeta: Nombre de la carpeta a buscar
        :return: Instancia de Carpeta si se encuentra, None en caso contrario
        """
        if carpeta_actual is None:
            return None

        if carpeta_actual.nombre == nombre_carpeta:
            return carpeta_actual

        for subcarpeta in carpeta_actual.subcarpetas:
            resultado = self._obtener_carpeta_recursiva(subcarpeta, nombre_carpeta)
            if resultado:
                return resultado

        return None

    def obtener_carpeta(self, nombre_carpeta):
        """
        Devuelve la carpeta por nombre, iniciando la búsqueda recursiva desde la raíz

        :param nombre_carpeta: Nombre de la carpeta
        :return: Instancia de Carpeta si se encuentra, None en caso contrario
        """
        return self._obtener_carpeta_recursiva(self.__raiz_carpetas, nombre_carpeta)

    def _obtener_carpeta_padre_recursiva(self, carpeta_actual, carpeta_hijo):

        for subcarpeta in carpeta_actual.subcarpetas:
            if subcarpeta.nombre == carpeta_hijo:
                return carpeta_actual

        for subcarpeta in carpeta_actual.subcarpetas:
            resultado = self._obtener_carpeta_padre_recursiva(subcarpeta, carpeta_hijo)

            if resultado:
                return resultado

        return None

    def mover_carpeta(self, carpeta, destino):
        carpeta = self.obtener_carpeta(carpeta)
        destino = self.obtener_carpeta(destino)

        if not carpeta or carpeta.nombre in ['raiz', 'inbox', 'sent']:
            raise ValueError('No se encontro la carpeta o es una carpeta protegida')

        if not destino:
            raise ValueError('Carpeta destino no encontrada')

        padre_actual = self._obtener_carpeta_padre_recursiva(self.__raiz_carpetas, carpeta.nombre)

        if not padre_actual:
            raise ValueError('No se encontro carpeta padre')

        padre_actual.eliminar_subcarpeta(carpeta)
        destino.agregar_subcarpeta(carpeta)

    # Métodos mensajes

    def buscar_mensaje(self, termino_busqueda, campo=None):
        """
        Delega la búsqueda recursiva de mensajes a la carpeta raíz del usuario.

        :param termino_busqueda: String a buscar en los mensajes
        :param campo: Campo de búsqueda ('asunto' o 'remitente'). Si es None busca en ambos
        :return: Lista de instancias de Mensaje que contienen el término
        """
        return self.__raiz_carpetas.buscar_mensaje(termino_busqueda, campo)


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

    def mover_mensaje(self, mensaje, origen, destino):

        origen = self.obtener_carpeta(origen)
        destino = self.obtener_carpeta(destino)

        if not origen:
            raise ValueError('Carpeta de origen no encontrada')

        if not destino:
            raise ValueError('Carpeta de destino no encontrada')

        try:
            origen.eliminar_mensaje(mensaje)
            destino.agregar_mensaje(mensaje)

        except:
            raise ValueError('No se pudo mover el mensaje')