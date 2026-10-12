Plan técnico — UniShort QR
Stack
Python 3.12 · FastAPI · Uvicorn · SQLAlchemy · Pydantic · segno (QR) ·SQLite (desarrollo) / PostgreSQL (objetivo).

Arquitectura en capas
Rutas (FastAPI) → Servicios (reglas de negocio) → Modelos (SQLAlchemy) → BD.

Modelo de datos
Entidad	Atributos
Usuario	id, nombre, correo (único), rol
Enlace	id, código_corto (ÚNICO), url_destino, estado, fecha_creacion, fecha_caducidad, creador_id (FK)
Métrica	id, enlace_id (FK), fecha_hora
Relaciones: un usuario crea muchos enlaces; un enlace tiene muchas métricas.

Endpoints previstos
Método	Ruta	Descripción
POST	/shorten	Crear enlace corto + QR
GET	/s/{id}	Redirección HTTP 302
GET	/links	Listar enlaces del creador
PATCH	/links/{id}	Desactivar enlace
GET	/links/{id}/metrics	Métricas agregadas
GET	/health	Verificación de servicio
Decisiones técnicas
HTTP 302 (no 301): permite contabilizar clics en cada acceso.
QR → enlace corto (no destino original): el QR impreso sigue funcionandosi cambia el destino.
Unicidad: índice UNIQUE en código_corto + regeneración con reintentos(Base62) ante colisión.
Caducidad: verificada al momento de la lectura del enlace (sin tareasprogramadas en el MVP).
Dependencias
fastapi, uvicorn[standard], sqlalchemy, pydantic, segno.
