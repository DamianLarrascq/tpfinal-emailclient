from uuid import uuid4


class GestorFiltros:

    def __init__(self, gestor_carpetas):
        self.gestor_carpetas = gestor_carpetas

    def agregar_filtro(self, usuario, filtro):

        if self.validar_filtro(filtro):
            if 'id' not in filtro:
                filtro['id'] = str(uuid4())

            usuario.agregar_filtro(filtro)
            return True

        return False

    def modificar_filtro(self, usuario, id_filtro, nuevo_filtro):

        filtros = usuario.filtros

        for i, filtro in enumerate(filtros):

            if filtro.get('id') == id_filtro:

                filtro_actualizado = filtro.copy()
                filtro_actualizado.update(nuevo_filtro)
                filtro_actualizado['id'] = id_filtro

                if self.validar_filtro(filtro_actualizado):

                    filtros[i] = filtro_actualizado
                    return True
                else:
                    return False

        return False

    def aplicar_filtros(self, mensaje, usuario):

        filtros = usuario.filtros
        if not filtros:
            return

        mensaje_movido = False

        for regla in filtros:
            if mensaje_movido and regla['accion'] == 'mover':
                continue

            coincidencia = False
            valor_buscado = regla['valor']

            if regla['criterio'] == 'remitente':
                if valor_buscado in mensaje.asunto.lower():
                    coincidencia = True

            elif regla['criterio'] == 'asunto':
                if valor_buscado in mensaje.asunto.lower():
                    coincidencia = True

            elif regla['criterio'] == 'cuerpo':
                if valor_buscado in mensaje.asunto.lower():
                    coincidencia = True

            if coincidencia:
                accion = regla['accion']

                if accion == 'leer':
                    mensaje.marcar_como_leido()

                elif accion == 'mover':
                    nombre_carpeta_destino = regla['destino']
                    carpeta_destino = self.gestor_carpetas.buscar_carpeta(usuario, nombre_carpeta_destino)

                    if carpeta_destino:
                        resultado = self.gestor_carpetas.mover_mensaje(mensaje, usuario.inbox, carpeta_destino)
                        if resultado:
                            mensaje_movido = True

    def listar_filtros(self, usuario):

        filtros = usuario.filtros

        if not filtros:
            raise ValueError('No hay filtros configurados')
        else:
            return filtros

    def eliminar_filtro(self, usuario, id_filtro):

        filtros = usuario.filtros

        for filtro in filtros:
            if filtro['id'] == id_filtro:
                filtros.remove(filtro)
                return True

        return False

    def validar_filtro(self, filtro):

        criterios_validos = ['remitente', 'asunto', 'cuerpo']
        acciones_validas = ['mover', 'leer', 'prioridad']

        if not all(key in filtro for key in ('criterio', 'valor', 'accion')):
            return False

        if filtro['criterio'] not in criterios_validos:
            return False
        if filtro['accion'] not in acciones_validas:
            return False

        if filtro['accion'] == 'mover'and not filtro.get('destino'):
            return False

        return True
