# 🔗 UniShort QR — Acortador URL + QR Institucional

> **Servicio institucional para la generación de enlaces cortos y códigos QR dinámicos (UNL).**  
> *Ficha 3 del banco de proyectos.*

---

## 🛠️ Stack Tecnológico

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)
![Git](https://img.shields.io/badge/Git-2.x-F05032?logo=git&logoColor=white)

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de contar con los siguientes componentes instalados en tu sistema:

* **Git for Windows:** `2.x` o superior.
* **Python:** `3.12` o superior *(Asegúrate de marcar la casilla **"Add python.exe to PATH"** durante la instalación desde [python.org](https://www.python.org/))*.

---

## 🚀 Instalación (PowerShell)

Clona el repositorio, configura el entorno virtual e instala las dependencias ejecutando los siguientes comandos:

```powershell
# 1. Clonar el repositorio
git clone [https://github.com/ServioVega/Unishort-QR.git](https://github.com/ServioVega/Unishort-QR.git)

# 2. Acceder al directorio del proyecto
cd Unishort-QR

# 3. Crear el entorno virtual
py -m venv .venv

# 4. Activar el entorno virtual
.venv\Scripts\Activate.ps1

# 5. Instalar dependencias
pip install -r requirements.txt
