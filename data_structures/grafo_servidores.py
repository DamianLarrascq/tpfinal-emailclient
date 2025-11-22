from time import sleep


class GrafoServidores:

    def __init__(self):

        self.__servidores = {}
        self.__adyacencia = {}

    def agregar_servidor(self, servidor):

        if servidor.nombre not in self.__servidores:
            self.__servidores[servidor.nombre] = servidor
            self.__adyacencia[servidor.nombre] = []
            return True

        return False

    def eliminar_servidor(self, servidor):

        nombre = servidor.nombre if hasattr(servidor, 'nombre') else servidor

        if nombre in self.__servidores:
            del self.__servidores[nombre]
            del self.__adyacencia[nombre]

            for nodo, vecinos in self.__adyacencia.items():
                self.__adyacencia[nodo] = [v for v in vecinos if v[0] != nombre]
            return True

        return False

    def conectar_servidores(self, servidor1, servidor2, peso=1):

        nombre1 = servidor1.nombre if hasattr(servidor1, 'nombre') else servidor1
        nombre2 = servidor2.nombre if hasattr(servidor2, 'nombre') else servidor2

        if nombre1 in self.__servidores and nombre2 in self.__servidores:
            vecinos1 = [v[0] for v in self.__adyacencia[nombre1]]

            if nombre2 not in vecinos1:
                self.__adyacencia[nombre1].append((nombre2, peso))
                self.__adyacencia[nombre2].append((nombre1, peso))
                return True
        return False

    def desconectar_servidores(self, servidor1, servidor2):

        nombre1 = servidor1.nombre if hasattr(servidor1, 'nombre') else servidor1
        nombre2 = servidor2.nombre if hasattr(servidor2, 'nombre') else servidor2

        if nombre1 in self.__adyacencia and nombre2 in self.__adyacencia:
            self.__adyacencia[nombre1] = [v for v in self.__adyacencia[nombre1] if v[0] != nombre2]
            self.__adyacencia[nombre2] = [v for v in self.__adyacencia[nombre2] if v[0] != nombre1]
            return True

        return False

    def encontrar_ruta_bfs(self, origen, destino):

        origen = origen.nombre if hasattr(origen, 'nombre') else origen
        destino = destino.nombre if hasattr(destino, 'nombre') else destino

        if origen not in self.__servidores or destino not in self.__servidores:
            return []

        cola = [[origen]]
        visitados = {origen}

        while len(cola) > 0:

            ruta_actual = cola.pop(0)
            nodo_final = ruta_actual[-1]

            if nodo_final == destino:
                return ruta_actual

            for vecino, peso in self.__adyacencia[nodo_final]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    nueva_ruta = list(ruta_actual)
                    nueva_ruta.append(vecino)
                    cola.append(nueva_ruta)

        return []

    def encontrar_ruta_dfs(self, origen, destino, visitados=None, ruta_actual=None):

        origen = origen.nombre if hasattr(origen, 'nombre') else origen
        destino = destino.nombre if hasattr(destino, 'nombre') else destino

        if origen not in self.__servidores or destino not in self.__servidores:
            return []

        if visitados is None:
            visitados = set()

        if ruta_actual is None:
            ruta_actual = []

        visitados.add(origen)
        ruta_actual.append(origen)

        if origen == destino:
            return list(ruta_actual)

        for vecino, peso in self.__adyacencia[origen]:
            if vecino not in visitados:
                resultado = self.encontrar_ruta_dfs(vecino, destino, visitados, ruta_actual)
                if resultado:
                    return resultado

        ruta_actual.pop()
        return []

    def servidores_alcanzables(self, origen):

        origen = origen.nombre if hasattr(origen, 'nombre') else origen
        if origen not in self.__servidores:
            return []

        alcanzables = []
        visitados = {origen}
        cola = [origen]

        while len(cola) > 0:
            nodo = cola.pop(0)
            alcanzables.append(nodo)

            for vecino, peso in self.__adyacencia[nodo]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)

        return alcanzables

    def es_conexo(self):

        if not self.__servidores:
            return True

        nodo_inicio = list(self.__servidores.keys())[0]
        alcanzables = self.servidores_alcanzables(nodo_inicio)

        return len(alcanzables) == len(self.__servidores)

    def obtener_componentes_conexas(self):

        visitados_globales = set()
        componentes = []

        for nombre in self.__servidores:
            if nombre not in visitados_globales:
                componente_actual = self.servidores_alcanzables(nombre)
                componentes.append(componente_actual)

                for nodo in componente_actual:
                    visitados_globales.add(nodo)

        return componentes

    def obtener_servidor(self, nombre_servidor):
        return self.__servidores.get(nombre_servidor)

    def obtener_todos_servidores(self):
        return list(self.__servidores.values())
