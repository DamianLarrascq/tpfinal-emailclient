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

    def eliminar_mensaje(self, mensaje_a_eliminar):

        actual = self.cabeza
        anterior = None

        if actual is not None and actual.mensaje is mensaje_a_eliminar:
            self.cabeza = actual.siguiente
            return True

        while actual is not None and actual.mensaje is not mensaje_a_eliminar:
            anterior = actual
            actual = actual.siguiente

        if actual is not None:
            anterior.siguiente = actual.siguiente
            return True

        return False

    def cambiar_prioridad(self, mensaje, nueva_prioridad):
        eliminado = self.eliminar_mensaje(mensaje)

        if not eliminado:
            return False

        mensaje.cambiar_prioridad(nueva_prioridad)

        self.encolar(mensaje)

        return True