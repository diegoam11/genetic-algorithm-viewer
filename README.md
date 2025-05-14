## Proyecto Django - Guía de Inicio Rápido

Esta guía te ayudará a configurar y ejecutar un proyecto Django en tu entorno local, incluyendo entornos virtuales y los comandos necesarios para Windows, macOS y Linux.

---

## 🛠️ **Requisitos Previos**
- Python 3.8+ instalado.  
- pip (gestor de paquetes de Python).  

---

## 🚀 **1. Clonar el Repositorio**
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```

---

## 🌐 **2. Crear un Entorno Virtual**
Para aislar las dependencias del proyecto, es recomendable crear un entorno virtual.

### Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

> Para salir del entorno virtual:
```bash
deactivate
```

---

## 📦 **3. Instalar Dependencias**
Una vez dentro del entorno virtual, instala las dependencias:
```bash
pip install -r requirements.txt
```

---


## ▶️ **6. Ejecutar el Servidor**
Inicia el servidor local:
```bash
python manage.py runserver
```

Accede en tu navegador a: [http://127.0.0.1:8000](http://127.0.0.1:8000)

