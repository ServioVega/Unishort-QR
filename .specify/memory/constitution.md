# Constitución del Proyecto — UniShort QR

| Campo | Valor |
|---|---|
| **Proyecto** | UniShort QR — Servicio institucional de acortamiento de URLs y códigos QR (UNL) |
| **Incremento** | F1 — `001-unishort-qr` |
| **Versión de la constitución** | 2.0.0 |
| **Fecha de ratificación** | 2026-10-20 |
| **Estado** | RATIFICADA |
| **Autoridad** | Equipo del curso "Desarrollo Basado en Plataformas" — Universidad Nacional de Loja |

## 1. Propósito y ámbito

Esta constitución define los principios innegociables que gobiernan la especificación, el diseño, la implementación, las pruebas y la evolución de UniShort QR. Aplica a **todo** artefacto del proyecto: documentos SDD (spec, clarify, plan, tasks), código fuente, migraciones de base de datos, pruebas, configuración de CI/CD y documentación. Ningún artefacto, decisión técnica o línea de código puede contradecir estos principios; si un principio impide avanzar, se enmienda la constitución por el proceso de gobernanza (sección 3) **antes** de desviarse. Este documento no registra decisiones de negocio (las decisiones D1–D15 viven en `specs/001-unishort-qr/clarify.md`); registra únicamente reglas de calidad y de proceso que sobreviven a cualquier cambio de requisitos.

## 2. Principios rectores

### Principio I — Especificación como fuente única de verdad (SDD)

**Obligaciones**
- DEBE existir un `spec.md` aprobado antes de escribir código funcional, y todo requisito implementado DEBE ser trazable a un RF del spec y a una tarea de `tasks.md`.
- NO DEBE implementarse funcionalidad alguna que no esté registrada en el spec o en el desglose de tareas vigentes.
- DEBE actualizarse el spec (con nueva versión) antes que el código cuando cambie un requisito.

**Justificación:** la especificación previa elimina la ambigüedad, evita retrabajo y permite que cualquier integrante (o agente de IA) entienda el qué y el porqué sin reconstruir contexto.

**Criterio verificable:** cada endpoint publicado tiene un RF asociado en `spec.md`, una tarea en `tasks.md` y al menos un escenario E que lo cubre; la ejecución de `/speckit.analyze` no reporta discrepancias entre constitution/spec/plan/tasks.

### Principio II — Arquitectura modular en capas con dominio puro

**Obligaciones**
- DEBE organizarse el código en capas: API (FastAPI), aplicación (casos de uso), dominio (entidades y reglas) e infraestructura (SQLAlchemy, QR, seguridad, reloj).
- DEBE mantenerse el dominio libre de dependencias de framework: las entidades del dominio NO DEBEN importar FastAPI, SQLAlchemy ni Pydantic.
- DEBE inyectarse las dependencias externas mediante puertos (`typing.Protocol`), incluido un reloj inyectable para el tiempo.

**Justificación:** un dominio puro es testeable sin servidor ni base de datos, y las capas aíslan el impacto de cambios tecnológicos (p. ej. migrar SQLite→PostgreSQL) al perímetro del sistema.

**Criterio verificable:** el módulo `app/dominio/` no contiene imports de fastapi/sqlalchemy/pydantic; la regla se comprueba con una prueba de arquitectura que recorre los imports del paquete.

### Principio III — Diseño con principios SOLID

**Obligaciones**
- DEBE haber una única razón de cambio por módulo: los routers no contienen reglas de negocio y los casos de uso no construyen respuestas HTTP.
- DEBE depender el código de abstracciones (puertos) y no de implementaciones concretas (repositorios, generador de códigos, reloj).
- NO DEBE modificarse una clase existente para añadir un caso de uso nuevo cuando pueda extenderse con una implementación de puerto.

**Justificación:** SOLID mantiene el coste de cambio plano conforme crece el sistema, lo que es decisivo en un equipo estudiantil rotativo donde cada integrante toca código ajeno.

**Criterio verificable:** en la revisión de cada PR se verifica que la lógica de negocio reside en `aplicacion/` o `dominio/`; ninguna regla de negocio vive dentro de un router.

### Principio IV — API REST versionada y coherente

**Obligaciones**
- DEBE exponerse toda la funcionalidad bajo el prefijo `/api/v1` y describirse mediante OpenAPI generado por FastAPI.
- DEBE usar códigos HTTP semánticos (201 creación, 302 redirección, 204 sin contenido, 404 inexistente, 410 gone, 409 conflicto, 422 validación).
- NO DEBE romperse la compatibilidad de endpoints publicados dentro del mismo incremento; los cambios incompatibles exigen una versión nueva (`/api/v2`).

**Justificación:** la versión en la ruta protege a consumidores (imprimibles QR, integraciones DTI) de cambios rompientes y documenta explícitamente la evolución del contrato.

**Criterio verificable:** el esquema OpenAPI (`/docs`) lista todos los endpoints bajo `/api/v1` y cada respuesta de error corresponde al catálogo del spec.

### Principio V — Contrato de respuesta universal (envelope)

**Obligaciones**
- DEBE envolver toda respuesta JSON en el envelope estándar: `success`, `message`, `data`, `errors`, `meta` (con `request_id`, `timestamp`, `version`).
- NO DEBE aplicar el envelope a las excepciones definidas: la redirección 302, el binario del QR y las respuestas 204/HEAD, que siguen el protocolo HTTP puro.
- DEBE incluirse el mismo `request_id` en la respuesta y en el log asociado.

**Justificación:** un único formato de éxito y error simplifica a los clientes y hace determinista el manejo de errores; las excepciones preservan la semántica HTTP que herramientas (navegadores, lectores QR) esperan.

**Criterio verificable:** la suite de pruebas afirma la presencia y tipos de las cinco claves del envelope en cada endpoint JSON, y la ausencia del envelope en 302/QR/204.

### Principio VI — Persistencia con integridad garantizada

**Obligaciones**
- DEBE garantizarse unicidad de `codigo_corto` mediante restricción UNIQUE en base de datos, no solo en aplicación.
- DEBE realizarse el conteo de accesos con UPSERT atómico en la tabla `acceso_diario` (sin leer-modificar-escribir) y bloqueo `SELECT FOR UPDATE` en operaciones de transición de estado.
- DEBEN ser reversibles todas las migraciones Alembic (upgrade/downgrade probadas en CI).
- NO DEBE confiarse en la generación en memoria de códigos como garantía de unicidad: la BD es la última línea de defensa con reintentos ante colisión.

**Justificación:** la concurrencia (dos clics simultáneos, dos creaciones simultáneas) puede corromper contadores o duplicar códigos si la integridad depende solo de la aplicación; la BD la garantiza de forma incondicional.

**Criterio verificable:** una prueba de concurrencia con PostgreSQL (servicio en CI) ejecuta accesos paralelos y afirma el conteo exacto; CI ejecuta `alembic upgrade head` y `alembic downgrade base` sin error.

### Principio VII — Seguridad y privacidad por diseño

**Obligaciones**
- NO DEBE almacenarse dirección IP, user-agent, cookies ni dato personal alguno de visitantes en base de datos, logs o métricas.
- DEBE validarse toda URL de destino: solo esquemas http/https, longitud ≤ 2048, y bloqueo de destinos internos (localhost, rangos privados, metadatos) para prevenir SSRF.
- DEBE almacenarse contraseñas con hash Argon2id y emitirse tokens JWT HS256 de corta vida; NO DEBE persistirse contraseñas en claro ni tokens sin expiración.
- DEBE restringirse la escritura (crear, desactivar, ver métricas) a roles institucionales autenticados; el visitante solo redirección pública.

**Justificación:** el servicio opera con enlaces institucionales y público general; una fuga de PII o un SSRF comprometería la confianza y la normativa de protección de datos de la universidad.

**Criterio verificable:** una prueba de suite afirma que no existen columnas de IP/PII en el esquema y que los logs de redirección no contienen identificadores de visitante; pruebas de seguridad cubren 422 para destinos internos y 401/403 para escritura sin rol.

### Principio VIII — Gobernanza del ciclo de vida de los enlaces

**Obligaciones**
- DEBE modelarse el ciclo de vida como máquina de estados explícita: ACTIVO → EXPIRADO (por fecha o por inactividad) o ACTIVO → DESACTIVADO, con todos los estados finales terminales.
- NO DEBE permitirse la reactivación de un enlace en estado terminal, ni la mutación del destino tras la creación.
- DEBE aplicarse la transición de forma idempotente (re-ejecutar el job de expiración no produce efectos duplicados).

**Justificación:** los estados terminales dan certeza normativa (un enlace retirado no "revive" por error), y la idempotencia permite reintentos seguros del planificador sin corromper datos.

**Criterio verificable:** pruebas con `freezegun` cubren expiración por fecha, expiración por 180 días de inactividad y rechazo de reactivación (409 TRANSICION_NO_PERMITIDA); ejecutar el job dos veces produce el mismo estado.

### Principio IX — Calidad verificable mediante pruebas automatizadas

**Obligaciones**
- DEBE cubrirse cada RF con al menos una prueba automatizada (pytest) y cada regla de negocio con al menos un caso negativo.
- DEBE probarse la concurrencia contra PostgreSQL y el tiempo (expiración) con `freezegun`, no con esperas reales.
- NO DEBE fusionarse un PR con pruebas fallidas o con cobertura de dominio/aplicación descendente.

**Justificación:** las pruebas automatizadas son el único criterio objetivo de "terminado" y protegen el incremento ante cambios de última hora de fin de ciclo.

**Criterio verificable:** CI ejecuta la suite completa en verde; el informe de cobertura mantiene o mejora el umbral acordado en los módulos de dominio y aplicación.

### Principio X — Errores con catálogo estable de códigos

**Obligaciones**
- DEBE identificarse cada error de aplicación con un código estable del catálogo del spec (p. ej. `URL_INVALIDA`, `ENLACE_NO_DISPONIBLE`, `PERMISO_DENEGADO`).
- NO DEBE exponerse trazas internas (stack traces) al cliente; el detalle técnico va a logs con `request_id`.
- DEBE documentarse todo código nuevo o modificado en el catálogo del spec antes de usarse.

**Justificación:** los códigos estables permiten a los clientes y al equipo de soporte diagnosticar sin inspeccionar el servidor, y desacoplan el mensaje humano (mutable) del identificador (inmutable).

**Criterio verificable:** cada respuesta 4xx/5xx del sistema contiene exactamente un código del catálogo; no existe respuesta de error con código improvisado.

### Principio XI — Modelado y documentación viva

**Obligaciones**
- DEBE mantenerse el modelado con estándares: C4 (contexto/contenedor/componente), UML (estados/secuencia), ADR para decisiones técnicas, BPMN para procesos con actores, OpenAPI para el contrato y Markdown para documentos.
- DEBE actualizarse el diagrama afectado en el mismo PR que modifica la arquitectura o el contrato.
- NO DEBE archivarse documentación en formatos binarios no versionables (Word/PDF en el repo) para artefactos de ingeniería.

**Justificación:** los diagramas estandarizados son el lenguaje común del curso y de la DTI; mantenerlos junto al código evita la documentación fósil.

**Criterio verificable:** cada ADR numerado (P-01…P-10 del plan) tiene fecha, estado y consecuencia; los diagramas C2/C3 del plan reflejan el código real del incremento.

### Principio XII — Gestión de código con GitFlow simplificado y Conventional Commits

**Obligaciones**
- DEBE trabajarse con `main` protegida (solo PR), `develop` de integración y ramas `feature/*` por tarea.
- DEBE escribirse cada commit con Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `test:`) y someterse todo PR a revisión cruzada de otro integrante.
- NO DEBE enviarse commits directos a `main` ni fusionarse PR sin revisión.

**Justificación:** la disciplina de ramas y commits es evaluable en el curso y habilita trazabilidad bidireccional entre commit ↔ tarea ↔ requisito.

**Criterio verificable:** el historial de `main` contiene solo commits de merge de PR con prefijos válidos; cada PR referencía al menos un ID de tarea de `tasks.md`.

### Principio XIII — Integración continua como puerta de calidad

**Obligaciones**
- DEBE ejecutarse en cada PR el pipeline: análisis estático (ruff) → pruebas con SQLite → pruebas de concurrencia con servicio PostgreSQL → verificación de migraciones (upgrade/downgrade).
- NO DEBE fusionarse ningún PR cuyo pipeline falle, sin excepción ni atajos.
- DEBE fallar el pipeline ante cualquier violación de estilo detectada por ruff (sin exclusiones ad-hoc en el código).

**Justificación:** la CI convierte la constitución en un mecanismo automático de cumplimiento: lo que no pasa el pipeline no existe.

**Criterio verificable:** el workflow de GitHub Actions está presente en `.github/workflows/`, corre en todos los PR y su estado es obligatoriamente verde antes del merge.

### Principio XIV — Observabilidad operativa

**Obligaciones**
- DEBE registrarse cada petición con un `request_id` único propagado a logs y respuestas.
- DEBE exponerse el endpoint `/health` (fuera de `/api/v1`) para verificación de disponibilidad.
- NO DEBE registrarse en logs el contenido completo de URLs de destino de visitantes cuando pueda contener datos sensibles; se registra el código corto y el resultado.

**Justificación:** sin correlación por `request_id`, diagnosticar un incidente en producción depende de adivinar; con ella, cada respuesta es rastreable a su registro.

**Criterio verificable:** cada respuesta JSON incluye `meta.request_id` y existe un log con ese mismo identificador; `/health` responde 200 con estado del servicio.

### Principio XV — Rendimiento con presupuesto definido

**Obligaciones**
- DEBE responder la redirección en menos de 1 segundo (tiempo de servidor) y la creación de enlace + QR en menos de 2 segundos.
- DEBE verificarse el presupuesto con pruebas de rendimiento razonables o mediciones documentadas en el incremento.
- NO DEBE introducirse una dependencia o llamada síncrona pesada en la ruta crítica de redirección (la ruta caliente debe ser mínima: lookup + expiración + contador).

**Justificación:** el QR impreso se escanea en la calle: la latencia de redirección es el contrato percibido del servicio y su degradación anula el valor del producto.

**Criterio verificable:** existe una medición o prueba registrada en el repositorio que documenta p95 < 1 s para `GET /s/{codigo}` en el entorno de pruebas.

### Principio XVI — Alcance por incrementos (F1 → F2 → F3)

**Obligaciones**
- DEBE limitarse el incremento F1 al alcance definido en `spec.md` (crear/redirigir/administrar/métricas/QR/expiración).
- NO DEBE incorporarse funcionalidad de F2 o F3 (p. ej. personalización visual de QR, analítica avanzada, lotes) al código de F1 sin apertura formal de incremento nuevo.
- DEBE registrarse toda idea fuera de alcance en el backlog documental (clarify/tasks) como candidata futura, sin implementarla.

**Justificación:** el alcance congelado por incremento es la única defensa realista contra el desbordamiento en un ciclo académico corto.

**Criterio verificable:** ninguna funcionalidad presente en el código carece de RF en el spec del incremento; las peticiones fuera de alcance quedan registradas como pendientes y no como código.

### Principio XVII — Uso responsable de inteligencia artificial

**Obligaciones**
- DEBE declararse el uso de herramientas de IA (agentes, generadores) en la memoria del proyecto y revisarse humanamente todo artefacto o código generado antes de integrarse.
- NO DEBE aceptarse código generado que el equipo no sea capaz de explicar línea por línea en la defensa.
- DEBE tratarse los datos del proyecto (specs, URLs institucionales) como no confidenciales antes de enviarlos a servicios de IA externos.

**Justificación:** la IA acelera la producción, pero la responsabilidad académica y técnica del resultado es del equipo; la comprensión verificable es parte del criterio de evaluación.

**Criterio verificable:** la memoria del incremento contiene una sección de uso de IA con herramientas empleadas y revisión humana realizada; cada integrante puede explicar los módulos que integró.

## 3. Gobernanza

### 3.1 Proceso de enmienda

Cualquier integrante puede proponer una enmienda mediante PR sobre este archivo, con: (a) texto del cambio, (b) justificación, (c) impacto en artefactos existentes. La enmienda requiere aprobación de al menos otro integrante (revisión cruzada) y, cuando afecte criterios evaluables, la validación del docente.

### 3.2 Versionado semántico de la constitución

- **MAJOR:** elimina o reemplaza principios, o cambia obligaciones DEBE/NO DEBE de forma incompatible con artefactos existentes.
- **MINOR:** añade un principio nuevo o criterios verificables adicionales compatibles con lo existente.
- **PATCH:** correcciones de redacción, referencias o formato sin cambio semántico.

### 3.3 Precedencia

Ante conflicto entre esta constitución y cualquier otro artefacto, prevalece la constitución. Ante conflicto entre spec y plan, prevalece el spec (el qué sobre el cómo). Las decisiones de negocio cerradas en `clarify.md` vinculan a spec y plan.

## 4. Registro de modificaciones

| Versión | Fecha | Cambios | Clase |
|---|---|---|---|
| 1.0.0 | 2026-10-12 | APE-001: aprobación inicial con 6 principios rectores (privacidad, SDD, calidad, seguridad, trazabilidad, alcance) | MAJOR |
| 2.0.0 | 2026-10-20 | Reescritura completa con la plantilla institucional: 17 principios I–XVII con obligaciones DEBE/NO DEBE, justificación y criterio verificable; gobernanza con versionado semántico; informe de resultado esperado. Los 6 principios originales quedan absorbidos (privacidad→VII, SDD→I, calidad→III/IX, seguridad→VII, trazabilidad→XII, alcance→XVI) | MAJOR |

## 5. Informe de resultado esperado

Con esta constitución ratificada, al cierre del incremento F1 el proyecto debe presentar: (1) un servicio FastAPI operable con contrato `/api/v1` documentado en OpenAPI y envelope universal; (2) una suite de pruebas automatizadas verde en CI que cubra los RF-01–RF-08, incluida concurrencia real sobre PostgreSQL y expiración temporal con `freezegun`; (3) artefactos SDD trazados (constitution ↔ clarify ↔ spec ↔ plan ↔ tasks) sin discrepancias al ejecutar `/speckit.analyze`; (4) un historial Git con GitFlow simplificado y Conventional Commits revisados por pares; y (5) evidencias verificables de privacidad (sin IP/PII), integridad (UNIQUE, UPSERT atómico) y rendimiento (redirección < 1 s). El incumplimiento de cualquier principio debe ser detectable por el criterio verificable asociado, no depender de la memoria del equipo.
