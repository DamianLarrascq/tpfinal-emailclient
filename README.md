# Trabajo Final para la Cátedra: Estructuras de Datos en Python (Comisión 3)

Este proyecto implementa un sistema de correo electrónico orientado a objetos en Python.

-----------
# Objetivo

El sistema permite:
- Registrar usuarios en un servidor de correo
- Enviar y recibir mensajes entre usuarios registrados
- Guardar copias de los mensajes enviados en la carpeta "sent", y recibidos en "inbox"
- Listar los asuntos de los mensajes recibidos

-----------

# Clases principales

- InterfazCorreo: Interfaz abstracta que define los métodos esenciales de un servidor de correo electrónico
- ServidorCorreo: Administra usuarios y gestiona el envío, recepción y listado de mensajes
- Usuario: Representa a un usuario con un correo único y sus carpetas
- Mensaje: Modela un mensaje con remitente, destinatario, asunto y cuerpo
- Carpeta: Almacena mensajes de un usuario en "inbox" y "sent"

-----------

# Ejemplo de uso:

## Crear un servidor
servidor = ServidorCorreo()

## Crear usuarios
usuario1 = Usuario("Damian", "damian@gmail.com")
usuario2 = Usuario("Victoria", "victoria@gmail.com")

## Registrar los usuarios en el servidor
servidor.registrar_usuario(usuario1)
servidor.registrar_usuario(usuario2)

## Crear mensaje de Damián para Victoria
msj = Mensaje("damian@gmail.com", "victoria@gmail.com", "Entrega TP Estructuras de Datos", "La primer entrega se realiza el 20/09")

## Enviar el mensaje
servidor.enviar_mensaje(msj, "victoria@gmail.com")

## Listar asuntos de los mensajes recibidos por Victoria
print(servidor.listar_mensajes("victoria@gmail.com"))
## ["Entrega TP Estructuras de Datos"]

-----------
# Diagrama UML:

[Diagrama de Clases --.pdf](https://github.com/user-attachments/files/22435820/Diagrama.de.Clases.--.pdf)


