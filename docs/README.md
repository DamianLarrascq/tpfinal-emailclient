# Cliente de Correo Electrónico - Proyecto Final ED
## Descripción
Sistema de gestión de correo electrónico implementado en Python utilizando
estructuras de datos avanzadas y algoritmos eficientes. El proyecto modela un
cliente de correo completo con gestión de usuarios, mensajes, carpetas
recursivas, filtros automáticos y una red distribuida de servidores.
## Integrantes del Grupo
- **Damián Larrascq - damian.larrascq@gmail.com
-----------
## Tecnologías Utilizadas
- **Lenguaje**: Python 3.10+
- **Estructuras de Datos**:
 - Árboles Generales (gestión de carpetas)
 - Colas de Prioridad (mensajes urgentes)
 - Grafos (red de servidores)
- **Algoritmos**:
 - Recursividad (búsquedas en árbol)
 - BFS/DFS (enrutamiento de mensajes)
- **Testing**: pytest
- **Control de Versiones**: Git/GitHub
-----------

## Características Principales
### ✉ Gestión de Mensajes
- Envío y recepción de mensajes
- Mensajes con prioridades (1-2)
- Etiquetado y categorización
- Búsqueda avanzada
### 📁 Sistema de Carpetas
- Estructura jerárquica de carpetas (árbol general)
- Subcarpetas ilimitadas
- Búsqueda recursiva de mensajes
- Movimiento de mensajes entre carpetas
### 🔍 Filtros Automáticos
- Creación de reglas de filtrado
- Aplicación automática a mensajes entrantes
- Múltiples criterios (remitente, asunto, palabras clave)
### 🚀 Mensajes Urgentes
- Cola de prioridades para mensajes importantes
- Procesamiento preferencial
- Notificaciones especiales
### 🌐 Red de Servidores
- Grafo de servidores interconectados
- Enrutamiento inteligente con BFS/DFS
- Simulación de envío entre dominios

-----------

## Instalación
### Requisitos Previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git
### Pasos de Instalación
1. Clonar el repositorio:
git clone https://github.com/DamianLarrascq/tpfinal-emailclient.git
2. Crear entorno virtual (recomendado):
python -m venv venv
source venv/bin/activate # En Windows: venv\Scripts\activate
3. Instalar dependencias:
pip install -r requirements.txt
4. Verificar instalación:
python -m pytest tests/

-----------

# Ejemplo de uso:

## Crear un servidor
servidor = ServidorCorreo()

## Crear usuarios
usuario1 = Usuario("Damian", "damian@gmail.com")\
usuario2 = Usuario("Victoria", "victoria@gmail.com")

## Registrar los usuarios en el servidor
servidor.registrar_usuario(usuario1)\
servidor.registrar_usuario(usuario2)

## Crear mensaje de Damián para Victoria
msj = Mensaje("damian@gmail.com", "victoria@gmail.com", "Entrega TP Estructuras de Datos", "La primer entrega se realiza el 20/09")

## Enviar el mensaje
servidor.enviar_mensaje(msj, "victoria@gmail.com")

## Listar asuntos de los mensajes recibidos por Victoria
print(servidor.listar_mensajes("victoria@gmail.com"))\
["Entrega TP Estructuras de Datos"]

## Buscar el mensaje en las carpetas de Victoria
resultados = servidor.buscar_mensaje("victoria@gmail.com", "Entrega")
print(f"Mensajes encontrados: {[m.asunto for m in resultados]}")
# Mensajes encontrados: ['Entrega TP Estructuras de Datos']

## Buscar por remitente
resultados_remitente = servidor.buscar_mensaje("victoria@gmail.com", "damian", campo="remitente")
print(f"Mensajes encontrados por remitente: {[m.asunto for m in resultados_remitente]}")
# Mensajes encontrados por remitente: ['Entrega TP Estructuras de Datos']

-----------
# Documentación:

![Diagramas](diagramas)


