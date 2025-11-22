from data_structures.grafo_servidores import GrafoServidores


class MockServidor:
    def __init__(self, nombre): self.nombre = nombre


def test_camino_bfs():
    grafo = GrafoServidores()
    s1 = MockServidor("A")
    s2 = MockServidor("B")
    s3 = MockServidor("C")

    grafo.agregar_servidor(s1)
    grafo.agregar_servidor(s2)
    grafo.agregar_servidor(s3)

    # A -> B -> C
    grafo.conectar_servidores(s1, s2)
    grafo.conectar_servidores(s2, s3)

    ruta = grafo.encontrar_ruta_bfs("A", "C")
    assert ruta == ["A", "B", "C"]


def test_es_conexo():
    grafo = GrafoServidores()
    s1 = MockServidor("A")
    s2 = MockServidor("B")
    grafo.agregar_servidor(s1)
    grafo.agregar_servidor(s2)

    assert grafo.es_conexo() is False  # No hay arista

    grafo.conectar_servidores(s1, s2)
    assert grafo.es_conexo() is True