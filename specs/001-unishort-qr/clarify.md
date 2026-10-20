# Clarify — UniShort QR (Incremento 001)

| Campo | Valor |
|---|---|
| **Feature** | `001-unishort-qr` (F1) |
| **Versión** | 1.0.0 |
| **Fecha** | 2026-10-20 |
| **Estado** | Sesión de clarificación cerrada; 6 decisiones provisionales pendientes de confirmación externa |
| **Vinculados** | `../../.specify/memory/constitution.md` · `spec.md` v1.0.0 |

## 1. Propósito

Este documento registra las decisiones tomadas durante la fase `/speckit.clarify` para cerrar los huecos de ambigüedad del spec antes de planificar. Cada decisión se identifica como D-NN, indica su estado (**Cerrada** = decisión técnica o de negocio adoptada por el equipo, obliga a spec/plan/tasks; **Provisional** = adoptada como hipótesis de trabajo pero pendiente de confirmación externa) y su base. Ninguna decisión de negocio se convierte en principio de la constitución: los principios (constitución) gobiernan el proceso; las decisiones (este documento) fijan el producto.

## 2. Matriz de decisiones (D1–D15)

| ID | Tema | Decisión | Estado | Base / Consecuencia |
|---|---|---|---|---|
| **D1** | Dominio y URL base pública | El enlace corto se servirá bajo el dominio institucional definitivo que asigne la DTI (hipótesis de trabajo: `unl.edu.ec/s/{codigo}` o subdominio dedicado). El código es agnóstico al dominio: cambiar el dominio no invalida los códigos ni los QR. | **Provisional** (pendiente DTI) | RF-02, RN-09. El QR codifica la URL corta absoluta; al confirmarse el dominio solo cambia la configuración (`BASE_URL`), no los datos. |
| **D2** | Autenticación y emisión de credenciales | Los usuarios institucionales (Creador, Administrador) se autentican con usuario/contraseña institucional y obtienen un JWT HS256 de corta vida. NO se integra aún con el directorio/SSO institucional en F1. | **Provisional** (pendiente DTI) | RF-04, RNF-07. La integración SSO queda como candidata de F2; el diseño con puertos de seguridad permite sustituir el mecanismo sin tocar el dominio. |
| **D3** | Vigencia obligatoria y máxima | Todo enlace DEBE declarar fecha de caducidad; máximo 240 días naturales desde la creación. No existen enlaces permanentes en F1. | **Provisional** (pendiente DTI) | RN-01, E-03. Valor tomado del ciclo de campañas institucionales; si la DTI exige otro máximo, solo cambia la constante de regla. |
| **D4** | Máquina de estados y terminalidad | Estados del enlace: ACTIVO, EXPIRADO, DESACTIVADO. EXPIRADO y DESACTIVADO son terminales: sin reactivación en F1. Transiciones solo vía casos de uso con bloqueo `SELECT FOR UPDATE`. | **Cerrada** | RF-05, RN-06, Principio VIII. Elimina ambigüedad de "pausar/reactivar" y simplifica auditoría. |
| **D5** | Expiración por inactividad | Un enlace ACTIVO sin accesos registrados durante 180 días naturales pasa a EXPIRADO por inactividad. La medición usa `ultimo_acceso` (fecha, UTC) actualizado por el contador atómico. | **Provisional** (pendiente DTI) | RN-04, RF-07. Si la DTI confirma otro umbral, cambia la constante; la mecánica no varía. |
| **D6** | Formato del código corto | Códigos Base62 de 7 caracteres generados criptográficamente al azar; unicidad garantizada por UNIQUE en BD con reintentos ante colisión (doble defensa aplicación+BD). | **Cerrada** | RN-02, RNF-03, Principio VI. 62^7 ≈ 3.5×10^12 códigos: colisión estadísticamente despreciable y detectable. |
| **D7** | Verbo de redirección | Redirección con HTTP 302 (temporal), nunca 301 (permanente). | **Cerrada** | RN-10. El 301 se cachea en navegadores e impediría contar accesos y corregir errores; el 302 preserva control total. |
| **D8** | Contenido del código QR | El QR codifica SIEMPRE la URL corta pública (no el destino), en formato PNG y SVG generados con segno. | **Cerrada** | RF-03, RN-09. Permite reciclar material impreso aunque cambie el destino y mantiene el patrón de flujo institucional. |
| **D9** | Privacidad de métricas | Solo métricas agregadas por día (`acceso_diario`). NO se registra IP, user-agent, ni identificador alguno del visitante. | **Cerrada** | RN-07, RNF-06, Principio VII. Requisito del cliente (DTI) y del docente; es restricción dura. |
| **D10** | Contrato de respuesta y errores | Envelope universal JSON (`success/message/data/errors/meta`) en todas las respuestas JSON; catálogo estable de códigos de error (12 códigos en spec). Excepciones al envelope: 302, binario del QR, 204/HEAD. | **Cerrada** | Principio V, Principio X. Da contratos deterministas a clientes y pruebas. |
| **D11** | Límites y validación del destino | URL destino: obligatoria, esquema http/https, longitud ≤ 2048, sin credenciales embebidas; bloqueo de destinos internos (localhost, 127.0.0.0/8, 10/8, 172.16/12, 192.168/16, 169.254/16, ::1, metadatos 169.254.169.254). | **Cerrada** | RN-05, RNF-07 (SSRF). Previene abuso del servicio como pivote hacia redes internas. |
| **D12** | Base de datos por entorno | Desarrollo y pruebas unitarias: SQLite. CI (concurrencia) y entrega/producción: PostgreSQL 16. Pendiente confirmar con el docente si la entrega exige PostgreSQL en la demo o basta la matriz dev/CI. | **Provisional** (pregunta abierta al docente) | Principio VI, P-04 del plan. El puertos-de-repositorio y Alembic hacen el cambio declarativo. |
| **D13** | Mecanismo de expiración | Doble mecanismo: (1) job programado idempotente (APScheduler) que transiciona ACTIVO→EXPIRADO por fecha/inactividad; (2) verificación en lectura en la ruta de redirección como última línea de defensa (nunca redirige un enlace vencido aunque el job tarde). | **Cerrada** | RF-07, Principio VIII. Reconcilia el plan original del equipo ("verificación al leer") con el requisito de estado observable: el job materializa el estado; la lectura garantiza la corrección. |
| **D14** | Estilo arquitectónico | Monolito modular en capas (API/aplicación/dominio/infraestructura) con dominio puro y puertos `typing.Protocol`; sin microservicios en F1. | **Cerrada** | Principio II, P-03 del plan. Escala de proyecto estudiantil: un despliegue, evolución simple. |
| **D15** | Flujo de trabajo y CI | GitFlow simplificado (main protegida, develop, feature/*), Conventional Commits, revisión cruzada; CI en GitHub Actions: ruff → pytest (SQLite) → pytest concurrencia (PostgreSQL) → alembic upgrade/downgrade. | **Cerrada** | Principios XII y XIII. Es la política evaluable del curso. |

## 3. Preguntas abiertas — para la DTI (8)

Estas preguntas NO bloquean el desarrollo F1: cada una tiene una hipótesis provisional que permite avanzar; la confirmación solo puede ajustar constantes o configuración.

| # | Pregunta | Decisiones que dependen | Hipótesis de trabajo si no responde |
|---|---|---|---|
| Q1 | ¿Cuál es el dominio definitivo (o subdominio) para los enlaces cortos y los QR? | D1 | Usar `BASE_URL` configurable; dominio de prueba en desarrollo. |
| Q2 | ¿Se confirma que F1 usa credenciales locales (usuario/contraseña institucional) sin SSO? | D2 | JWT local con cuentas creadas por el Administrador. |
| Q3 | ¿Se confirma el máximo de vigencia de 240 días por enlace? | D3 | 240 días como constante de regla. |
| Q4 | ¿Se confirma el umbral de inactividad de 180 días para expirar un enlace? | D5 | 180 días como constante de regla. |
| Q5 | ¿Se confirma el formato QR PNG + SVG del enlace corto con segno? | D8 | PNG + SVG. |
| Q6 | ¿Existe política de retención de enlaces expirados (purga física) o permanecen históricos? | D4, RF-07 | Retención histórica indefinida (sin borrado) en F1. |
| Q7 | ¿Qué ocurre si un Solicitante necesita reactivar un enlace expirado por inactividad tras una campaña? (¿nueva solicitud o reactivación asistida?) | D4 | Nueva solicitud (los terminales no se reactivan). |
| Q8 | ¿Se requieren notificaciones (correo) previas a la expiración de un enlace? | D3, alcance F1 | Sin notificaciones en F1; candidata para F2. |

## 4. Preguntas abiertas — para el docente (1)

| # | Pregunta | Decisiones que dependen | Hipótesis de trabajo si no responde |
|---|---|---|---|
| Q9 | ¿La entrega del incremento F1 exige demostrar PostgreSQL (D12), o es suficiente la matriz SQLite (dev/pruebas) + PostgreSQL (CI)? | D12, P-04 | Entrega con SQLite en demo + PostgreSQL probado en CI. |

## 5. Impacto y trazabilidad

- **Spec:** todas las decisiones cerradas (D4, D6–D11, D13–D15) están incorporadas como requisitos (RF/RN/RNF) de `spec.md` v1.0.0 sin marcadores de ambigüedad.
- **Decisiones provisionales (D1, D2, D3, D5, D12):** aparecen en el spec con su hipótesis de trabajo y están etiquetadas; su confirmación exterior NO modifica estructura ni contrato, solo constantes/configuración.
- **Tareas:** el desglose de `tasks.md` incluye la tarea de configuración externa (`BASE_URL`, umbrales) centralizada para que cada respuesta externa sea un cambio de una línea.
- **Registro:** nuevas dudas surgidas durante plan/implementación DEBEN añadirse a esta matriz con ID correlativo (D16+) y trazar su impacto.
