from data_structures.cola_prioridad import ColaPrioridad
from models.mensaje import Mensaje


def test_orden_prioridad():
    cola = ColaPrioridad()
    m1 = Mensaje("a", "b", "Baja", "c", prioridad=2)
    m2 = Mensaje("a", "b", "Alta", "c", prioridad=1)

    cola.encolar(m1)
    cola.encolar(m2)

    # Debe salir primero el de prioridad 1
    salida = cola.desencolar()
    assert salida.prioridad == 1
    assert salida.asunto == "Alta"