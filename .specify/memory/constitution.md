Constitución del equipo — UniShort QR
Propósito
Servicio institucional de acortamiento de URLs y códigos QR para la UNL.

Principios rectores
Privacidad primero: no se almacenan direcciones IP, huellas de navegadorni datos personales de visitantes. Solo métricas agregadas.
Especificación antes que código: todo cambio funcional se refleja primeroen specs/001-unishort-qr/spec.md.
Calidad de código: Python compatible con PEP 8, type hints y validacióncon Pydantic.
Seguridad básica: validar la URL de destino (HTTP/HTTPS) y aplicarpermisos por rol.
Trazabilidad: commits con Conventional Commits y PR con revisión cruzada.
Alcance controlado: ninguna funcionalidad nueva entra al MVP sinregistrarse en clarify y tasks.
Flujo de trabajo Git
main: estable, protegida, solo Pull Requests.
develop: integración; base de las ramas feature/*.
feature/: una tarea por rama.
Commits: feat:, fix:, docs:, chore:, test:.
Todo PR requiere revisión de otro integrante.
Criterios de aceptación globales
El entorno se reproduce con el README sin ayuda oral.
Enlaces inactivos o expirados responden HTTP 404/410.
Redirección 302 con respuesta del servidor < 1 segundo.
