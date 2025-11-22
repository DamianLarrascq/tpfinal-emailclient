from models.usuario import Usuario

def test_creacion_usuario():
    user = Usuario("Pepe", "pepe@test.com")
    assert user.nombre == "Pepe"
    assert user.correo == "pepe@test.com"
    # Verifica carpetas por defecto
    assert user.inbox.nombre == "inbox"
    assert user.sent.nombre == "sent"
    assert user.obtener_carpeta("papelera") is not None

def test_agregar_filtro():
    user = Usuario("Pepe", "pepe@test.com")
    filtro = {"id": "1", "nombre": "Test", "criterio": "asunto", "valor": "hola", "accion": "leer"}
    user.agregar_filtro(filtro)
    assert len(user.filtros) == 1
    assert user.filtros[0]['nombre'] == "Test"