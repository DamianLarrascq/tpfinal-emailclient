from models.carpeta import Carpeta
from models.mensaje import Mensaje


def test_agregar_y_eliminar_mensaje():
    carpeta = Carpeta("Trabajo")
    msg = Mensaje("a", "b", "Asunto", "Cuerpo")

    carpeta.agregar_mensaje(msg)
    assert len(carpeta.obtener_mensajes) == 1

    carpeta.eliminar_mensaje(msg)
    assert len(carpeta.obtener_mensajes) == 0


def test_busqueda_recursiva_interna():
    raiz = Carpeta("Raiz")
    hija = Carpeta("Hija", padre=raiz)
    raiz.agregar_subcarpeta(hija)

    msg = Mensaje("x", "y", "Secreto", "Contenido")
    hija.agregar_mensaje(msg)

    # Buscar desde la raíz debe encontrar el mensaje en la hija
    encontrados = raiz.buscar_mensaje("Secreto", campo="asunto")
    assert len(encontrados) == 1
    assert encontrados[0].asunto == "Secreto"