import os
import io
import base64
import urllib.request
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
MODELO_URL = (
    "https://github.com/opencv/opencv_zoo/raw/main/models/"
    "face_detection_yunet/face_detection_yunet_2023mar.onnx"
)
RUTA_XML = BASE_DIR / "haarcascade_frontalface_default.xml"
RUTA_YUNET = BASE_DIR / "face_detection_yunet.onnx"

app = FastAPI(
    title="Vision Artificial - Deteccion de Rostros",
    description="API de deteccion de rostros compatible con OpenCV 4.x (Haar Cascade) y OpenCV 5.x (YuNet).",
    version="1.0.0",
)

templates_dir = BASE_DIR / "templates"
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))

_clasificador = None
_detector_yunet = None


def _descargar_modelo_si_falta() -> None:
    if RUTA_YUNET.exists():
        return
    try:
        urllib.request.urlretrieve(MODELO_URL, str(RUTA_YUNET))
    except Exception as exc:
        raise RuntimeError(
            "No se pudo descargar el modelo YuNet. "
            "Coloque face_detection_yunet.onnx en la carpeta Visionartificial."
        ) from exc


def _cargar_detector():
    global _clasificador, _detector_yunet
    if _clasificador is not None or _detector_yunet is not None:
        return

    if hasattr(cv2, "CascadeClassifier") and RUTA_XML.exists():
        cls = cv2.CascadeClassifier(str(RUTA_XML))
        if not cls.empty():
            _clasificador = cls
            return

    _descargar_modelo_si_falta()
    _detector_yunet = True


def _detectar_rostros(imagen_bgr: np.ndarray):
    _cargar_detector()
    global _clasificador, _detector_yunet

    rostros = []
    altura, ancho = imagen_bgr.shape[:2]

    if _clasificador is not None:
        gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
        resultados = _clasificador.detectMultiScale(
            gris, scaleFactor=1.1, minNeighbors=8, minSize=(40, 40)
        )
        for r in resultados:
            rostros.append([int(v) for v in r])
        return rostros, "Haar Cascade (OpenCV 4.x)"

    if _detector_yunet is None or _detector_yunet is True:
        _detector_yunet = cv2.FaceDetectorYN_create(
            str(RUTA_YUNET),
            "",
            (ancho, altura),
            0.6,
            0.3,
            5000,
        )
    else:
        _detector_yunet.setInputSize((ancho, altura))
    _, resultados = _detector_yunet.detect(imagen_bgr)
    if resultados is not None:
        for det in resultados:
            x, y, w, h = int(det[0]), int(det[1]), int(det[2]), int(det[3])
            rostros.append([x, y, w, h])
    return rostros, "YuNet FaceDetectorYN (OpenCV 5.x)"


def _bytes_a_imagen(data: bytes) -> np.ndarray:
    arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="No se pudo decodificar la imagen.")
    return img


def _imagen_a_png_base64(img_bgr: np.ndarray) -> str:
    ok, buffer = cv2.imencode(".png", img_bgr)
    if not ok:
        raise HTTPException(status_code=500, detail="No se pudo codificar la imagen de salida.")
    return base64.b64encode(buffer.tobytes()).decode("ascii")


INDEX_HTML = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Deteccion de Rostros - Vision Artificial</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 2rem 1rem;
      color: #1f2937;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: #ffffff;
      border-radius: 16px;
      box-shadow: 0 20px 60px rgba(0,0,0,.2);
      overflow: hidden;
    }
    header {
      padding: 2rem;
      background: linear-gradient(90deg, #1f2937, #4c1d95);
      color: white;
    }
    header h1 { margin: 0 0 .5rem; font-size: 1.8rem; }
    header p  { margin: 0; opacity: .9; }
    .content { padding: 2rem; }
    .drop {
      border: 2px dashed #a78bfa;
      border-radius: 12px;
      padding: 2.5rem 1rem;
      text-align: center;
      cursor: pointer;
      background: #f5f3ff;
      transition: .2s;
    }
    .drop:hover { background: #ede9fe; border-color: #7c3aed; }
    .drop input { display: none; }
    button {
      background: #7c3aed; color: white; border: 0; padding: .8rem 1.6rem;
      border-radius: 8px; cursor: pointer; font-size: 1rem; font-weight: 600;
      margin-top: 1rem; transition: .2s;
    }
    button:hover { background: #6d28d9; }
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      margin-top: 2rem;
    }
    @media (max-width: 700px) { .grid { grid-template-columns: 1fr; } }
    .card {
      background: #f9fafb;
      border-radius: 12px;
      padding: 1rem;
      text-align: center;
    }
    .card h3 { margin: 0 0 .75rem; font-size: 1rem; color: #4b5563; }
    .card img { max-width: 100%; border-radius: 8px; border: 1px solid #e5e7eb; }
    .info {
      background: #ecfdf5; color: #065f46; border-radius: 8px;
      padding: 1rem; margin-top: 1.5rem; font-size: .9rem;
    }
    .error { background: #fef2f2; color: #991b1b; }
    .chip {
      display: inline-block; background: #e0e7ff; color: #3730a3;
      padding: .2rem .6rem; border-radius: 999px; font-size: .8rem;
      margin-right: .3rem;
    }
    footer {
      padding: 1rem 2rem;
      background: #f9fafb;
      font-size: .85rem;
      color: #6b7280;
      text-align: center;
      border-top: 1px solid #f3f4f6;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>👁️ Vision Artificial - Deteccion de Rostros</h1>
      <p>Sube una imagen y detecta rostros automaticamente. Compatible con OpenCV 4.x y 5.x.</p>
    </header>
    <div class="content">
      <label class="drop">
        <input type="file" id="archivo" accept="image/*" />
        <div id="dropTexto">
          <strong>Arrastra una imagen aqui</strong><br/>
          o haz click para seleccionar un archivo
        </div>
      </label>
      <div style="text-align:center;">
        <button id="btnDetectar">🔍 Detectar rostros</button>
      </div>
      <div id="resultado" class="grid" style="display:none;">
        <div class="card">
          <h3>Imagen original</h3>
          <img id="imgOriginal" alt="Original" />
        </div>
        <div class="card">
          <h3>Rostros detectados <span id="chipCount" class="chip">0</span></h3>
          <img id="imgProcesada" alt="Procesada" />
          <div style="margin-top:.5rem;" id="chipModelo"></div>
        </div>
      </div>
      <div id="mensaje"></div>
    </div>
    <footer>
      Taller 3 Machine Learning — Jonathan Martinez · OpenCV + FastAPI
    </footer>
  </div>
<script>
  const input     = document.getElementById('archivo');
  const btn       = document.getElementById('btnDetectar');
  const resultado = document.getElementById('resultado');
  const imgOrig   = document.getElementById('imgOriginal');
  const imgProc   = document.getElementById('imgProcesada');
  const chipCnt   = document.getElementById('chipCount');
  const chipMod   = document.getElementById('chipModelo');
  const mensaje   = document.getElementById('mensaje');

  let archivoActual = null;

  input.addEventListener('change', e => {
    archivoActual = e.target.files?.[0] || null;
  });

  btn.addEventListener('click', async () => {
    if (!archivoActual) {
      mensaje.className = 'info error';
      mensaje.textContent = 'Primero selecciona una imagen.';
      return;
    }
    mensaje.className = '';
    mensaje.textContent = '';
    btn.disabled = true;
    btn.textContent = 'Procesando...';
    const fd = new FormData();
    fd.append('imagen', archivoActual);
    try {
      const res = await fetch('/detectar', { method: 'POST', body: fd });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error desconocido');
      const blob = new Blob([archivoActual], { type: archivoActual.type });
      imgOrig.src = URL.createObjectURL(blob);
      imgProc.src = 'data:image/png;base64,' + data.imagen_procesada;
      chipCnt.textContent = data.total_rostros + ' rostros';
      chipMod.innerHTML = '<span class="chip">' + data.modelo_usado + '</span>';
      resultado.style.display = 'grid';
      mensaje.className = 'info';
      mensaje.innerHTML = '<strong>Listo!</strong> Se detectaron ' +
        data.total_rostros + ' rostro(s). Coordenadas: ' +
        JSON.stringify(data.rostros);
    } catch (err) {
      mensaje.className = 'info error';
      mensaje.textContent = 'Error: ' + err.message;
    } finally {
      btn.disabled = false;
      btn.textContent = '🔍 Detectar rostros';
    }
  });
</script>
</body>
</html>
"""


@app.on_event("startup")
async def startup_event() -> None:
    index_path = templates_dir / "index.html"
    index_path.write_text(INDEX_HTML, encoding="utf-8")
    _cargar_detector()


@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def pagina_inicio(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health", tags=["Sistema"])
async def salud():
    _cargar_detector()
    return {
        "estado": "ok",
        "opencv_version": cv2.__version__,
        "clasificador_cargado": _clasificador is not None,
        "yunet_cargado": _detector_yunet is not None and _detector_yunet is not True,
    }


@app.post("/detectar", tags=["Deteccion"])
async def detectar(imagen: UploadFile = File(...)):
    data = await imagen.read()
    if not data:
        raise HTTPException(status_code=400, detail="La imagen esta vacia.")
    img_bgr = _bytes_a_imagen(data)
    rostros, modelo = _detectar_rostros(img_bgr)
    salida = img_bgr.copy()
    for (x, y, w, h) in rostros:
        cv2.rectangle(salida, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(
            salida,
            f"x{x},y{y}",
            (x, max(0, y - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )
    return {
        "total_rostros": len(rostros),
        "rostros": [
            {"x": x, "y": y, "ancho": w, "alto": h} for (x, y, w, h) in rostros
        ],
        "modelo_usado": modelo,
        "imagen_procesada": _imagen_a_png_base64(salida),
    }
