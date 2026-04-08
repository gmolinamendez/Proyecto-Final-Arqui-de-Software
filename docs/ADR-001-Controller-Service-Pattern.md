# ADR 001: Implementación del Patrón Controller-Service

## Estado
Aceptado

## Contexto
El proyecto requiere una arquitectura limpia, escalable y mantenible para el backend construido en Flask. A medida que la aplicación crece, mezclar la lógica de negocio, las consultas a la base de datos y el enrutamiento HTTP en los mismos archivos puede generar un código difícil de mantener, propenso a errores y complicado de someter a pruebas unitarias. 

## Decisión
Se ha decidido implementar el patrón **Controller-Service** (separación de responsabilidades):
- **Controllers (Enrutadores en Flask)**: Encargados exclusivamente de manejar las solicitudes HTTP, validar la entrada del usuario, llamar a las funciones del modelo/servicio apropiadas y devolver las respuestas HTTP (códigos de estado, JSON).
- **Services (Lógica de Negocio/Persistencia)**: Encargados de procesar la lógica de negocio y realizar interacciones directas con la base de datos (y otras integraciones externas si existiesen).

## Consecuencias
- **Positivas**: 
  - La lógica de negocio está completamente desacoplada del protocolo HTTP.
  - Facilita las pruebas automáticas al permitir simular (mocking) la capa de datos.
  - Mejora drásticamente la legibilidad y estructura del código, garantizando que futuras implementaciones no transformen al sistema en un "espagueti".
- **Negativas**:
  - Implica un ligero aumento en la cantidad de archivos y capas en el backend.
  - Puede añadir una leve complejidad para desarrolladores puramente acostumbrados a diseños monolíticos simples en scripts únicos.
