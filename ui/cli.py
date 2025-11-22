from ui.menu import Menu
import time
from models.servidor import ServidorCorreo


class CLI:

    def __init__(self, gestor_mensajes, gestor_carpetas, gestor_filtros, gestor_red):
        self.gestor_mensajes = gestor_mensajes
        self.gestor_carpetas = gestor_carpetas
        self.gestor_filtros = gestor_filtros
        self.gestor_red = gestor_red
        self.usuario_actual = None

    def iniciar(self, usuario_inicial=None):

        if usuario_inicial:
            self.usuario_actual = usuario_inicial
            self._bucle_principal()
        else:
            print('Usando usuario por defecto')

    def _bucle_principal(self):

        while True:
            Menu.mostrar_bienvenida()
            estadisticas = self.gestor_mensajes.obtener_estadisticas_usuario(self.usuario_actual)
            print(f"Resumen: {estadisticas['pendientes']} no leidos | {estadisticas['recibidos']} recibidos")

            opcion = Menu.menu_principal(self.usuario_actual)

            if opcion == '1':
                self._redactar_mensaje()
            elif opcion == '2':
                self._ver_inbox()
            elif opcion == '3':
                self._ver_enviados()
            elif opcion == '4':
                self._menu_carpetas()
            elif opcion == '5':
                self._menu_filtros()
            elif opcion == '6':
                self._menu_red()
            elif opcion == '0':
                print('Cerrando sesion')
                break
            else:
                input('Opcion invalida')

    def _redactar_mensaje(self):
        print('\n--- Nuevo mensaje ---')
        destino = input('Para: ')
        asunto = input('Asunto: ')
        cuerpo = input('Mensaje: ')

        try:
            prioridad = int(input('Prioridad (1-alta, 2-baja) [Default: 2]'))
        except:
            prioridad = 2

        if self.gestor_mensajes.enviar_mensaje(self.usuario_actual, destino, asunto, cuerpo, prioridad):
            input('Mensaje enviado. Presione enter para volver')
        else:
            input('Error al enviar. Verique red o destinatario.')

    def _ver_inbox(self):
        print('\n--- Bandeja de entrada ---')
        mensajes = self.gestor_mensajes.recibir_mensajes(self.usuario_actual)

        for mensaje in mensajes:
            if not mensaje.leido:
                self.gestor_filtros.aplicar_filtros(mensaje, self.usuario_actual)

        mensajes = self.gestor_mensajes.recibir_mensajes(self.usuario_actual)

        if not mensajes:
            print('No hay mensajes')
        else:
            mensajes = self.gestor_mensajes.ordenar_mensajes(self.usuario_actual.inbox, 'fecha')
            for index, mensaje in enumerate(mensajes):
                estado = "[Urgente]" if mensaje.prioridad == 1 else ""
                print(f"{index + 1}. {estado} {mensaje.asunto} - De: {mensaje.remitente.correo}")

            operacion = input('\nSeleccione numero para leer: ')
            if operacion.isdigit() and 0 < int(operacion) <= len(mensajes):
                msg = mensajes[int(operacion)-1]
                print('Asunto: ' + str(msg.asunto))
                print('De: ' + str(msg.remitente.correo))
                print('Cuerpo: ' + str(msg.cuerpo))
                self.gestor_mensajes.marcar_como_leido(msg)

                accion = input("\n1.Eliminar, 2.Mover, 3.Cambiar Prioridad: ")
                if accion == '1':
                    self.gestor_mensajes.eliminar_mensaje(msg, self.usuario_actual)

                elif accion == '2':
                    destino = input("Nombre carpeta destino: ")
                    carpeta = self.gestor_carpetas.buscar_carpeta(self.usuario_actual, destino)
                    if carpeta:
                        self.gestor_carpetas.mover_mensaje(msg, self.usuario_actual.inbox, carpeta)
                    else:
                        print("Carpeta no encontrada.")

                elif accion == '3':
                    print('Prioridad actual: ' + str(msg.prioridad))
                    nueva_prioridad = int(input('Ingrese nueva prioridad (1=Alta, 2=Baja): '))

                    if self.gestor_mensajes.cambiar_prioridad_mensaje(msg, nueva_prioridad):
                        if msg.prioridad == int(nueva_prioridad):
                            print('Prioridad actualizada')
                        else:
                            print('No se pudo cambiar la prioridad')
                    else:
                        print('Error: Ingrese un numero valido')

            input("\nEnter para volver")

    def _ver_enviados(self):
        print('\n--- Enviados ---')
        for mensaje in self.usuario_actual.sent.obtener_mensajes:
            print(mensaje.asunto + '->' + mensaje.destinatario)
        input('Enter para volver')

    def _menu_carpetas(self):

        while True:
            Menu.limpiar_pantalla()
            operacion = Menu.menu_carpetas()

            if operacion == '1':
                self.gestor_carpetas.listar_carpetas(self.usuario_actual)
                input('Enter para continuar')
            elif operacion == '2':
                nombre = input('Nombre de carpeta nueva: ')
                padre = input('Carpeta padre (enter para raiz): ') or 'raiz'
                self.gestor_carpetas.crear_carpeta(self.usuario_actual, nombre,padre)
                input('Enter')
            elif operacion == '3':
                nombre = input('Nombre de la carpeta a eliminar: ')
                self.gestor_carpetas.eliminar_carpeta(self.usuario_actual, nombre)
                input('Enter')
            elif operacion == '4':
                termino = input('Buscar (Asunto/Remitente): ')
                resultado = self.gestor_mensajes.buscar_mensajes(self.usuario_actual, None, termino)
                print('Encontrados: ' + str(len(resultado)))
                for mensaje in resultado:
                    print(mensaje.asunto)
                    input('Enter')
            elif operacion == '0':
                break

    def _menu_filtros(self):
        while True:
            Menu.limpiar_pantalla()
            operacion = Menu.menu_filtros()
            if operacion == "1":
                self.gestor_filtros.listar_filtros(self.usuario_actual)
                input("Presione Enter para continuar")
            elif operacion == "2":
                nombre = input("Nombre del filtro: ")
                criterio = input("Criterio (asunto/remitente/cuerpo): ")
                valor = input("Valor a buscar: ")
                accion = input("Acción (mover/leer/prioridad): ")
                destino = None

                if accion == 'mover':
                    destino = input("Carpeta destino: ")
                self.gestor_filtros.crear_filtro(self.usuario_actual, nombre, criterio, valor, accion, destino)
                input("Presione Enter para continuar")

            elif operacion == "3":
                self.gestor_filtros.listar_filtros(self.usuario_actual)
                filtro_a_eliminar = input("Copie el ID del filtro a eliminar: ")
                self.gestor_filtros.eliminar_filtro(self.usuario_actual, filtro_a_eliminar)
                input("Enter")
            elif operacion == "0":
                break

    def _menu_red(self):
        while True:
            Menu.limpiar_pantalla()
            operacion = Menu.menu_red()
            if operacion == "1":
                nombre = input("Nombre (ej: gmail.com): ")
                nuevo_srv = ServidorCorreo(nombre)
                self.gestor_red.agregar_servidor(nuevo_srv)
                input("Enter...")
            elif operacion == "2":
                srv1 = input("Nombre Servidor 1: ")
                srv2 = input("Nombre Servidor 2: ")
                self.gestor_red.conectar_servidores(srv1, srv2)
                input("Enter...")
            elif operacion == "3":
                origen = input("Servidor Origen: ")
                destino = input("Servidor Destino: ")
                ruta = self.gestor_red.encontrar_mejor_ruta(origen, destino)
                if ruta:
                    print(f"Ruta: {' -> '.join(ruta)}")
                else:
                    print("No hay conexión.")
                input("Enter...")
            elif operacion == "0":
                break