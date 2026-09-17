# 🤖 Taller 3 - Modelos de Machine Learning

Repositorio oficial: **https://github.com/Jonathan-stack23/Taller-3-Python.git**

Este repositorio reúne diferentes proyectos y modelos desarrollados como parte del aprendizaje y aplicación de técnicas de **Machine Learning, Inteligencia Artificial y Visión Artificial**.

Cada proyecto aborda un problema diferente y cuenta con un despliegue web para poder probar su funcionamiento.

---

## 📁 Estructura del proyecto

```
Machine-learning/
├── api/
│   └── index.py                 # ⚡ Serverless Function Vercel (Flask)
│                                   POST /api/detectar, GET /health
├── public/                      # 🌐 UI web estatica para Vercel
│   ├── index.html
│   ├── script.js
│   └── style.css
├── Carga_datos/                 # Ejemplos de carga de datos
├── Modelos_ML/
│   ├── RandomForest/            # Prediccion enfermedades · Streamlit
│   ├── RegresionLineal/         # Prediccion precio aptos · FastAPI+Django
│   ├── Visionartificial/        # 👁️ Deteccion rostros OpenCV
│   │   ├── main.py              # FastAPI (alternativa local)
│   │   ├── index.ipynb          # Notebook Jupyter tutorial paso a paso
│   │   ├── faces.jpg            # Imagen de ejemplo
│   │   └── haarcascade_frontalface_default.xml
│   └── py_img-main/             # Proyecto alterno vision artificial
├── requirements.txt             # Dependencias (incluye Flask + opencv-headless)
├── vercel.json                  # Configuracion despliegue ▲ Vercel
├── .gitignore
└── README.MD
```

---

## 👤 1. Visión Artificial — Detección de rostros (Desplegable en Vercel ✅)

### 📷 Descripción

Este proyecto utiliza técnicas de **Visión Artificial (Computer Vision)** para detectar rostros en imágenes mediante **OpenCV**. El repositorio cuenta con **tres formas** de ejecutarlo:

1. **Notebook Jupyter** (`Modelos_ML/Visionartificial/index.ipynb`) — tutorial paso a paso
2. **API local FastAPI** (`Modelos_ML/Visionartificial/main.py`) — servidor local `uvicorn`
3. **▲ Despliegue en Vercel** (preconfigurado 100%):
   - 🌐 UI web demo (arrastra y suelta imágenes) — carpeta `public/`
   - 🔗 `GET /health` — estado del servicio
   - 🔗 `POST /api/detectar` — envía imagen multipart/form-data, recibe JSON con coordenadas e imagen procesada
   - 🔗 `POST /api/detect` — alias compatible con otros proyectos
- **Compatibilidad OpenCV 4.x (Haar Cascade XML) y OpenCV 5.x (YuNet FaceDetectorYN)**

### 🧠 Tecnología utilizada

* Python
* Flask (Serverless Vercel)
* OpenCV (opencv-python-headless)
* Haar Cascade / YuNet
* Visión Artificial · Detección de rostros

### ▲ Despliegue en Vercel

Instrucciones completas en la **sección de despliegue Vercel** abajo.

---

## 📊 2. Regresión Lineal — Predicción del precio de apartamentos

### 🏠 Descripción

Este proyecto utiliza un modelo de **Regresión Lineal** para realizar una estimación aproximada del valor de un apartamento en la ciudad de **Medellín, Colombia**.

> ⚠️ El resultado es únicamente una estimación generada por el modelo.

### 🧠 Modelo utilizado

**Regresión Lineal (Linear Regression)**

---

## 🌳 3. Random Forest — Predicción de enfermedades

### 🩺 Descripción

Este proyecto utiliza el algoritmo **Random Forest (Bosque Aleatorio)** para realizar predicciones relacionadas con enfermedades a partir de los datos ingresados por el usuario.

### 🧠 Modelo utilizado

**Random Forest Classifier**

> ⚠️ Las predicciones tienen fines educativos. No deben utilizarse como diagnóstico médico.

---

## ▲ Despliegue en Vercel (Visión Artificial - Flask Serverless)

El proyecto ya está **100% listo** para desplegar en Vercel con cero cambios manuales.

### 📋 Pre-requisitos

1. Repositorio subido a **GitHub** (https://github.com/Jonathan-stack23/Taller-3-Python)
2. Cuenta gratuita en **https://vercel.com** (Sign up con GitHub es lo más rápido)

### 🛠️ Método 1 — Importar proyecto desde GitHub (Recomendado)

1. Entra a **Vercel** → Click en **Add New…** → **Project**
2. En el buscador importa el repo: **`Jonathan-stack23/Taller-3-Python`** → **Import**
3. En la pantalla **Configure Project**:
   - **Framework Preset**: Déjalo en **Other** (no es necesario elegir uno)
   - **Root Directory**: **dejalo vacío** (la raíz del proyecto)
   - **Build Command**: *(déjalo vacío, no se necesita)*
   - **Install Command**: *(automático — Vercel lee `requirements.txt`)*
   - **Output Directory**: *(déjalo vacío, Vercel ya sirve `public/`)*
   - **Node.js Version**: *(no es necesario, usa la de por sí predeterminada)*
4. Click en **Deploy**
5. Espera **2 a 4 minutos** mientras Vercel:
   - Instala Python runtime (`@vercel/python`)
   - Instala dependencias (opencv-python-headless ~50 MB)
   - Construye el paquete serverless de `api/index.py`
   - Publica los estáticos de `public/`

### ✅ Verificar que el despliegue funcionó

Cuando termine recibirás una URL como: **`https://TUSIGLAS.vercel.app`**

Ábrela y prueba:

```
/                         ← UI web demo — arrastra imagen y detecta rostros
/health                   ← JSON: estado, versión OpenCV, detectores cargados
/docs                     ← (no aplica — endpoints documentados abajo)
```

### 🧪 Probar API por consola (curl)

```bash
curl -X POST \
  -F "imagen=@Modelos_ML/Visionartificial/faces.jpg" \
  https://TUSIGLAS.vercel.app/api/detectar
```

Respuesta JSON de ejemplo:

```json
{
  "success": true,
  "total_rostros": 6,
  "faces_detected": 6,
  "modelo_usado": "YuNet FaceDetectorYN (OpenCV 5.x)",
  "rostros": [
    {"x": 80,  "y": 27,  "ancho": 76, "alto": 106},
    {"x": 537, "y": 29,  "ancho": 69, "alto": 94 }
  ],
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "imagen_procesada": "/9j/4AAQSkZJRg..."
}
```

### 🧪 Probar localmente antes de subir

```bash
cd Machine-learning
pip install -r requirements.txt
python api/index.py   # Flask en http://localhost:5000
# Abre http://localhost:5000 — misma UI que en Vercel
```

### ⚠️ Solución de problemas comunes en Vercel

| Problema | Solución |
|---|---|
| `Error: 50mb Lambda size exceeded` | Cambiado en `vercel.json` → `"maxLambdaSize": "50mb"` |
| OpenCV no carga / `libGL.so` | Usamos `opencv-python-headless` (sin dependencias gráficas) |
| `cv2.CascadeClassifier` no existe | Detecta versión automáticamente y se cambia a YuNet (descarga onnx en primer request) |
| Primer request lento (~10 seg) | Normal — es el cold start + descarga del modelo YuNet (~7 MB) |

---

## 📚 Tecnologías utilizadas

* 🐍 Python
* 🤖 Machine Learning · Scikit-learn
* 📷 OpenCV 4.x y 5.x compatibles (opencv-python-headless)
* 🌳 Random Forest · 📈 Regresión Lineal · 👁️ Visión Artificial
* ⚡ Flask Serverless Functions (▲ Vercel)
* 🎈 Streamlit · 🎨 Django · ▲ Vercel

---

## 📋 Resumen de proyectos

| # | Proyecto                      | Tecnología / Modelo               | Problema                                        |
| - | ----------------------------- | ---------------------------------- | ------------------------------------------------ |
| 1 | 🏠 Predicción de apartamentos | Regresión Lineal                   | Estimar el valor de un apartamento en Medellín   |
| 2 | 👤 Detección de rostros       | OpenCV + Flask Serverless (Vercel) | Detectar rostros en imágenes                    |
| 3 | 🩺 Predicción de enfermedades | Random Forest + Streamlit          | Clasificar enfermedades a partir de datos        |

---

## 🎯 Objetivo

Aplicar diferentes técnicas de **Inteligencia Artificial y Machine Learning** a problemas prácticos, además de aprender el proceso completo de desarrollo y despliegue de modelos (notebooks → APIs → plataformas como Vercel).

---

## 👨‍💻 Autor

**Jonathan Martinez**

Desarrollado como parte del aprendizaje en **Programación, Machine Learning e Inteligencia Artificial** — Taller 3 Python, 3er trimestre.
