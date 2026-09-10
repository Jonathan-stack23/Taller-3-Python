FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando para correr Django en producción usando Gunicorn
CMD gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}
