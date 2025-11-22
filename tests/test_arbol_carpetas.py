from models.carpeta import Carpeta
from data_structures.arbol_carpetas import ArbolCarpetas


def test_estructura_arbol():
    raiz = Carpeta("Raiz")
    arbol = ArbolCarpetas(raiz)

    sub1 = Carpeta("Docs")
    arbol.insertar_carpeta(raiz, sub1)

    encontrada = arbol.buscar_carpeta_recursiva("Docs")
    assert encontrada is not None
    assert encontrada.padre == raiz


def test_profundidad():
    raiz = Carpeta("R")
    arbol = ArbolCarpetas(raiz)
    sub1 = Carpeta("N1", padre=raiz)
    sub2 = Carpeta("N2", padre=sub1)

    arbol.insertar_carpeta(raiz, sub1)
    arbol.insertar_carpeta(sub1, sub2)

    assert arbol.obtener_profundidad() == 3