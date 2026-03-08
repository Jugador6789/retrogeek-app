# 🎮 RetroGeek Store & PC Hardware Scanner

Una plataforma moderna de distribución de videojuegos construida con React, Tauri y Python. Incluye un escáner de telemetría real que lee el hardware de la computadora del usuario usando WMI.

## 🚀 Tecnologías Usadas
* **Frontend:** React, Vite, Tauri, CSS puro (Estilo Epic Games).
* **Backend:** Python, Flask, SQLite3.
* **Telemetría:** `WMI`, `psutil` (Lectura de CPU, GPU y RAM en tiempo real).

## 🛠️ Cómo instalar y correr este proyecto

### 1. Preparar el Backend (Python)
Abre una terminal, entra a la carpeta `motor-python` y ejecuta:
```bash
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
python generar_bd.py
python servidor.py