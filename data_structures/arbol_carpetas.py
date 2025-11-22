from models.carpeta import Carpeta


class ArbolCarpetas:

    def __init__(self, raiz):
        self.raiz = raiz

    def insertar_carpeta(self, padre, nueva_carpeta):

        if not isinstance(padre, Carpeta):
            raise ValueError('Carpeta padre debe ser instancia de Carpeta')

        padre.agregar_subcarpeta(nueva_carpeta)

    def eliminar_carpeta(self, nombre):

        if nombre == self.raiz.nombre:
            raise ValueError('No se puede eliminar la carpeta raiz')

        carpeta = self.buscar_carpeta_recursiva(nombre)

        if carpeta:
            padre = carpeta.padre
            if padre:
                padre.eliminar_subcarpeta(carpeta)
                return True
            else:
                raise ValueError('La carpeta no tiene padre asignado')

        return False

    def buscar_carpeta_recursiva(self, nombre, carpeta_actual=None):

        if carpeta_actual is None:
            carpeta_actual = self.raiz

        if carpeta_actual.nombre == nombre:
            return carpeta_actual

        for subcarpeta in carpeta_actual.subcarpetas:
            resultado = self.buscar_carpeta_recursiva(nombre, subcarpeta)
            if resultado:
                return resultado

        return None

    def mover_mensaje(self, mensaje, carpeta_origen, carpeta_destino):
        try:
            carpeta_origen.eliminar_mensaje(mensaje)
            carpeta_destino.agregar_mensaje(mensaje)
            return True
        except ValueError:
            return False

    def listar_carpetas_recursivo(self, carpeta_actual=None, nivel=0):

        if carpeta_actual is None:
            carpeta_actual = self.raiz

        indentacion = ' ' * nivel
        cantidad_mensajes = len(carpeta_actual.obtener_mensajes)

        print(f'{indentacion}[{carpeta_actual.nombre}] ({cantidad_mensajes} mensajes)')

        for subcarpeta in carpeta_actual.subcarpetas:
            self.listar_carpetas_recursivo(subcarpeta, nivel + 1)

    def obtener_profundidad(self, carpeta_actual=None):

        if carpeta_actual is None:
            carpeta_actual = self.raiz

        if not carpeta_actual.subcarpetas:
            return 1

        profundidad_hijos = [self.obtener_profundidad(subcarpeta) for subcarpeta in carpeta_actual.subcarpetas]

        return 1 + max(profundidad_hijos)

    def contar_mensajes_totales(self, carpeta_actual=None):

        if carpeta_actual is None:
            carpeta_actual = self.raiz

        cantidad = len(carpeta_actual.obtener_mensajes)

        for subcarpeta in carpeta_actual.subcarpetas:
            cantidad += self.contar_mensajes_totales(subcarpeta)

        return cantidad