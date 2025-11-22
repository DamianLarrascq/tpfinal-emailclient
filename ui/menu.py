import os

class Menu:
    @staticmethod
    def limpiar_pantalla():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def mostrar_bienvenida():
        Menu.limpiar_pantalla()
        print('--------------------')
        print(' Cliente Correo  ')
        print('--------------------')

    @staticmethod
    def mostrar_login():
        print('\n--- Login ---')
        email = input('Email: ')

        return email

    @staticmethod
    def menu_principal(usuario):
        print('\n--- Bienvenido ' + usuario.nombre + ' ' + usuario.correo)
        print('1. Redactar mensaje')
        print('2. Bandeja de entrada (inbox)')
        print('3. Bandeja de salida (sent)')
        print('4. Gestionar carpetas (Arbol)')
        print('5. Gestionar filtros')
        print('6. Panel admin')
        print('0. Salir')

        return input('Seleccione una opcion: ')

    @staticmethod
    def menu_carpetas():
        print("\n--- Carpetas ---")
        print("1. Ver estructura de arbol")
        print("2. Crear nueva carpeta")
        print("3. Eliminar carpeta")
        print("4. Buscar mensaje (Recursivo)")
        print("0. Volver")
        return input("Seleccione una opcion: ")

    @staticmethod
    def menu_filtros():
        print('\n--- Filtros ---')
        print('1. Ver filtros activos')
        print('2. Crear nuevo filtro')
        print('3. Eliminar filtro')
        print('0. Volver')

        return input('Seleccione una opcion: ')

    @staticmethod
    def menu_red():
        print('\n--- Panel admin ---')
        print('1. Agregar servidor')
        print('2. Conectar servidores')
        print('3. Verificar ruta entre dos servidores')
        print('0. Volver')

        return input('Seleccione una opcion: ')