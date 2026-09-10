import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
VENDOR_DIR = BASE_DIR / "_vendor"
if VENDOR_DIR.exists():
    sys.path.insert(0, str(VENDOR_DIR))

from contextlib import asynccontextmanager
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    BASE_DIR = Path(__file__).resolve().parent
    MODEL_PATH = BASE_DIR / "models/linear_model.joblib"
    try:
        model = joblib.load(MODEL_PATH)
    except Exception:
        model = None
    yield
    model = None

app = FastAPI(
    title="API de Predicción de Precios de Viviendas",
    description="Predicción de precios de viviendas según su superficie",
    version="1.0",
    lifespan=lifespan
)

# Definir el esquema de entrada para la predicción
class housem2(BaseModel):
    area_m2: float = Field(..., example=82.5, description="Superficie de la vivienda en metros cuadrados")
    
@app.get("/")
def health_check():
    return {"status": "OK","message": "API de Predicción de Precios de Viviendas está en funcionamiento.", "model_loaded": model is not None}

@app.post("/predict")
def predict(data: housem2):
    if not model:
        raise HTTPException(status_code=502, detail="Modelo no disponible. Por favor, intente más tarde.")
    
    prediction = model.predict([[data.area_m2]])[0]
    
    return {
        "area_m2": data.area_m2,
        "predicted_price": round(float(prediction), 2)
    }
