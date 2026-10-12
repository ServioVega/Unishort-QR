Especificación — UniShort QR (Incremento 001)
Problema
La comunidad universitaria comparte enlaces mediante servicios externos deacortamiento, con control limitado de administración, vigencia y estadísticas.

Actores
Creador (docente/administrativo), Administrador institucional (DTI/TI),Visitante (estudiante/público), Requirente (DTI).

Requisitos funcionales
RF1 (P1) Crear enlace: el creador envía una URL original y recibe unenlace corto con identificador alfanumérico único y su imagen QR.
Aceptación: la URL se valida (HTTP/HTTPS); el identificador no se repite;la respuesta incluye el enlace corto y el QR en menos de 2 s.
RF2 (P1) Redirigir: al visitar /s/{id} el servicio responde HTTP 302hacia la URL original si el enlace está activo y no expiró.
Aceptación: enlace inexistente → 404; deshabilitado → 404 o 410;expirado → 410; todos con mensaje informativo.
RF3 (P1) Generar QR: el QR codifica la URL corta (no el destino),para mantener control de redirección y métricas.
RF4 (P1) Autenticación básica: solo usuarios institucionales con rolválido pueden crear y administrar enlaces.
RF5 (P2) Administrar: el creador lista, desactiva y consulta vigenciade sus enlaces; el administrador puede desactivar cualquiera.
RF6 (P2) Métricas: contador agregado de clics por enlace, sin IP nidatos personales.
Requisitos no funcionales
Redirección con respuesta del servidor < 1 s.
0 % de colisión de identificadores (unicidad garantizada en la BD).
No se almacenan IP ni datos personales de visitantes.
Criterios de éxito (del ACD1)
Enlace + QR generados en < 2 s. 2. 100 % de redirecciones 302 exitosas enenlaces activos. 3. QR legible en Android/iOS. 4. 0 % colisiones.
404/410 estandarizado en enlaces inactivos.
Fuera de alcance (incremento 001)
Creación masiva en lote; analítica avanzada (IP/geolocalización);personalización visual del QR; OAuth2/SSO institucional.

Preguntas abiertas (clarify — pendientes con DTI)
¿Quién puede crear enlaces (estudiantes también o solo docentes/admin)?
¿Los enlaces expiran por defecto o solo cuando se desactivan?
¿Qué nivel de analítica se permite recolectar?
