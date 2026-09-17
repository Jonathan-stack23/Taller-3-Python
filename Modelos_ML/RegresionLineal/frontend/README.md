# Frontend Django — Habita

Interfaz para consultar el modelo de predicción que expone el backend FastAPI.

## Inicio local

1. Desde la raíz del proyecto, instala las dependencias del backend y del frontend:
   `pip install -r backend/requirements.txt -r frontend/requirements.txt`
2. En una terminal, inicia el backend desde la raíz del proyecto:
   `uvicorn backend.main:app --reload --port 8000`
3. En otra terminal, inicia Django desde la raíz del proyecto:
   `python frontend/manage.py runserver 8001`
4. Abre `http://127.0.0.1:8001`.

Por defecto Django reenvía las consultas a `http://127.0.0.1:8000/predict`. Si el backend está en otra dirección, define la variable de entorno `PREDICTION_API_URL` antes de iniciar Django. En Railway usa el dominio público del backend, preferiblemente con el protocolo: `https://mi-backend.up.railway.app`.
