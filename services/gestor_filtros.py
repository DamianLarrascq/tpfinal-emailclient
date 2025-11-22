import uuid


class GestorFiltros:

    def __init__(self, gestor_carpetas):
        self.gestor_carpetas = gestor_carpetas

    def crear_filtro(self, usuario, nombre, criterio, valor, accion, destino=None):

        nuevo_filtro = {
            'id': str(uuid.uuid4())[:8],
            'nombre': nombre,
            'criterio': criterio,
            'valor': valor,
            'accion': accion,
            'destino': destino
        }

        return self.agregar_filtro(usuario, nuevo_filtro, nuevo_filtro['id'])

    def agregar_filtro(self, usuario, filtro, id_filtro):

        if self.validar_filtro(filtro):
            if 'id' not in filtro:
                filtro['id'] = str(id_filtro)

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
            criterio = regla['criterio']
            valor_buscado = regla['valor']

            if criterio == 'etiqueta':
                coincidencia = valor_buscado in mensaje.etiquetas

            elif criterio in ['remitente', 'asunto', 'cuerpo']:
                try:
                    campo_mensaje = getattr(mensaje, criterio)
                    coincidencia = valor_buscado.lower() in campo_mensaje.lower()
                except AttributeError:
                    coincidencia = False

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

                elif accion == 'prioridad':
                    try:
                        nueva_prioridad = int(valor_buscado)
                        mensaje.cambiar_prioridad(nueva_prioridad)
                    except ValueError:
                        pass

    def listar_filtros(self, usuario):

        filtros = usuario.filtros

        if not filtros:
            raise ValueError('No hay filtros configurados')
        else:
            print('--- Filtros activos ---')
            for i, filtro in enumerate(filtros):
                nombre = filtro.get('nombre')
                filtro_id = filtro['id']
                accion = filtro['accion']
                criterio = filtro['criterio']
                valor = filtro['valor']

                print('ID: ' + filtro_id + '\nNombre: ' + nombre + '\nAccion: ' + accion + '\nCriterio: ' + criterio + '\nValor: ' + valor)

    def eliminar_filtro(self, usuario, id_filtro):

        filtros = usuario.filtros

        for filtro in filtros:
            if filtro['id'] == id_filtro:
                filtros.remove(filtro)
                return True

        return False

    def validar_filtro(self, filtro):

        criterios_validos = ['remitente', 'asunto', 'cuerpo', 'etiqueta']
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
