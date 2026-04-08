# ADR 002: Uso de Raw SQL para la Persistencia de Datos

## Estado
Aceptado

## Contexto
El Documento Técnico de Omega exige que el proyecto garantice un alto control sobre las consultas y esquemas de la base de datos. Si bien los ORMs (Object-Relational Mappers) como SQLAlchemy (en su modo declarativo) facilitan el desarrollo, a menudo introducen consultas ineficientes o impiden al desarrollador ejercer un modelado óptimo cuando las tablas crecen en complejidad.

## Decisión
Se ha adoptado el uso directo de **Raw SQL** para la definición de tablas y la manipulación de datos, aunque se utilice la herramienta `sqlalchemy` o `psycopg2` como un adaptador para enviar estas consultas.
* Las tablas principales (`Users`, `Events`, `Persons`, `EventAttendees`) se gestionan mediante consultas DDL directas integradas a un origen único (`init.sql`).
* Las consultas o manipulaciones CRUD se escribirán en sentencias preparadas explícitamente para garantizar una indexación y control granular al máximo.

## Consecuencias
- **Positivas**: 
  - Rendimiento óptimo mediante consultas explícitas y exactas sin el "overhead" causado por ORMs.
  - Mayor transparencia hacia la estructura de la base de datos permitiendo acoplar fácilmente el backend al sistema PostgreSQL existente.
  - Los archivos `.sql` y sentencias sirven como fuente confiable (Single Source of Truth) para la base de datos.
- **Negativas**:
  - Mantenimiento manual de migraciones y compatibilidad (es necesario modificar el código SQL ante cualquier cambio en el formato de la tabla).
  - Mayor riesgo de inyecciones SQL si no se utilizan consultas correctamente parametrizadas.
