from models.mensaje import Mensaje


class GestorMensajes:

    def __init__(self, gestor_red, gestor_carpetas):
        self.gestor_red = gestor_red
        self.gestor_carpetas = gestor_carpetas

    def enviar_mensaje(self, remitente,destinatario, asunto, cuerpo, prioridad=2):

        nuevo_mensaje = Mensaje(remitente, destinatario, asunto, cuerpo, prioridad)

        try:
            dominio_origen = remitente.correo.split('@')[1]
            dominio_destino = destinatario.split('@')[1]
        except IndexError:
            return False

        servidor_origen = None

        for servidor in self.gestor_red.grafo.__servidores.values():
            if servidor.dominio == dominio_origen:
                servidor_origen = servidor
                break

        if not servidor_origen:
            return False

        envio_gestor = self.gestor_red.enviar_mensaje_red(nuevo_mensaje, servidor_origen, destinatario)

        if envio_gestor:
            remitente.enviar_mensaje(nuevo_mensaje)
            return True

        return False

    def recibir_mensajes(self, usuario):

        return usuario.inbox.obtener_mensajes

    def marcar_como_leido(self, mensaje):

        mensaje.marcar_como_leido()

    def eliminar_mensaje(self, mensaje, usuario):

        carpeta_origen = self._encontrar_carpeta_contenedora(usuario.raiz, mensaje)

        carpeta_papelera = usuario.obtener_carpeta('papelera')
        if not carpeta_papelera:
            carpeta_papelera = usuario.agregar_carpeta('papelera')

        if carpeta_origen and carpeta_papelera:
            return self.gestor_carpetas.mover_mensaje(mensaje, carpeta_origen, carpeta_papelera)

        return False

    def buscar_mensajes(self, usuario, criterio, valor):

        return usuario.raiz.buscar_mensaje(valor, criterio)

    def ordenar_mensajes(self, carpeta, criterio='fecha'):

        mensajes = list(carpeta.obtener_mensajes)

        if criterio == 'fecha':
            mensajes.sort(key=lambda m: m.fecha, reverse=True)
        elif criterio == 'prioridad':
            mensajes.sort(key=lambda m: m.prioridad)
        elif criterio == 'asunto':
            mensajes.sort(key=lambda m: m.asunto)

        return mensajes

    def _encontrar_carpeta_contenedora(self, carpeta_actual, mensaje):

        if mensaje in carpeta_actual.obtener_mensajes:
            return carpeta_actual

        for subcarpeta in carpeta_actual.subcarpetas:
            resultado = self._encontrar_carpeta_contenedora(subcarpeta, mensaje)
            if resultado:
                return resultado

        return None