FROM python:3.10-slim

WORKDIR /app 

COPY requirements.txt .
RUN  pip install --no-cache-dir -r requirements.txt

COPY . .

# Deja los CSS y JavaScript listos para ser servidos por WhiteNoise.
RUN python manage.py collectstatic --noinput

CMD gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}
