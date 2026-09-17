from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np
import base64
import os
import urllib.request

app = Flask(__name__, static_folder="../public")

BASE_DIR = os.path.dirname(__file__)
RAIZ_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
RUTA_XML = os.path.join(RAIZ_DIR, "Modelos_ML", "Visionartificial", "haarcascade_frontalface_default.xml")
RUTA_YUNET_LOCAL = os.path.join(RAIZ_DIR, "Modelos_ML", "Visionartificial", "face_detection_yunet.onnx")
MODELO_YUNET_URL = (
    "https://github.com/opencv/opencv_zoo/raw/main/models/"
    "face_detection_yunet/face_detection_yunet_2023mar.onnx"
)

_clasificador = None
_detector_yunet = None


def _descargar_yunet_si_falta() -> bool:
    if os.path.exists(RUTA_YUNET_LOCAL):
        return True
    try:
        os.makedirs(os.path.dirname(RUTA_YUNET_LOCAL), exist_ok=True)
        urllib.request.urlretrieve(MODELO_YUNET_URL, RUTA_YUNET_LOCAL)
        return True
    except Exception:
        return False


def _cargar_detector():
    global _clasificador, _detector_yunet
    if _clasificador is not None or _detector_yunet is not None:
        return

    if hasattr(cv2, "CascadeClassifier") and os.path.exists(RUTA_XML):
        cls = cv2.CascadeClassifier(RUTA_XML)
        if not cls.empty():
            _clasificador = cls
            return

    if _descargar_yunet_si_falta():
        _detector_yunet = "pending"


def _detectar(imagen_bgr: np.ndarray):
    _cargar_detector()
    global _clasificador, _detector_yunet

    rostros = []
    altura, ancho = imagen_bgr.shape[:2]

    if _clasificador is not None:
        gris = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)
        resultado = _clasificador.detectMultiScale(
            gris, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
        )
        for r in resultado:
            rostros.append([int(v) for v in r])
        return rostros, "Haar Cascade (OpenCV 4.x)"

    if _detector_yunet == "pending":
        try:
            _detector_yunet = cv2.FaceDetectorYN_create(
                RUTA_YUNET_LOCAL, "", (ancho, altura), 0.6, 0.3, 5000
            )
        except Exception:
            return [], "YuNet no disponible"
    if _detector_yunet not in (None, "pending"):
        try:
            _detector_yunet.setInputSize((ancho, altura))
        except Exception:
            pass
        try:
            _, res = _detector_yunet.detect(imagen_bgr)
        except Exception:
            return [], "YuNet error"
        if res is not None:
            for det in res:
                x, y, w, h = int(det[0]), int(det[1]), int(det[2]), int(det[3])
                if w > 0 and h > 0:
                    rostros.append([x, y, w, h])
        return rostros, "YuNet FaceDetectorYN (OpenCV 5.x)"

    return [], "Ningun detector disponible"


@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    if path in ("", None):
        return serve_index()
    try:
        return send_from_directory(app.static_folder, path)
    except Exception:
        return serve_index()


@app.route("/health", methods=["GET"])
def health():
    _cargar_detector()
    return jsonify(
        {
            "estado": "ok",
            "opencv_version": cv2.__version__,
            "clasificador_haar_cargado": _clasificador is not None,
            "yunet_cargado": _detector_yunet is not None and _detector_yunet != "pending",
            "rutas": {
                "GET /": "UI web",
                "GET /health": "Estado del servicio",
                "POST /api/detectar": "Enviar imagen multipart/form-data (campo: imagen)",
                "POST /api/detect": "Alias de /api/detectar (campo: image)",
            },
        }
    )


@app.route("/api/detectar", methods=["POST"])
def detectar():
    campo = "imagen" if "imagen" in request.files else "image"
    if campo not in request.files:
        return jsonify({"error": "No se proporciono ninguna imagen. Usa el campo 'imagen' o 'image'."}), 400

    archivo = request.files[campo]
    try:
        datos = archivo.read()
        nparr = np.frombuffer(datos, dtype=np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({"error": "Formato de imagen invalido"}), 400

        salida = img.copy()
        rostros, modelo = _detectar(img)

        for x, y, w, h in rostros:
            cv2.rectangle(salida, (x, y), (x + w, y + h), (0, 0, 255), 3)
            cv2.putText(
                salida, f"({x},{y})", (x, max(0, y - 8)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
            )

        ok, buffer = cv2.imencode(".jpg", salida, [int(cv2.IMWRITE_JPEG_QUALITY), 88])
        if not ok:
            return jsonify({"error": "No se pudo codificar la imagen procesada"}), 500
        imagen_b64 = base64.b64encode(buffer.tobytes()).decode("ascii")

        return jsonify(
            {
                "success": True,
                "total_rostros": len(rostros),
                "faces_detected": len(rostros),
                "modelo_usado": modelo,
                "rostros": [
                    {"x": x, "y": y, "ancho": w, "alto": h}
                    for (x, y, w, h) in rostros
                ],
                "image": f"data:image/jpeg;base64,{imagen_b64}",
                "imagen_procesada": imagen_b64,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/detect", methods=["POST"])
def detect_alias():
    return detectar()


_cargar_detector()
app.debug = False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
