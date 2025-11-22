from models.carpeta import Carpeta
from data_structures.arbol_carpetas import ArbolCarpetas


class GestorCarpetas:

    def crear_carpeta(self, usuario, nombre, padre='raiz'):

        arbol = ArbolCarpetas(usuario.raiz)

        if arbol.buscar_carpeta_recursiva(nombre):
            raise ValueError('La carpeta ya existe')

        carpeta_padre = arbol.buscar_carpeta_recursiva(padre)

        if carpeta_padre:
            nueva_carpeta = Carpeta(nombre, padre=padre)
            arbol.insertar_carpeta(carpeta_padre, nueva_carpeta)
            return nueva_carpeta
        else:
            raise ValueError('La carpeta padre no existe')

    def eliminar_carpeta(self, usuario, nombre):

        arbol = ArbolCarpetas(usuario.raiz)

        if arbol.eliminar_carpeta(nombre):
            return True

        return False

    def mover_mensaje(self, mensaje, carpeta_origen, carpeta_destino):

        arbol = ArbolCarpetas(carpeta_destino)
        if arbol.mover_mensaje(mensaje, carpeta_origen, carpeta_destino):
            return True
        else:
            return False

    def buscar_carpeta(self, usuario, nombre):

        arbol = ArbolCarpetas(usuario.raiz)
        return arbol.buscar_carpeta_recursiva(nombre)

    def listar_carpetas(self, usuario):

        arbol = ArbolCarpetas(usuario.raiz)
        arbol.listar_carpetas_recursivo(usuario.raiz)

    def obtener_arbol_carpetas(self, usuario):

        return ArbolCarpetas(usuario.raiz)