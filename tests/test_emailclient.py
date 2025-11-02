import unittest
from usuario import Usuario
from mensaje import Mensaje
from cola_prioridad import ColaPrioridad, Nodo

class TestRecursividad(unittest.TestCase):

    def setUp(self):
        """
        Crea un usuario con una estructura de carpetas anidadas
        """
        self.user = Usuario("UsuarioUno", "usuariouno@test.com")
        self.user.agregar_carpeta("Personal", "inbox")
        self.user.agregar_carpeta("Trabajo", "Personal")
        self.user.agregar_carpeta("Viajes", "Trabajo")

        # Mensajes
        self.msg_viajes = Mensaje("amigo@viajes.com", "test@servidor.com", "Vacaciones 2024", "...")
        self.msg_trabajo = Mensaje("jefe@empresa.com", "test@servidor.com", "Informe Final", "...")
        self.msg_inbox = Mensaje("info@promo.com", "test@servidor.com", "Nueva Oferta", "...")

        # Almacenar mensajes en sus carpetas
        self.user.obtener_carpeta("Viajes").agregar_mensaje(self.msg_viajes)
        self.user.obtener_carpeta("Trabajo").agregar_mensaje(self.msg_trabajo)
        self.user.obtener_carpeta("inbox").agregar_mensaje(self.msg_inbox)

    def test_busqueda_recursiva_en_profundidad(self):
        """Verifica que la búsqueda recursiva encuentre mensajes en cualquier nivel."""
        # Buscar el mensaje que está en el nivel más profundo (Viajes)
        resultados = self.user.buscar_mensaje("vacaciones", campo='asunto')
        self.assertIn(self.msg_viajes, resultados)
        self.assertEqual(len(resultados), 1)

    def test_mover_carpeta_completa_y_recursiva(self):
        """Verifica que mover una carpeta mueva todo su contenido y cambie la estructura."""

        # Mover 'Trabajo' (que contiene 'Viajes' y msg_trabajo) a 'inbox'
        self.user.mover_carpeta("Trabajo", "inbox")

        # 1. Comprobar que el mensaje sigue siendo accesible por búsqueda recursiva
        resultados = self.user.buscar_mensaje("Informe Final", campo='asunto')
        self.assertIn(self.msg_trabajo, resultados)

        # 2. Comprobar que la carpeta 'Personal' ya NO contiene 'Trabajo'
        padre_original = self.user.obtener_carpeta("Personal")
        trabajo_en_personal = padre_original.obtener_subcarpeta("Trabajo")
        self.assertIsNone(trabajo_en_personal)

        # 3. Comprobar que 'inbox' AHORA contiene 'Trabajo'
        nuevo_padre = self.user.obtener_carpeta("inbox")
        trabajo_en_inbox = nuevo_padre.obtener_subcarpeta("Trabajo")
        self.assertIsNotNone(trabajo_en_inbox)

        # 4. Verificar integridad de la subestructura
        viajes_en_trabajo = trabajo_en_inbox.obtener_subcarpeta("Viajes")
        self.assertIsNotNone(viajes_en_trabajo)

    def test_mover_mensaje_limite(self):
        """Verifica el caso límite de mover un mensaje que no existe en el origen."""
        mensaje_falso = Mensaje("a@a.com", "b@b.com", "Error", "")
        with self.assertRaises(ValueError):
            # Intenta mover un mensaje que NO está en inbox
            self.user.mover_mensaje(mensaje_falso, "inbox", "Trabajo")

        # Intenta mover un mensaje que SÍ está, y verifica que se elimina del origen
        self.user.mover_mensaje(self.msg_inbox, "inbox", "Personal")
        self.assertNotIn(self.msg_inbox, self.user.obtener_carpeta("inbox").obtener_mensajes)
        self.assertIn(self.msg_inbox, self.user.obtener_carpeta("Personal").obtener_mensajes)


class TestColaPrioridad(unittest.TestCase):

    def setUp(self):
        self.cola = ColaPrioridad()

        # Mensajes con diferentes prioridades
        self.msg_normal_A = Mensaje("a@a.com", "b@b.com", "Normal A", "...", prioridad=2)
        self.msg_urgente_B = Mensaje("b@b.com", "b@b.com", "Urgente B", "...", prioridad=1)
        self.msg_normal_C = Mensaje("c@c.com", "b@b.com", "Normal C", "...", prioridad=2)
        self.msg_urgente_D = Mensaje("d@d.com", "b@b.com", "Urgente D", "...", prioridad=1)

    def test_prioridad_y_orden(self):
        """Verifica que los mensajes se desencolen en orden de prioridad (1 primero)
        y FIFO para la misma prioridad."""

        # Encolar en un orden mezclado
        self.cola.encolar(self.msg_normal_A)
        self.cola.encolar(self.msg_urgente_B)
        self.cola.encolar(self.msg_normal_C)
        self.cola.encolar(self.msg_urgente_D)

        # Desencolado 1: Debe ser el primer mensaje de prioridad 1 que se encoló (Urgente B)
        self.assertEqual(self.cola.desencolar().asunto, "Urgente B")

        # Desencolado 2: Debe ser el segundo mensaje de prioridad 1 (Urgente D)
        self.assertEqual(self.cola.desencolar().asunto, "Urgente D")

        # Desencolado 3: Debe ser el primer mensaje de prioridad 2 (Normal A)
        self.assertEqual(self.cola.desencolar().asunto, "Normal A")

        # Desencolado 4: Debe ser el segundo mensaje de prioridad 2 (Normal C)
        self.assertEqual(self.cola.desencolar().asunto, "Normal C")

        # Caso Límite: Cola vacía
        self.assertIsNone(self.cola.desencolar())