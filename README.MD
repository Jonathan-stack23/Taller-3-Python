# 🤖 Taller 3 - Modelos de Machine Learning

Repositorio oficial: **https://github.com/Jonathan-stack23/Taller-3-Python.git**

Este repositorio reúne diferentes proyectos y modelos desarrollados como parte del aprendizaje y aplicación de técnicas de **Machine Learning, Inteligencia Artificial y Visión Artificial**.

Cada proyecto aborda un problema diferente y cuenta con un despliegue web para poder probar su funcionamiento.

---

## 📁 Estructura del proyecto

```
Machine-learning/
├── Carga_datos/                 # Ejemplos de carga de datos (CSV, Excel, API, Web Scraping)
├── Modelos_ML/
│   ├── RandomForest/            # Prediccion de enfermedades - Streamlit
│   ├── RegresionLineal/         # Prediccion precio apartamentos (FastAPI + Django)
│   ├── Visionartificial/        # 👁️ Deteccion de rostros (OpenCV + FastAPI)
│   │   ├── main.py              # ⚡ API web FastAPI (despliegue Render)
│   │   ├── index.ipynb          # Notebook Jupyter con el ejercicio
│   │   ├── faces.jpg            # Imagen de ejemplo
│   │   └── haarcascade_frontalface_default.xml
│   └── py_img-main/             # Proyecto alterno vision artificial
├── requirements.txt             # Dependencias globales
├── Procfile                     # Comando de arranque Render
├── build.sh                     # Build script Render (instala libs OpenCV)
├── render.yaml                  # Blueprint para despliegue 1-click
├── .gitignore
└── README.MD
```

---

## 📊 1. Regresión Lineal — Predicción del precio de apartamentos

### 🏠 Descripción

Este proyecto utiliza un modelo de **Regresión Lineal** para realizar una estimación aproximada del valor de un apartamento en la ciudad de **Medellín, Colombia**.

El modelo recibe información relacionada con el inmueble y, a partir de los datos proporcionados, calcula un **precio estimado**.

> ⚠️ El resultado es únicamente una estimación generada por el modelo y no representa necesariamente el valor comercial real del inmueble.

### 🧠 Modelo utilizado

**Regresión Lineal (Linear Regression)**

La regresión lineal busca establecer una relación entre diferentes variables de entrada y una variable de salida numérica. En este caso, se utiliza para estimar el precio de un apartamento.

### 🌐 Despliegue

<s>🚀 Abrir aplicación — Frontend</s><br>
<s>🔧 Abrir API — Backend</s>

---

## 👤 2. Visión Artificial — Detección de rostros

### 📷 Descripción

Este proyecto utiliza técnicas de **Visión Artificial (Computer Vision)** para detectar rostros en imágenes mediante **OpenCV**. El repositorio incluye:

- **Notebook Jupyter** (`index.ipynb`) — tutorial paso a paso
- **API Web FastAPI** (`main.py`) — **lista para Render**:
  - 🌐 Página web demo con interfaz gráfica (arrastra y suelta imagenes)
  - 🔗 Endpoint `POST /detectar` (JSON, sube imagen y recibe coordenadas + imagen procesada)
  - 🔗 Endpoint `GET /health` (monitoreo)
- **Compatibilidad OpenCV 4.x (Haar Cascade) y OpenCV 5.x (YuNet FaceDetectorYN)**

### 🧠 Tecnología utilizada

* Python
* OpenCV
* FastAPI + Uvicorn
* Haar Cascade / YuNet
* Visión Artificial
* Detección de rostros

### 🌐 Despliegue en Render

Instrucciones completas en la **sección de despliegue Render** abajo.

<s>👤 Abrir aplicación — Detección de rostros</s>

---

## 🌳 3. Random Forest — Predicción de enfermedades

### 🩺 Descripción

Este proyecto utiliza el algoritmo **Random Forest (Bosque Aleatorio)** para realizar predicciones relacionadas con enfermedades a partir de los datos ingresados por el usuario.

Random Forest está compuesto por múltiples árboles de decisión. Cada árbol realiza una predicción y posteriormente se combinan las predicciones de los diferentes árboles para obtener el resultado final. En problemas de clasificación, este proceso puede entenderse como una **votación entre los árboles**.

### 🧠 Modelo utilizado

**Random Forest Classifier**

El algoritmo permite trabajar con múltiples variables de entrada y utilizar diferentes árboles de decisión para realizar una clasificación.

### 🌐 Despliegue

<s>🌳 Abrir aplicación — Random Forest</s>

> ⚠️ Las predicciones realizadas por este proyecto tienen fines educativos y demostrativos. No deben utilizarse como diagnóstico médico.

---

## 🚀 Despliegue en Render (Vision Artificial - FastAPI)

El servicio web de **detección de rostros** ya está configurado para desplegarse en Render con cero cambios manuales.

### 📋 Pre-requisitos

1. Tener el repositorio subido a GitHub
2. Cuenta en https://render.com (gratis es suficiente para pruebas)

### 🛠️ Método 1 — Blueprint con render.yaml (recomendado)

1. Entra a Render → **Blueprints** → **New Blueprint Instance**
2. Conecta tu repositorio `Jonathan-stack23/Taller-3-Python`
3. Selecciona `render.yaml` y sigue los pasos

Render creará automáticamente:
- **Runtime**: Python
- **Build command**: `./build.sh` (instala libgl + libopencv)
- **Start command**: `uvicorn Modelos_ML.Visionartificial.main:app --host 0.0.0.0 --port $PORT`
- **Health check**: `/health`
- **Python version**: 3.11.8
- **Region**: Oregon
- **Plan**: Starter

### 🛠️ Método 2 — Web Service manual

1. New → **Web Service**
2. Conecta el repositorio
3. Configuración:
   | Campo | Valor |
   |---|---|
   | Runtime | Python 3 |
   | Build Command | `./build.sh` |
   | Start Command | `uvicorn Modelos_ML.Visionartificial.main:app --host 0.0.0.0 --port $PORT` |
   | Region | Oregon |
   | Plan | Starter (Free funciona para pruebas) |
4. En **Environment variables** (opcional): `PYTHON_VERSION=3.11.8`
5. Click en **Create Web Service** y espera 2-5 minutos

### ✅ Verificar despliegue

Cuando termine el build, visita:

```
https://TU-APP.onrender.com/              ← UI web demo
https://TU-APP.onrender.com/health        ← JSON con estado del detector
https://TU-APP.onrender.com/docs          ← Documentación Swagger /docs
```

### 🧪 Probar el endpoint `/detectar` con curl

```bash
curl -X POST -F "imagen=@faces.jpg" \
  https://TU-APP.onrender.com/detectar
```

Respuesta JSON de ejemplo:

```json
{
  "total_rostros": 6,
  "rostros": [
    {"x": 80,  "y": 27,  "ancho": 76, "alto": 106},
    {"x": 537, "y": 29,  "ancho": 69, "alto": 94 }
  ],
  "modelo_usado": "YuNet FaceDetectorYN (OpenCV 5.x)",
  "imagen_procesada": "iVBORw0KGgoAAAA...PNG en base64"
}
```

---

## 📚 Tecnologías utilizadas

Los proyectos utilizan diferentes tecnologías relacionadas con el desarrollo de aplicaciones y Machine Learning:

* 🐍 Python
* 🤖 Machine Learning
* 📊 Scikit-learn
* 📷 OpenCV (4.x y 5.x compatibles)
* 🌳 Random Forest
* 📈 Regresión Lineal
* 👁️ Visión Artificial (Haar Cascade / YuNet)
* ⚡ FastAPI + Uvicorn
* 🎈 Streamlit
* 🎨 Django
* 🚀 Render
* ▲ Vercel

---

## 📋 Resumen de proyectos

| # | Proyecto                      | Tecnología / Modelo        | Problema                                       |
| - | ----------------------------- | -------------------------- | ---------------------------------------------- |
| 1 | 🏠 Predicción de apartamentos | Regresión Lineal           | Estimar el valor de un apartamento en Medellín |
| 2 | 👤 Detección de rostros       | Visión Artificial + OpenCV + FastAPI | Detectar rostros en imágenes          |
| 3 | 🩺 Predicción de enfermedades | Random Forest + Streamlit  | Clasificar enfermedades a partir de datos      |

---

## 🎯 Objetivo

El objetivo de estos proyectos es aplicar diferentes técnicas de **Inteligencia Artificial y Machine Learning** a problemas prácticos, además de aprender el proceso completo de desarrollo y despliegue de modelos.

Los proyectos permiten explorar diferentes enfoques, desde modelos de regresión para predecir valores numéricos hasta algoritmos de clasificación y técnicas de visión artificial.

---

## 👨‍💻 Autor

**Jonathan Martinez**

Proyectos desarrollados como parte del proceso de aprendizaje en **Programación, Machine Learning e Inteligencia Artificial** — Taller 3 Python, 3er trimestre.
