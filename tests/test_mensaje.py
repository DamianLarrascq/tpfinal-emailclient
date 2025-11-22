from models.mensaje import Mensaje

def test_propiedades_mensaje():
    msg = Mensaje("a@a.com", "b@b.com", "Hola", "Mundo", prioridad=2)
    assert msg.leido is False
    msg.marcar_como_leido()
    assert msg.leido is True

def test_comparacion_prioridad():
    # Prioridad 1 (Alta) < Prioridad 2 (Baja) para efectos de ordenamiento/heap
    msg_urgente = Mensaje("a", "b", "U", "C", prioridad=1)
    msg_normal = Mensaje("a", "b", "N", "C", prioridad=2)
    assert msg_urgente < msg_normal