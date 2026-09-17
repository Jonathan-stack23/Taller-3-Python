# 🤖 Taller 3 - Modelos de Machine Learning

**📦 Repositorio GitHub (clonar aquí):** https://github.com/Jonathan-stack23/Taller-3-Python.git
```bash
git clone https://github.com/Jonathan-stack23/Taller-3-Python.git
cd Taller-3-Python
```

**👨‍💻 Autor:** Jonathan Martinez  
**📅 Trimestre:** 3er trimestre · Python / Machine Learning  
**🌐 Despliegue sugerido:** ▲ Vercel (Vision Artificial), 🎈 Streamlit (Random Forest), Otros (Regresion Lineal)

---

## 📁 Estructura del repositorio

```
Taller-3-Python/
├── api/                            # ⚡ BACKEND VERCEL RAIZ (Vision Artificial - Flask Serverless)
│   └── index.py                    #    GET /, /health  ·  POST /api/detectar, /api/detect
├── public/                         # 🌐 FRONTEND VERCEL RAIZ (UI demo, drag&drop, metricas)
│   ├── index.html
│   ├── script.js
│   └── style.css
├── Modelos_ML/
│   ├── 👁️ Visionartificial/        # MODELO 1 · Notebook + FastAPI local
│   │   ├── index.ipynb             # Tutorial paso a paso Jupyter
│   │   ├── main.py                 # API FastAPI alternativa (local, no Vercel)
│   │   ├── faces.jpg               # Dataset imagen ejemplo
│   │   └── haarcascade_frontalface_default.xml
│   │
│   ├── 🖼️ py_img-main/            # MODELO 1b · CLON PERSONALIZADO py_img (Frontend + Flask Vercel)
│   │   ├── api/index.py            # Backend Flask Serverless (GET/, POST /api/detect)
│   │   ├── public/                 # Frontend Bootstrap: subir imagen + CAMARA WEB EN VIVO
│   │   ├── vercel.json             # Config despliegue Vercel independiente
│   │   └── haarcascade_frontalface_default.xml
│   │
│   ├── 🏠 RegresionLineal/         # MODELO 2 · Prediccion precio apartamentos
│   │   ├── backend/                # FastAPI · Dockerfile · model.joblig
│   │   │   ├── main.py             # POST /predict -> precio estimado
│   │   │   ├── train.py
│   │   │   ├── models/linear_model.joblib
│   │   │   └── requirements.txt
│   │   └── frontend/               # Django UI · Dockerfile
│   │       ├── manage.py
│   │       ├── predictor/views.py  # Formulario -> consume backend
│   │       └── requirements.txt
│   │
│   └── 🌳 RandomForest/            # MODELO 3 · Prediccion enfermedades
│       ├── 1.Crear_dataset.py
│       ├── 2.Entrenar_modelo.py
│       ├── 3.Predecir_enefermedad.py   # streamlit run 3.Predecir_enefermedad.py
│       ├── data/dataset_medico_ampliado.csv
│       └── models/modelo_random_forest_ampliado.pkl
├── Carga_datos/                    # Ejemplos carga CSV / Excel / API / WebScraping
├── requirements.txt                # Dependencias globales
├── vercel.json                     # ▲ Despliegue Vercel (raiz)
├── .gitignore
└── README.MD                       # ← Este documento (documentacion tecnica)
```

---

## 👁️ MODELO 1 — Vision Artificial · Detección de Rostros

### Descripción técnica
Detector de rostros en imágenes y video. Funciona con **OpenCV** y cuenta con **dos detectores automáticos** según la versión de OpenCV instalada.

| Item | Valor |
|---|---|
| **Problema** | Detección de objetos (rostros humanos) en imágenes/video |
| **Algoritmo / Modelo** | 1) Haar Cascade (OpenCV 4.x), 2) YuNet FaceDetectorYN DNN (OpenCV 5.x) |
| **Framework backend** | Flask (Serverless en Vercel) + FastAPI (alternativa local) |
| **Frontend** | UI estática (HTML/JS/CSS) + UI Bootstrap en `py_img-main/` |
| **Entrada** | Imagen BGR / frame de cámara |
| **Salida** | `[{x,y,ancho,alto}]` + imagen con rectángulos |
| **Dataset entrenamiento** | Integrado en OpenCV (Haar XML preentrenado / YuNet ONNX preentrenado) |
| **Métricas** | Conteo de rostros detectados · Coordenadas bounding-box |
| **Rendimiento** | ~30–60 ms/imagen en CPU · Cold start Vercel + descarga onnx ~10 s en el primer request |

---

#### Archivos clave

| Archivo | Función |
|---|---|
| [api/index.py](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/api/index.py) | Backend Flask Serverless Vercel (raíz) |
| [public/index.html](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/public/index.html) | UI drag&drop principal |
| [Modelos_ML/Visionartificial/index.ipynb](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/Modelos_ML/Visionartificial/index.ipynb) | Notebook Jupyter · tutorial |
| [Modelos_ML/py_img-main/api/index.py](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/Modelos_ML/py_img-main/api/index.py) | Clon py_img (con cámara en vivo) |

---

#### Endpoints — Backend raíz `/api/`

| Método | Path | Descripción | Body | Respuesta |
|---|---|---|---|---|
| `GET` | `/` | UI web demo | — | HTML |
| `GET` | `/health` | Estado servicio + versión OpenCV | — | JSON `{estado,opencv_version,clasificador_haar_cargado,yunet_cargado,rutas}` |
| `POST` | `/api/detectar` | Detectar rostros | `multipart/form-data` campo **`imagen`** (file) | JSON `{success,total_rostros,rostros:[{x,y,ancho,alto}],modelo_usado,image:"data:image/jpeg;base64,..."}` |
| `POST` | `/api/detect` | Alias (compatibilidad con py_img) | campo **`image`** (file) | Mismo formato + campo `faces_detected` |

#### Ejemplo curl
```bash
curl -X POST \
  -F "imagen=@Modelos_ML/Visionartificial/faces.jpg" \
  https://TUSIGLAS.vercel.app/api/detectar
```

#### Probar localmente
```bash
pip install -r requirements.txt
python api/index.py          # Flask en http://localhost:5000
# OR  (FastAPI local)
uvicorn Modelos_ML.Visionartificial.main:app --reload   # http://localhost:8000/docs
```

#### ▲ Desplegar en Vercel (proyecto raíz)
1. Vercel → Add New → Project → importa `Jonathan-stack23/Taller-3-Python`
2. Framework preset: **Other** · Root dir: **(vacío)**
3. Deploy · URL final: `https://TUSIGLAS.vercel.app`

---

## 🏠 MODELO 2 — Regresión Lineal · Predicción Precio Apartamentos (Medellín)

### Descripción técnica
Modelo supervisado de **regresión lineal múltiple** que estima el valor de un apartamento a partir de sus características (área, habitaciones, baños, estrato, ubicación, etc.).

| Item | Valor |
|---|---|
| **Problema** | Regresión (predicción valor numérico continuo) |
| **Algoritmo / Modelo** | Linear Regression (Scikit-learn) |
| **Framework backend** | FastAPI · Dockerfile |
| **Framework frontend** | Django (formulario UI) · Dockerfile |
| **Hipótesis** | El precio de un inmueble se explica linealmente por combinación de sus atributos estructurales y geográficos |
| **Variables de entrada X** | `area_m2`, `habitaciones`, `banos`, `estrato`, `barrio`, `parqueaderos`, `piso`, `edad_construccion`… |
| **Variable objetivo Y** | `precio_apartamento` (COP $) |
| **Serialización modelo** | `joblib` → RegresionLineal/backend/models/linear_model.joblib |
| **Métricas típicas** | R² Score, MAE (Error absoluto medio), RMSE |
| **Hiperparámetros** | `fit_intercept=True`, `copy_X=True`, `n_jobs=None` (scikit-learn defaults) |

---

#### Arquitectura (2 capas, dockerizadas)

```
    [Usuario]
        │
        ▼
 ┌─────────────────┐          HTTP JSON POST /predict          ┌────────────────────┐
 │  Django UI      │ ─────────────────────────────────────────▶ │  FastAPI Backend   │
 │  (Formulario)   │ ◀───────────────────────────────────────── │  Linear Regression │
 └─────────────────┘          {precio_estimado, r2, mae}        └────────────────────┘
```

#### Archivos clave

| Archivo | Función |
|---|---|
| [RegresionLineal/backend/main.py](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/Modelos_ML/RegresionLineal/backend/main.py) | FastAPI endpoints |
| [RegresionLineal/backend/train.py](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/Modelos_ML/RegresionLineal/backend/train.py) | Entrenamiento → guarda joblib |
| [RegresionLineal/backend/models/linear_model.joblib](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/Modelos_ML/RegresionLineal/backend/models/linear_model.joblib) | Modelo entrenado |
| [RegresionLineal/frontend/predictor/views.py](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/Modelos_ML/RegresionLineal/frontend/predictor/views.py) | Vista Django formulario |

#### Endpoints — Backend Regresión Lineal

| Método | Path | Body | Respuesta |
|---|---|---|---|
| `GET` | `/` | — | Swagger UI + docs |
| `POST` | `/predict` | JSON `{area_m2:90, habitaciones:3, banos:2, estrato:4, ...}` | `{precio_estimado:int, r2:float, mae:float, metodo:"LinearRegression"}` |

#### Probar localmente (Terminal 1 + Terminal 2)
```bash
# Terminal 1 · Backend
cd Modelos_ML/RegresionLineal/backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2 · Frontend Django
cd Modelos_ML/RegresionLineal/frontend
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8001
```

---

## 🌳 MODELO 3 — Random Forest · Predicción Enfermedades

### Descripción técnica
Clasificador multiclase basado en **Random Forest Classifier** (ensamble de árboles de decisión) que recibe síntomas/parámetros médicos y predice una enfermedad.

| Item | Valor |
|---|---|
| **Problema** | Clasificación multiclase (enfermedad X / Y / Z) |
| **Algoritmo / Modelo** | RandomForestClassifier · 100 árboles (Scikit-learn) |
| **Framework UI** | 🎈 Streamlit (`streamlit run 3.Predecir_enefermedad.py`) |
| **Hipótesis** | Combinaciones no-lineales de síntomas predicen enfermedad → RandomForest captura interacciones mejor que árbol individual |
| **Dataset** | `dataset_medico_ampliado.csv` — filas = pacientes; columnas = síntomas + `diagnostico` (etiqueta) |
| **Preprocesamiento** | One-Hot / LabelEncoding variables categóricas; imputación NaN; Train/Test split 80/20 |
| **Serialización modelo** | `joblib` → models/modelo_random_forest_ampliado.pkl |
| **Métricas típicas** | Accuracy · Precision · Recall · F1-score · Matriz de confusión · Feature importance |
| **Hiperparámetros** | `n_estimators=100`, `criterion="gini"`, `max_depth=None`, `min_samples_split=2`, `class_weight="balanced"` |

---

#### Pipeline ML

```
1.Crear_dataset.py  ──►  dataset_medico_ampliado.csv
                             │
                             ▼
                2.Entrenar_modelo.py
                · train_test_split
                · GridSearchCV (opcional)
                · RandomForest.fit(X_train, y_train)
                · Evaluar en X_test (accuracy, f1)
                · joblib.dump(model, .pkl)
                             │
                             ▼
            3.Predecir_enefermedad.py  (🎈 Streamlit)
            · Formulario UI -> capturea sintomas
            · joblib.load(.pkl)
            · model.predict(X_usuario) → diagnostico
            · Muestra probabilidades por clase + feature_importance
```

#### Archivos clave

| Archivo | Función |
|---|---|
| [RandomForest/1.Crear_dataset.py](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/Modelos_ML/RandomForest/1.Crear_dataset.py) | Genera dataset sintético médico ampliado |
| [RandomForest/2.Entrenar_modelo.py](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/Modelos_ML/RandomForest/2.Entrenar_modelo.py) | Entrena RandomForest + guarda .pkl |
| [RandomForest/3.Predecir_enefermedad.py](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/Modelos_ML/RandomForest/3.Predecir_enefermedad.py) | Streamlit UI producción |
| [RandomForest/data/dataset_medico_ampliado.csv](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/Modelos_ML/RandomForest/data/dataset_medico_ampliado.csv) | Dataset |
| [RandomForest/models/modelo_random_forest_ampliado.pkl](file:///C:/Users/Acer/Documents/Jonathan%20SENA/Python/3%20trimestre/Taller3/Machine-learning/Modelos_ML/RandomForest/models/modelo_random_forest_ampliado.pkl) | Modelo entrenado |

#### Probar localmente
```bash
cd Modelos_ML/RandomForest
pip install -r ../../requirements.txt       # Streamlit, pandas, sklearn…
python 1.Crear_dataset.py                   # Generar dataset (opcional)
python 2.Entrenar_modelo.py                 # Reentrenar modelo (opcional)
streamlit run 3.Predecir_enefermedad.py     # Abre UI en el navegador
```

> ⚠️ ADVERTENCIA: Herramienta educativa/demostrativa. **NO USAR COMO DIAGNÓSTICO MÉDICO REAL.**

---

## 🖼️ MODELO 1b — Clon `py_img-main` PERSONALIZADO (Despliegue Vercel separado)

Clon del repositorio py_img suministrado (Carlos Castro), adaptado y **personalizado por Jonathan Martinez**. Cuenta con:
- ✅ Frontend Bootstrap (2 modos: subir imagen / **cámara web en vivo** cada 600ms)
- ✅ Backend Flask Serverless + OpenCV Haar Cascade
- ✅ `vercel.json` propio para desplegar como proyecto independiente en Vercel

#### ▲ Desplegar py_img-main solo en Vercel (RUTA ESPECIAL ROOT)
1. Vercel → Add New → Project → importar `Jonathan-stack23/Taller-3-Python`
2. En **Root Directory** escribir: **`Modelos_ML/py_img-main`**
3. Framework: Other → Deploy. Done.

Frontend: `/`, Backend endpoint: `POST /api/detect` (campo `image`).

---

## 📋 Resumen comparativo 3 Modelos

| # | Modelo | Tarea ML | Algoritmo | UI | Despliegue sugerido | Endpoint principal |
|---|---|---|---|---|---|---|
| 1 | 👁️ Detección Rostros | Object Detection (Computer Vision) | Haar Cascade + YuNet DNN | 2 UIs (drag & drop + Bootstrap cámara) | ▲ Vercel (Flask Serverless) | `POST /api/detectar` |
| 2 | 🏠 Precio Apartamentos | **Regresión** lineal múltiple | Scikit LinearRegression | Django Formulario + FastAPI JSON | Railway / Fly.io (2 dockers) | `POST /predict` |
| 3 | 🩺 Predicción Enfermedades | **Clasificación** multiclase | RandomForest Classifier (100 trees) | 🎈 Streamlit Community Cloud | UI Form → predict() interna |

---

## 🔗 Links importantes
- **GitHub repo**: https://github.com/Jonathan-stack23/Taller-3-Python.git
- Clon Vercel (raiz): **`vercel.json`** carpeta raíz (Vision Artificial UI simple)
- Clon Vercel (py_img): **`Modelos_ML/py_img-main/vercel.json`** (subir imagen + webcam en vivo)
- Documentación API Vision Artificial: abre `/health` de tu despliegue
- Dataset ejemplo: `Modelos_ML/Visionartificial/faces.jpg`, `RandomForest/data/dataset_medico_ampliado.csv`

---

## 👨‍💻 Autor

**Jonathan Martinez**  
**Taller 3 · Python Machine Learning (3er trimestre)**

> Estructura modular · 3 modelos desplegables · Documentación técnica · Compatibilidad OpenCV 4 / 5
