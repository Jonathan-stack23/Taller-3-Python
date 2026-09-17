# 🧠 VisionML · py_img-main (CLON PERSONALIZADO)
> Taller 3 de Machine Learning · SENA · 3er trimestre Python  
> **Autor:** Jonathan Martinez · https://github.com/Jonathan-stack23

Clon personalizado del repositorio `py_img` (Carlos Castro). Adaptado con identidad visual propia, métricas avanzadas, compatibilidad OpenCV 4/5 y link directo al repo del proyecto.

✅ **Desplegable directamente en ▲ Vercel** (tiene su propio `vercel.json` independiente).

---

## 📌 1. Qué incluye este clon

| Capa | Stack | Personalización |
|---|---|---|
| **Frontend** | HTML5 + CSS3 + Bootstrap 5 + JS vanilla | Marca `VisionML`, paleta azul/púrpura Vercel, estado en vivo, badges, footer autor, link GitHub |
| **Backend** | Python 3 + Flask 3 (Serverless) | Endpoints `/`, `/health`, `/api/detect`, `/api/detectar` · Haar/YuNet dual · métricas `modelo_usado` |
| **Visión artificial** | OpenCV (`opencv-python-headless`) | Haar Cascade XML para OpenCV 4.x · YuNet DNN ONNX (descarga automática) para OpenCV 5.x |
| **Despliegue** | ▲ Vercel | `@vercel/python` con `maxLambdaSize=50mb` para albergar opencv |

---

## 📁 Estructura interna

```
py_img-main/
├── api/
│   └── index.py                          # Flask Serverless (GET/, /health, POST /api/detect)
├── public/
│   ├── index.html                        # UI VisionML personalizada
│   ├── script.js                         # Lógica drag&drop + webcam cada 600ms + métricas tiempo/modelo
│   └── style.css                         # Tema azul/púrpura (Inter + Space Grotesk + JetBrains Mono)
├── haarcascade_frontalface_default.xml   # Modelo Haar Cascade preentrenado
├── requirements.txt                      # Flask · opencv-python-headless · numpy<2.2
├── vercel.json                           # Config despliegue Vercel (50MB lambda)
└── README.md                             # ← este documento
```

---

## 🚀 2. Cómo desplegar en Vercel (3 clicks)

### Opción A) Proyecto Vercel independiente (recomendado)
1. Abre **https://vercel.com** → **Add New…** → **Project**
2. Importa el repo **`Jonathan-stack23/Taller-3-Python`**
3. Dentro de la pantalla **Configure Project**:
   - **Root Directory**: escribe **`Modelos_ML/py_img-main`** (IMPORTANTE)
   - **Framework Preset**: `Other`
   - Deja todo lo demás por defecto → **Deploy**
4. Espera 2–4 minutos (opencv se instala en cold-build)

Cuando termine, tu URL final será algo como `https://visionml-jonathan-tualias.vercel.app`.

### Opción B) Correr localmente

```bash
cd Modelos_ML/py_img-main
pip install -r requirements.txt
python api/index.py
# Abre http://localhost:5000
```

---

## 🔌 3. Documentación del API

| Método | Path | Descripción | Cuerpo |
|---|---|---|---|
| `GET` | `/` | UI VisionML | — |
| `GET` | `/health` | Healthcheck (versión OpenCV, modelo activo, rutas disponibles) | — |
| `POST` | `/api/detect` | Detectar rostros (nombre original py_img) | `multipart/form-data` campo **`image`** (JPG/PNG) |
| `POST` | `/api/detectar` | Alias en español | `multipart/form-data` campo **`imagen`** o **`image`** |

### Respuesta JSON ejemplo:
```json
{
  "success": true,
  "total_rostros": 6,
  "faces_detected": 6,
  "rostros": [{"x":120,"y":80,"ancho":110,"alto":110}, ...],
  "modelo_usado": "Haar Cascade (OpenCV 4.9.0)",
  "autor": "Jonathan Martinez",
  "proyecto": "Taller 3 Machine Learning",
  "repositorio": "https://github.com/Jonathan-stack23/Taller-3-Python.git",
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ…",
  "imagen_procesada": "/9j/4AAQSkZJRgABAQ…"
}
```

### Ejemplo curl:
```bash
cd Taller-3-Python
curl -X POST \
  -F "image=@Modelos_ML/Visionartificial/faces.jpg" \
  https://TU-URL-PY-IMG.vercel.app/api/detect
```

---

## 🧪 4. Compatibilidad OpenCV 4 / 5

| Versión OpenCV | Detector activo |
|---|---|
| 4.x.x | **Haar Cascade** (usa `haarcascade_frontalface_default.xml` de la carpeta) |
| 5.x.x | **YuNet DNN** (descarga automática de `face_detection_yunet_2023mar.onnx` al primer request en `/api/detect`) |

El campo `modelo_usado` en la respuesta JSON te indica cuál se usó en cada petición.

---

## 🔗 5. Repositorio oficial del proyecto

```
https://github.com/Jonathan-stack23/Taller-3-Python.git
```
```bash
git clone https://github.com/Jonathan-stack23/Taller-3-Python.git
```

---

## 📌 6. Cómo se compara con el py_img original

| Aspecto | py_img original (Carlos Castro) | **ESTE clon (Jonathan Martinez)** |
|---|---|---|
| Autor footer | Carlos Andrés Castro Jaramillo | **Jonathan Martinez · Taller 3 ML** |
| Marca título | Rostros · Análisis de imagen | **VisionML · Detección de Rostros \| Taller 3** |
| Paleta CSS | Arcilla / Olivo (DM Sans / Playfair) | **Azul + Púrpura Vercel (Inter + Space Grotesk + JetBrains Mono)** |
| Métricas front | Solo contador numérico | **Contador + tiempo en ms + nombre del modelo + estado en vivo** |
| Endpoint /health | ❌ No existe | ✅ Incluye (estado, versión cv2, rutas, repo link) |
| Respuesta JSON | `success, faces_detected, image` | + `total_rostros, rostros[], modelo_usado, autor, repositorio, imagen_procesada` |
| OpenCV 5 | ❌ Fallaría (solo Haar) | ✅ **Dual: Haar si puede, YuNet ONNX si OpenCV 5** |
| Link GitHub repo | Sin link directo | ✅ **Botón prominente + HTML meta + footer + /health + JSON** |
| Lambda size Vercel | sin límite explícito | ✅ **50 MB** para evitar `Maximum Lambda size exceeded` |

---

✍️ **Jonathan Martinez** · Python · Machine Learning · SENA
