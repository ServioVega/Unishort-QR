Delimitación del problema — UniShort QR
Problema
La comunidad universitaria comparte enlaces a recursos académicos medianteservicios externos de acortamiento, sobre los cuales la Universidad tienecontrol limitado de administración, vigencia y supervisión, dificultando ladesactivación oportuna, la prevención de usos inadecuados y la obtención deestadísticas de acceso.

Actores y necesidades
Actor	Necesidad
Usuario creador (docente/administrativo)	Crear enlaces, obtener el QR, administrar y desactivar los suyos
Administrador institucional (DTI/TI)	Supervisar todos los enlaces, desactivar inadecuados, consultar métricas
Estudiante o público general	Acceder de forma ágil y segura al destino correcto
Requirente institucional (DTI)	Servicio institucional, mantenible, con seguridad y privacidad básicas
Alcance del primer incremento (MVP)
Autenticación básica · creación de enlaces con identificador único ·generación automática de QR de la URL corta · redirección HTTP 302 ·administración básica del creador · métricas agregadas sin datos personales.

Fuera del primer incremento
Creación masiva en lote · analítica avanzada (IP/geolocalización) ·personalización visual del QR · OAuth2/SSO institucional.

Restricciones y supuestos
Cero colisiones de identificadores (UNIQUE en BD incluso ante solicitudessimultáneas) · redirección < 1 s · sin almacenar IP ni datos del visitante ·dominio institucional definido por DTI.

Criterios de éxito
Enlace + QR en < 2 s · 2) 100 % redirecciones 302 en enlaces activos ·
QR legible en móviles estándar · 4) 0 % colisiones · 5) HTTP 404/410 enenlaces inactivos con mensaje informativo.
Riesgos tempranos y mitigación
Riesgo	Impacto	Prob.	Mitigación
Colisión de identificadores	Alto	Baja–Media	UNIQUE en BD, Base62, reintentos
Enlaces maliciosos (phishing)	Alto	Media	Validación de URL y desactivación por admin
Vulneración de privacidad	Alto	Baja	Solo métricas agregadas (principio constitucional)
Entorno no reproducible	Medio	Media	venv + requirements fijados + prueba cruzada
Cambios de requisitos del DTI	Medio	Media	Artefacto clarify y MVP acotado