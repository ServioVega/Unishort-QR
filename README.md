UniShort QR — Acortador URL + QR institucional
Servicio institucional para generar enlaces cortos y códigos QR (UNL).Ficha 3 del banco de proyectos. Stack: Python + FastAPI.

Requisitos
Git para Windows 2.x
Python 3.12 o superior (instalado desde python.org con "Add to PATH")
Instalación (PowerShell)
git clone https://github.com/ServioVega/Unishort-QR.gitcd Unishort-QRpy -m venv .venv.venv\Scripts\Activate.ps1pip install -r requirements.txt

Ejecución
uvicorn app.main:app --reload

Documentación interactiva: http://127.0.0.1:8000/docs
Verificación: http://127.0.0.1:8000/health -> {"status": "ok"}
Detener el servidor: Ctrl + C
Estrategia de ramas
main: estable, protegida (solo Pull Requests)
develop: integración del equipo
feature/*: trabajo por tareaCommits: Conventional Commits (feat:, fix:, docs:, chore:).Los Pull Requests se dirigen a develop con revisión cruzada.
Estructura
app/ backend FastAPIspecs/ artefactos SDD (spec, plan, tasks).specify/ constitutiontests/ pruebas