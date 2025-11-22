from data_structures.grafo_servidores import GrafoServidores

class GestorRed:

    def __init__(self):
        self.grafo = GrafoServidores()

    def agregar_servidor(self, servidor):

        resultado = self.grafo.agregar_servidor(servidor)
        return resultado

    def conectar_servidores(self, servidor1, servidor2, peso=1):

        nombre1 = servidor1.nombre if hasattr(servidor1, 'nombre') else servidor1
        nombre2 = servidor2.nombre if hasattr(servidor2, 'nombre') else servidor2

        resultado = self.grafo.conectar_servidor(nombre1, nombre2, peso)
        return resultado

    def enviar_mensaje_red(self, mensaje, servidor_origen, servidor_destino):

        ruta = self.encontrar_mejor_ruta(servidor_origen, servidor_destino)

        if not ruta:
            raise ValueError('Ruta no disponible')

        if isinstance(servidor_destino, str):
            servidor_destino = self.grafo.__servidores.get(servidor_destino)

        if servidor_destino:
            return servidor_destino.recibir_mensaje_local(mensaje)
        else:
            return False

    def encontrar_mejor_ruta(self, servidor_origen, servidor_destino):

        ruta = self.grafo.encontrar_ruta_bfs(servidor_origen, servidor_destino)
        return ruta

    def verificar_conectividad(self, servidor1, servidor2):

        ruta = self.grafo.encontrar_ruta_dfs(servidor1, servidor2)
        conectados = len(ruta) > 0

        return conectados
