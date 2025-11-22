from models.usuario import Usuario
from models.servidor import ServidorCorreo
from services.gestor_red import GestorRed
from services.gestor_mensajes import GestorMensajes
from services.gestor_carpetas import GestorCarpetas
from services.gestor_filtros import GestorFiltros
from ui.cli import CLI


def main():
    print("Inicializando sistema de correo...")

    # 1. Inicializar servicios
    gestor_red = GestorRed()
    gestor_carpetas = GestorCarpetas()
    gestor_mensajes = GestorMensajes(gestor_red, gestor_carpetas)
    gestor_filtros = GestorFiltros(gestor_carpetas)

    # 2. Configurar red de servidores
    srv_google = ServidorCorreo("gmail.com")
    srv_yahoo = ServidorCorreo("yahoo.com")
    srv_outlook = ServidorCorreo("outlook.com")

    # Los agregamos al grafo
    gestor_red.agregar_servidor(srv_google)
    gestor_red.agregar_servidor(srv_yahoo)
    gestor_red.agregar_servidor(srv_outlook)

    # Conectamos los servidores
    gestor_red.conectar_servidores("gmail.com", "yahoo.com")
    gestor_red.conectar_servidores("yahoo.com", "outlook.com")

    # 3. Crear Usuarios Demo
    user_pepe = Usuario("Pepe", "pepe@gmail.com")
    user_juan = Usuario("Juan", "juan@outlook.com")

    # Registrar usuarios en sus servidores locales
    srv_google.registrar_usuario(user_pepe)
    srv_outlook.registrar_usuario(user_juan)

    # Creamos una carpeta personalizada para Pepe
    gestor_carpetas.crear_carpeta(user_pepe, "Trabajo")

    # Creamos un filtro para Pepe
    gestor_filtros.crear_filtro(
        user_pepe,
        nombre="Filtro Trabajo",
        criterio="asunto",
        valor="urgente",
        accion="mover",
        destino="Trabajo"
    )

    print("Sistema listo. Iniciando CLI...")

    # 5. Iniciar Interfaz
    # Iniciamos sesión automáticamente con Pepe para la demo
    app = CLI(gestor_mensajes, gestor_carpetas, gestor_filtros, gestor_red)
    app.iniciar(usuario_inicial=user_pepe)
if __name__ == "__main__":
    main()
