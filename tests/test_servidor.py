from models.servidor import ServidorCorreo
from models.usuario import Usuario
from models.mensaje import Mensaje


def test_registro_usuario():
    srv = ServidorCorreo("gmail.com")
    user = Usuario("Ana", "ana@gmail.com")
    srv.registrar_usuario(user)
    assert "ana@gmail.com" in srv.usuarios


def test_envio_local():
    srv = ServidorCorreo("local.com")
    u1 = Usuario("A", "a@local.com")
    u2 = Usuario("B", "b@local.com")
    srv.registrar_usuario(u1)
    srv.registrar_usuario(u2)

    msg = Mensaje("a@local.com", "b@local.com", "Hola", "Cuerpo")
    # Simulamos el envío directo
    srv.enviar_mensaje(msg, "b@local.com")

    assert len(u2.inbox.obtener_mensajes) == 1