from pathlib import Path
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="API de Predicción de Precios de Vivienda",
              description="Esta API permite predecir el precio de una vivienda en función de su superficie en metros cuadrados utilizando un modelo de regresión lineal previamente entrenado.",
              version="1.0.0")

# Permite que el frontend estático consulte la API desde el navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "linear_model.joblib"

try:
    # Cargar el modelo entrenado desde el archivo
    model = joblib.load(MODEL_PATH)
except Exception:
    model = None

class Housem2(BaseModel):
    area_m2: float = Field(..., example=82.5, description="Superficie de la vivienda en metros cuadrados", gt=0)

@app.get("/")
def health_check():
    """
    Endpoint de verificación de estado de la API.
    Retorna un mensaje indicando que la API está funcionando correctamente.
    """
    return {"status": "OK", "message": "API de Predicción de Precios de Vivienda está funcionando correctamente.","model_loaded": model is not None}

@app.post("/predict")
def predict_price(data: Housem2):
    """
    Endpoint para predecir el precio de una vivienda en función de su superficie.
    Recibe un objeto JSON con la superficie en metros cuadrados y retorna el precio estimado.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible. Por favor, intente más tarde.")
    
    # Realizar la predicción utilizando el modelo cargado
    prediction = model.predict([[data.area_m2]])[0]
    
    return {"area_m2": data.area_m2, "predicted_price": round(prediction, 2)}