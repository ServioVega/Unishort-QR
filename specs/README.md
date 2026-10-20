# Specs — Mapa de features (features map)

Índice de todos los incrementos/features del proyecto UniShort QR gestionados con GitHub Spec Kit. Cada feature vive en su carpeta `NNN-<slug>/` y sus artefactos siguen el flujo SDD: constitution → specify → clarify → plan → tasks → implement → converge.

| Feature | Incremento | Título | Estado | Artefactos | Rama |
|---|---|---|---|---|---|
| `001-unishort-qr` | **F1** | Núcleo del servicio: crear enlaces+QR, redirección, expiración, administración, métricas agregadas | **Implementación** (artefactos SDD aprobados; código pendiente F1-00..F1-14) | `clarify.md` v1.0.0 · `spec.md` v1.0.0 · `plan.md` v1.0.0 · `tasks.md` v1.0.0 | `001-unishort-qr` |
| *(reservado)* | F2 | Extensión candidata: personalización de QR, notificaciones de expiración, analítica avanzada, SSO | Propuesto (backlog — no iniciar sin apertura formal) | — | — |

## Convenciones

1. **Numeración:** `NNN` correlativo por feature (001, 002, …); slug corto en kebab-case.
2. **Artefactos obligatorios por feature:** `spec.md` (qué), `plan.md` (cómo), `tasks.md` (desglose). `clarify.md` se crea con `/speckit.clarify` y registra decisiones D-NN.
3. **Transversal:** la constitución vive en `../.specify/memory/constitution.md` y aplica a TODAS las features; las decisiones de negocio viven en el `clarify.md` de cada feature, nunca en la constitución.
4. **Ramas:** una rama `NNN-<slug>` por feature; tareas internas en `feature/f1-XX-<slug>`; merge por PR a `develop` con CI verde.
5. **Estado de una feature:** Propuesto → Especificado → Planificado → Implementación → Convergido → Entregado. El estado se actualiza aquí al cerrar cada fase.

## Trazabilidad rápida (F1)

- Decisiones de negocio: `001-unishort-qr/clarify.md` (D1–D15; abiertas Q1–Q8 DTI, Q9 docente).
- Requisitos → tareas: `001-unishort-qr/tasks.md` §2 (columna Traza: cada tarea lista sus RF/E).
- Criterios de aceptación globales: `001-unishort-qr/spec.md` §11 (CA-01–CA-12).
