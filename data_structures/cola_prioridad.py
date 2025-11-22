class Nodo:
    def __init__(self, mensaje):
        self.mensaje = mensaje
        self.siguiente = None


class ColaPrioridad:
    def __init__(self):
        self.cabeza = None

    def encolar(self, mensaje):

        nuevo_nodo = Nodo(mensaje)
        nueva_prioridad = mensaje.prioridad

        if self.cabeza is None or nueva_prioridad < self.cabeza.mensaje.prioridad:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
            return

        actual = self.cabeza

        while actual.siguiente is not None and actual.siguiente.mensaje.prioridad <= nueva_prioridad:
            actual = actual.siguiente

        nuevo_nodo.siguiente = actual.siguiente
        actual.siguiente = nuevo_nodo

    def desencolar(self):

        if self.cabeza is None:
            return None

        mensaje = self.cabeza.mensaje
        self.cabeza = self.cabeza.siguiente

        return mensaje

    def esta_vacia(self):
        return self.cabeza is None