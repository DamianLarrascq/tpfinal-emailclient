class Carpeta:
    """
    Representa una carpeta que almacena mensajes de un usuario
    """

    def __init__(self, nombre, padre=None):
        """
        Inicializa una carpeta como un nodo del árbol con un nombre,
        una referencia a su padre y listas apra mensajes y subcarpetas.

        :param nombre: Nombre de la carpeta
        :param padre: Instancia de Carpeta que es el nodo superior
        """
        self.__nombre = nombre
        self.__mensajes = []
        self.__subcarpetas = []
        self.__padre = padre

    @property
    def nombre(self):
        """
        Getter de nombre de la carpeta

        :return: String con nombre de la carpeta
        """
        return self.__nombre

    # Métodos subcarpetas

    @property
    def subcarpetas(self):
        return self.__subcarpetas

    def agregar_subcarpeta(self, carpeta):
        """
        Agrega una isntancia de Carpeta como subcarpeta,
        estableciendo la relación padre-hijo.

        :param carpeta:
        """
        if isinstance(carpeta, Carpeta):
            carpeta.__padre = self
            self.__subcarpetas.append(carpeta)
        else:
            raise TypeError('Solo se pueden agregar objetos Carpeta como subcarpeta')

    def obtener_subcarpeta(self, nombre):
        """
        Busca y devuelve una subcarpeta directamente por nombre.

        :param nombre: Nombre de la subcarpeta a buscar
        :return: Instancia de Carpeta si se encuentra, None en caso contrario.
        """
        for sub in self.subcarpetas:
            if sub.nombre == nombre:
                return sub
        return None

    def eliminar_subcarpeta(self, carpeta):
        try:
            self.__subcarpetas.remove(carpeta)
            return 'Subcarpeta eliminada con exito'
        except ValueError:
            raise ValueError('Error al eliminar subcarpeta')

    # Métodos mensajes

    @property
    def obtener_mensajes(self):
        """
        Devuelve todos los mensajes almacenados en la carpeta

        :return: Lista de instancias de Mensaje
        """
        return self.__mensajes

    def agregar_mensaje(self, mensaje):
        """
        Agrega un mensaje a la carpeta

        :param mensaje: Instancia de Mensaje
        """
        self.__mensajes.append(mensaje)

    def _buscar_mensaje_recursivo(self, termino_busqueda, campo=None):
        """
        Método que implementa la lógica recursiva de búsqueda.
        Busca mensajes en una carpeta y en sus subcarpetas.

        :param termino_busqueda: String a buscar
        :param campo: Campo de búsqueda ('asunto' o 'remitente'). Si es None busca en ambos
        :return: Lista de instancias de Mensaje que contienen el término
        """
        resultados = []
        termino = termino_busqueda.lower()

        for mensaje in self.__mensajes:

            es_asunto = termino in mensaje.asunto.lower()
            es_remitente = termino in mensaje.remitente.lower()

            if campo is None and (es_asunto or es_remitente):
                resultados.append(mensaje)

            elif campo == 'asunto' and termino in mensaje.asunto.lower():
                resultados.append(mensaje)

            elif campo == 'remitente' and termino in mensaje.remitente.lower():
                resultados.append(mensaje)

        for subcarpeta in self.__subcarpetas:
            total_mensajes = subcarpeta._buscar_mensaje_recursivo(termino_busqueda, campo)
            resultados.extend(total_mensajes)

        return resultados

    def buscar_mensaje(self, termino_busqueda, campo=None):
        """
        Inicia el proceso de búsqueda recursiva de mensajes en una carpeta y sus subcarpetas

        :param termino_busqueda: String a buscar
        :param campo: Campo de búsqueda ('asunto' o 'remitente'). Si es None busca en ambos
        :return: Lista de instancias de Mensaje que contienen el término
        """
        return self._buscar_mensaje_recursivo(termino_busqueda, campo)

    def eliminar_mensaje(self, mensaje):
        try:
            self.__mensajes.remove(mensaje)
            return 'Mensaje eliminado con exito'
        except ValueError:
            raise ValueError('Error al eliminar mensaje')
