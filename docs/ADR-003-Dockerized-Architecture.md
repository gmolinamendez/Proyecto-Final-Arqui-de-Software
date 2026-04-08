# ADR 003: Arquitectura Totalmente Dockerizada

## Estado
Aceptado

## Contexto
El equipo y el entorno de calificación del proyecto exigen que la aplicación garantice reproducibilidad en distintas máquinas (incluyendo Mac M1, Windows y Linux) sin generar conflictos de dependencias (el clásico problema de *"en mi máquina sí funciona"*). El Documento Técnico requiere una configuración estándar para las entregas y demostraciones (puerto 5050).

## Decisión
Se ha decidido mantener y optimizar una **arquitectura completamente dockerizada**.
* El ecosistema completo se orquesta a través de `docker-compose`.
* Contamos con dos entornos aislados principales:
  1. El Backend (incluyendo estáticos de Frontend empaquetados).
  2. La Base de Datos basada en `postgres:16-alpine`.
* Se ha configurado la propiedad explícita de plataforma (`platform: linux/arm64`) para asegurar el buen rendimiento del contenedor en chips de Apple Silicon (M1/M2/M3).
* El mapeo del puerto es explícitamente `5050` local al contenedor para emparejarse con el Documento Técnico. 

## Consecuencias
- **Positivas**: 
  - Ambientes de ejecución agnósticos a la máquina anfitrión garantizando alta fidelidad entre desarrollo, pruebas y producción.
  - Resolución simple de dependencias en sistema operativo (ej, `psycopg2-binary` sin fallos asíncronos mediante dependencias exactas en la imagen `python:3.12-slim`).
  - La base de datos se inicializa a su estado ideal automáticamente en el primer inicio.
- **Negativas**:
  - Introduce tiempos de carga superiores debido a la recolección inicial y construcción de imágenes en la primera ejecución (`docker-compose up --build`).
  - Posibilidad de almacenamiento retenido, requiriendo purga de volúmenes si el prototipo de base de datos evoluciona severamente.
