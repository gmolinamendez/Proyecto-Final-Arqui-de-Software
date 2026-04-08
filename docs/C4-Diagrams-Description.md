# Descripciones para Diagramas C4

Para cumplir con el rubro de Documentación, a continuación se enuncia la descripción funcional de los 3 niveles del framework C4 adaptados a la actual arquitectura del software.

## Nivel 1: Diagrama de Contexto (Context Diagram)

**Propósito**: Mostrar el panorama general del sistema, evidenciando cómo encaja en el entorno tecnológico y con sus usuarios.

**Descripción para el Diseño:**
- **Actor Principal**: *"Usuario Administrador/Cliente"* que necesita visualizar y registrar información de Eventos o Asistentes usando una interfaz gráfica en el navegador.
- **Sistema de Software Central**: *"Sistema de Gestión de Eventos"* (Este proyecto). Su función es proveer servicios web para alojar y servir la aplicación Frontend así como también recibir llamadas a APIs para la persistencia y lectura de usuarios, personas y eventos.
- **Sistema de Software Externo**: No se utilizan pasarelas de pago ni APIs públicas en este paso. El límite funcional está dictado íntegramente por los confines operacionales del repositorio hospedado.

## Nivel 2: Diagrama de Contenedores (Container Diagram)

**Propósito**: Acercarse al Sistema de Gestión de Eventos para evidenciar las piezas ejecutables e interactivas individuales.

**Descripción para el Diseño:**
- **Contenedor 1 (Single-Page Application - SPA)**: Construido en React (Node.js vía Vite y distribuido a través de archivos estáticos). Provee las vistas interactivas alojadas y consumidas por el navegador del cliente. 
- **Contenedor 2 (Backend API Application)**: Construido con `Flask` en `Python 3.12`. Atiende a los usuarios mediante un servidor WSGI (`gunicorn`). Controla rutas de APIs (ej. `/api/users`), expone la SPA desde su carpeta `dist`, canaliza llamadas y coordina la persistencia de datos.
- **Contenedor 3 (Database)**: Base de Datos relacional implementada en `PostgreSQL 16` utilizando datos estructurados sobre alpinelinux. Resguarda todo estado de negocio (Esquemas: `Users`, `Events`, `Persons`, `EventAttendees`).

*Relaciones:* 
- El Cliente se conecta a la aplicación API usando `HTTPS/HTTP` en el puerto `5050`. 
- La aplicación SPA efectúa llamadas REST a los endpoints de la aplicación API vía `AJAX/Fetch`. 
- El Backend interactúa con la base de datos vía consultas DML a través del protocolo nativo sobre TCP (`psycopg2-binary`).

## Nivel 3: Diagrama de Componentes (Component Diagram)

**Propósito**: Realizar un desglose del Contenedor Backend API (Contenedor 2) para entender cómo el software estructura la canalización de operaciones internas.

**Descripción para el Diseño:**
- **Componente: Enrutador Global (main.py y APIs/*.py)**: Enlaza peticiones entrantes desde el servidor web mediante decoradores de Flask, determinando si debe servir contenido estático de React o enrutar hacia un Endpoint RESTful. Redirige todo tráfico API mediante alias (`_register_api_aliases()`).
- **Componente: Controladores REST (Controllers)**: Métodos puntuales encargados de la validación inicial del esquema de entrada y control del código de respuesta para sus respectivos dominios lógicos (Usuarios, Eventos, Asistentes y Personas).
- **Componente: Servicios/Models Layer (Raw SQL Services)**: Contiene la lógica transaccional. Construye cadenas SQL (`INSERT`, `SELECT`, etc.) que satisfacen la interfaz de datos y llama a la clase `database` de persistencia.
- **Componente: Database Connection Manager (database.py)**: Responsable de extraer el conector desde la URI del ecosistema (.env/Docker) usando directivas del engine transaccional subyacente. Asegura mantener el `pool_pre_ping=True` válido frente a reinicios de PostgreSQL.

*Relaciones:*
- La capa de routing intercepta peticiones.
- Los routers invocan los Controladores.
- Los Controladores inyectan y mandan respuestas desde los Servicios.
- Los Servicios utilizan el Connection Manager para ejecutar el Raw SQL en el contenedor de Base de Datos externa.
