# =============================================================================
# VisionML - Backend Flask Serverless para Vercel
# Personalizado por: Jonathan Martinez
# Taller 3 Machine Learning · SENA
# Compatibilidad dual: OpenCV 4 (Haar Cascade) · OpenCV 5 (YuNet DNN ONNX)
# =============================================================================
from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np
import base64
import os
import urllib.request

app = Flask(__name__, static_folder="../public")

# -----------------------------------------------------------------------------
# Configuración de rutas (py_img-main vive dentro de Modelos_ML/py_img-main)
# El XML Haar y el ONNX YuNet están en la RAIZ de py_img-main al lado de /api
# -----------------------------------------------------------------------------
BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_XML = os.path.join(BASE, "..", "haarcascade_frontalface_default.xml")
RUTA_YUNET_LOCAL = os.path.join(BASE, "..", "face_detection_yunet.onnx")
URL_YUNET = (
    "https://github.com/opencv/opencv_zoo/raw/main/models/"
    "face_detection_yunet/face_detection_yunet_2023mar.onnx"
)

# Estado global de detectores (cargados una sola vez por cold-start)
clasificador_haar = None
detector_yunet = None
modelo_usado_por_defecto = None
_info_inicializacion = {}


def _descargar_yunet_si_falta():
    """Descarga el modelo YuNet ONNX oficial si no existe localmente."""
    if os.path.exists(RUTA_YUNET_LOCAL) and os.path.getsize(RUTA_YUNET_LOCAL) > 1_000_000:
        return True
    try:
        _info_inicializacion["yunet_descargando"] = True
        urllib.request.urlretrieve(URL_YUNET, RUTA_YUNET_LOCAL)
        _info_inicializacion["yunet_descargando"] = False
        return os.path.exists(RUTA_YUNET_LOCAL) and os.path.getsize(RUTA_YUNET_LOCAL) > 1_000_000
    except Exception as exc:
        _info_inicializacion["yunet_error_descarga"] = str(exc)
        return False


def _inicializar_detectores():
    """Carga el Haar Cascade y/o YuNet. Compatible con OpenCV 4 y 5."""
    global clasificador_haar, detector_yunet, modelo_usado_por_defecto

    # 1. Intentar Haar Cascade (solo existe en OpenCV <5.x)
    if hasattr(cv2, "CascadeClassifier") and os.path.exists(RUTA_XML):
        clasificador_haar = cv2.CascadeClassifier(RUTA_XML)
        if not clasificador_haar.empty():
            modelo_usado_por_defecto = "Haar Cascade (OpenCV {})".format(cv2.__version__)
            _info_inicializacion["haar"] = "OK"
            return

    # 2. Fallback: YuNet DNN (si OpenCV >= 5.0 sin CascadeClassifier directo,
    #    o si el XML Haar no cargó por alguna razón)
    if _descargar_yunet_si_falta() and hasattr(cv2, "FaceDetectorYN_create"):
        try:
            detector_yunet = cv2.FaceDetectorYN_create(
                RUTA_YUNET_LOCAL, "", (320, 320), 0.6, 0.3, 5000
            )
            modelo_usado_por_defecto = "YuNet DNN (OpenCV {})".format(cv2.__version__)
            _info_inicializacion["yunet"] = "OK"
            return
        except Exception as exc:
            _info_inicializacion["yunet_error_init"] = str(exc)

    # 3. Caso límite: ni Haar ni YuNet disponibles
    modelo_usado_por_defecto = "No disponible"
    _info_inicializacion["error"] = (
        "No se pudo inicializar ningún detector. Verifica OpenCV y archivos."
    )


# Ejecutar la inicialización en frío (import-time)
_inicializar_detectores()


# -----------------------------------------------------------------------------
# Helpers de detección
# -----------------------------------------------------------------------------
def _detectar_rostros(imagen_bgr):
    """
    Detecta rostros en una imagen BGR.
    Retorna: (lista_de_rostros, modelo_usado_str)
             lista_de_rostros = [ {"x":int,"y":int,"ancho":int,"alto":int}, ... ]
    """
    rostros_salida = []
    modelo = modelo_usado_por_defecto

    alto, ancho = imagen_bgr.shape[:2]

    # Ruta 1: Haar Cascade
    if clasificador_haar is not None and not clasificador_haar.empty():
        gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
        cajas = clasificador_haar.detectMultiScale(
            gris, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
        )
        for (x, y, w, h) in cajas:
            rostros_salida.append({"x": int(x), "y": int(y), "ancho": int(w), "alto": int(h)})
        return rostros_salida, modelo or "Haar Cascade"

    # Ruta 2: YuNet DNN (OpenCV 5)
    if detector_yunet is not None:
        detector_yunet.setInputSize((ancho, alto))
        ok, resultados = detector_yunet.detect(imagen_bgr)
        if resultados is not None and len(resultados) > 0:
            for det in resultados:
                # det = [x, y, w, h, x_reojo, y_reojo, x_ojo_i, ... , score]
                x, y, w, h = det[0], det[1], det[2], det[3]
                if w > 0 and h > 0:
                    rostros_salida.append(
                        {"x": int(x), "y": int(y), "ancho": int(w), "alto": int(h)}
                    )
        return rostros_salida, modelo or "YuNet DNN"

    return rostros_salida, modelo or "N/A"


def _dibujar_rectangulos(imagen_bgr, rostros):
    """Pinta los bounding-box y un pequeño texto de coordenadas."""
    salida = imagen_bgr.copy()
    for idx, r in enumerate(rostros, start=1):
        x, y, w, h = r["x"], r["y"], r["ancho"], r["alto"]
        # Rectángulo principal verde BGR=(52, 211, 153)
        cv2.rectangle(salida, (x, y), (x + w, y + h), (52, 153, 211), 3)
        # Pequeña etiqueta superior con el número de rostro
        etiqueta = "Rostro #{}".format(idx)
        (tw, th), _ = cv2.getTextSize(etiqueta, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(salida, (x, y - th - 10), (x + tw + 6, y), (52, 153, 211), -1)
        cv2.putText(
            salida, etiqueta, (x + 3, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA,
        )
    return salida


# -----------------------------------------------------------------------------
# Rutas HTTP
# -----------------------------------------------------------------------------
@app.route("/")
def servir_indice():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:ruta>")
def servir_estaticos(ruta):
    try:
        return send_from_directory(app.static_folder, ruta)
    except Exception:
        return servir_indice()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "estado": "operativo" if modelo_usado_por_defecto != "No disponible" else "fallido",
        "app": "VisionML - py_img-main personalizado",
        "autor": "Jonathan Martinez",
        "proyecto": "Taller 3 - Machine Learning (SENA)",
        "repositorio": "https://github.com/Jonathan-stack23/Taller-3-Python.git",
        "opencv_version": cv2.__version__,
        "haar_cargado": clasificador_haar is not None and not clasificador_haar.empty(),
        "yunet_cargado": detector_yunet is not None,
        "modelo_activo": modelo_usado_por_defecto,
        "rutas_disponibles": [
            {"metodo": "GET", "path": "/", "descripcion": "UI Frontend VisionML"},
            {"metodo": "GET", "path": "/health", "descripcion": "Healthcheck del servicio"},
            {"metodo": "POST", "path": "/api/detect",
             "descripcion": "Detectar rostros en multipart/form-data campo 'image'"},
            {"metodo": "POST", "path": "/api/detectar",
             "descripcion": "Alias español - campo 'imagen' o 'image'"},
        ],
        "info_inicializacion": _info_inicializacion,
    })


@app.route("/api/detect", methods=["POST"])
def detectar_api():
    return _manejar_deteccion()


@app.route("/api/detectar", methods=["POST"])
def detectar_api_alias():
    return _manejar_deteccion()


def _manejar_deteccion():
    """Punto de entrada unificado /api/detect y /api/detectar."""
    # Aceptar ambos nombres de campo: "image" (py_img original) y "imagen" (español)
    archivo = None
    if "image" in request.files:
        archivo = request.files["image"]
    elif "imagen" in request.files:
        archivo = request.files["imagen"]

    if archivo is None:
        return (
            jsonify({
                "success": False,
                "error": "No se recibió ninguna imagen. Usa el campo 'image' o 'imagen'.",
            }),
            400,
        )

    try:
        # 1. Decodificar la imagen subida
        buffer_bytes = archivo.read()
        arreglo_np = np.frombuffer(buffer_bytes, np.uint8)
        imagen_bgr = cv2.imdecode(arreglo_np, cv2.IMREAD_COLOR)

        if imagen_bgr is None:
            return (
                jsonify({"success": False, "error": "Formato de imagen inválido."}),
                400,
            )

        # 2. Ejecutar detección + dibujo
        rostros, modelo = _detectar_rostros(imagen_bgr)
        imagen_procesada = _dibujar_rectangulos(imagen_bgr, rostros)

        # 3. Codificar a JPEG base64 (calidad 88, buen balance peso/calidad)
        ok, buffer_jpg = cv2.imencode(
            ".jpg", imagen_procesada, [int(cv2.IMWRITE_JPEG_QUALITY), 88]
        )
        if not ok:
            return jsonify({"success": False, "error": "Fallo al codificar la imagen."}), 500

        base64_str = base64.b64encode(buffer_jpg.tobytes()).decode("utf-8")
        data_uri = "data:image/jpeg;base64,{}".format(base64_str)

        return jsonify({
            "success": True,
            "total_rostros": len(rostros),
            "faces_detected": len(rostros),  # alias para compatibilidad py_img original
            "rostros": rostros,
            "modelo_usado": modelo,
            "autor": "Jonathan Martinez",
            "proyecto": "Taller 3 Machine Learning",
            "repositorio": "https://github.com/Jonathan-stack23/Taller-3-Python.git",
            "image": data_uri,             # dataURI completo para <img src=...>
            "imagen_procesada": base64_str,  # base64 pura (sin prefijo)
        })

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": "Excepción: {}".format(str(exc)),
        }), 500


# -----------------------------------------------------------------------------
# Entrada para Vercel + desarrollo local
# -----------------------------------------------------------------------------
app.debug = False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
