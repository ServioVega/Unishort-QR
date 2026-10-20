# Tasks — UniShort QR (Incremento 001)

| Campo | Valor |
|---|---|
| **Feature** | `001-unishort-qr` (F1) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-10-20 |
| **Vinculados** | `spec.md` v1.0.0 · `plan.md` v1.0.0 · `clarify.md` v1.0.0 |

## 1. Seguimiento del equipo (tracker original, preservado)

Estado del equipo al 2026-10-12 (se conserva como registro histórico de gestión; los T1–T5 se mantienen Done):

| ID | Tarea | Issue | Responsable | Estado |
|---|---|---|---|---|
| T1 | Configurar repositorio y ramas | #1 | Servio | Done |
| T2 | Entorno reproducible y README | #2 | Wilson | Done |
| T3 | Esqueleto FastAPI + /health | #3 | Víctor | Done |
| T4 | Constitution y spec | #4 | María | Done |
| T5 | Delimitación problema/riesgos | #5 | Martina | Done |
| T6 | Modelo entidad Enlace (UNIQUE) | #6 | Servio | **Pending → absorbido por F1-02** |
| T7 | POST /shorten | #7 | Servio | **Pending → absorbido por F1-03/F1-04** |
| T8 | GET /s/{id} con 302/404/410 | #8 | Wilson | **Pending → absorbido por F1-05** |

> T6–T8 no se pierden: se integran al desglose técnico por fases (sección 2), que añade los criterios de done, dependencias y trazabilidad a requisitos que el tracker manual no registraba.

## 2. Desglose técnico por fases (SDD)

Convenciones: cada tarea termina con PR a `develop` (revisión cruzada, Conventional Commits, CI verde). "Criterio de done" es objetivo y verificable. Trazabilidad: RF/E del `spec.md` y P del `plan.md`.

### Fase 0 — Base transversal

| ID | Tarea | Criterio de done | Traza | Estado |
|---|---|---|---|---|
| F1-00 | Scaffolding del incremento: `pyproject.toml`, configuración `pydantic-settings` (BASE_URL, umbrales 240/180, límites), `pyproject` ruff, estructura de carpetas del plan §5 | `uvicorn app.main:app` levanta; `/health` 200; config cargada por entorno | P-01, P-05 | Pending |
| F1-01 | Envelope universal + manejo de excepciones → catálogo: middleware `request_id`, builder del envelope, traducción de excepciones de dominio a códigos del catálogo (12) | Toda respuesta JSON tiene las 5 claves y `meta` completa; pruebas de envelope verdes | P-10 del spec (RNF-08), D10 | Pending |

### Fase 1 — Dominio y persistencia (absorbe T6)

| ID | Tarea | Criterio de done | Traza | Estado |
|---|---|---|---|---|
| F1-02 | Dominio puro: entidades (Enlace, Solicitud, Usuario, AccesoDiario), reglas RN-01..RN-11, errores de dominio, puertos Protocol; modelos ORM + migración inicial reversible | `app/dominio/` sin imports de framework; migración sube y baja sin error; UNIQUE `codigo_corto` en esquema; índice parcial único solicitudes PENDIENTES | RF-01, RN-01..11, P-03/P-04, CA-11 | Pending |
| F1-02b | Generador de códigos Base62×7 con reintentos ante colisión (mín. 5) | Prueba de colisión simulada regenera y crea (E-09); formato y longitud verificados | RN-02, RNF-03 | Pending |

### Fase 2 — Creación (absorbe T7)

| ID | Tarea | Criterio de done | Traza | Estado |
|---|---|---|---|---|
| F1-03 | Seguridad: Argon2id + JWT HS256, endpoint `POST /api/v1/auth/token`, dependencias de rol | 401 `CREDENCIALES_INVALIDAS` en login fallido/token vencido; 403 `PERMISO_DENEGADO` sin rol; hash verificable en BD (CA-09) | RF-04, RNF-07 | Pending |
| F1-04 | Caso de uso CrearEnlace + `POST /api/v1/links` (+ `POST /api/v1/solicitudes` con RN-08) + QR segno PNG/SVG | E-01/E-02/E-03/E-04 verdes; creación ≤ 2 s (CA-02); SOLICITUD_DUPLICADA 409 en duplicado pendiente | RF-01/RF-03, RN-01/05/08/09 | Pending |

### Fase 3 — Redirección (absorbe T8)

| ID | Tarea | Criterio de done | Traza | Estado |
|---|---|---|---|---|
| F1-05 | `GET /s/{codigo}`: lookup, verificación en lectura (fecha/inactividad), 302/404/410 | E-05/E-06/E-07/E-08 verdes; 302 sin envelope; 404/410 con envelope y catálogo | RF-02, RN-06/10, D13 | Pending |
| F1-06 | Contador atómico: UPSERT `acceso_diario` + `ultimo_acceso` | E-10: 25 accesos concurrentes → conteo exacto (PostgreSQL en CI) | RF-08, Principio VI | Pending |

### Fase 4 — Administración y métricas

| ID | Tarea | Criterio de done | Traza | Estado |
|---|---|---|---|---|
| F1-07 | Listar/detalle enlaces (paginado, filtro estado, alcance por rol) | Creador ve solo los suyos; Admin ve todos; paginación y filtros probados | RF-05, RN-11 | Pending |
| F1-08 | Desactivar enlace (`PATCH /links/{id}/desactivar`) con `SELECT FOR UPDATE` | Desactivación → 204; redirecciones → 410; sobre terminal → 409 `TRANSICION_NO_PERMITIDA` (E-07) | RF-05, RN-06, D4 | Pending |
| F1-09 | Métricas agregadas (`GET /links/{id}/metrics`) | Total + serie diaria correctos; cero datos de visitantes (CA-08) | RF-06, RN-07 | Pending |

### Fase 5 — Expiración programada

| ID | Tarea | Criterio de done | Traza | Estado |
|---|---|---|---|---|
| F1-10 | Job APScheduler → caso de uso ExpirarEnlaces (fecha e inactividad, lotes, idempotente) | freezegun: expira por fecha y por 180 días; doble ejecución sin efectos duplicados; job documentado en README operativo | RF-07, RN-04, P-08 | Pending |

### Fase 6 — Calidad, CI y entrega

| ID | Tarea | Criterio de done | Traza | Estado |
|---|---|---|---|---|
| F1-11 | Suite de pruebas completa: unitarias (dominio, freezegun), integración (API SQLite), concurrencia (PostgreSQL, marcadas CI) | Cobertura de dominio/aplicación al umbral acordado; todos los E-01..E-10 mapeados a pruebas | Principio IX, CA-07/CA-12 | Pending |
| F1-12 | Workflow GitHub Actions: ruff → pytest SQLite → pytest concurrencia PostgreSQL → alembic upgrade/downgrade | CI verde en PR; merge bloqueado en rojo (regla de repo) | Principio XIII, CA-11 | Pending |
| F1-13 | Medición de rendimiento redirección (< 1 s) y creación (≤ 2 s) documentada | Registro de medición en el repo (doc de incremento o prueba de temporización) | RNF-01/RNF-02, CA-02/CA-03 | Pending |
| F1-14 | Cierre del incremento: actualizar README operativo (arranque, job, variables), specs/README.md (estado), memoria de uso de IA (Principio XVII) | Documentos actualizados; tags/merge a main con PR | Principios XII/XVII | Pending |

## 3. Orden de ejecución y paralelismo

- **Serie crítica:** F1-00 → F1-01 → F1-02 → (F1-03 ∥ F1-02b) → F1-04 → F1-05 → F1-06 → F1-07/F1-08/F1-09 (paralelizables) → F1-10 → F1-11/F1-12 (paralelizables) → F1-13 → F1-14.
- Tareas con `∥` pueden repartirse entre integrantes en ramas `feature/*` distintas sin conflicto (puertos estabilizan interfaces).
- Cada tarea referencía su issue de GitHub y su rama: `feature/f1-04-crear-enlace`.

## 4. Historial

| Versión | Fecha | Cambios |
|---|---|---|
| 0.1.0 (repo inicial) | 2026-10-12 | Tracker manual T1–T8 (T1–T5 Done). |
| 1.0.0 | 2026-10-20 | Desglose SDD por fases F1-00..F1-14 con criterios de done y trazabilidad; tracker del equipo preservado en §1; T6–T8 integrados. |
