FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY manage.py ./manage.py
COPY config ./config
COPY app_prediccion ./app_prediccion

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN python manage.py collectstatic --noinput

ENV PORT=8000

EXPOSE ${PORT}

CMD gunicorn config.wsgi:application --bind 0.0.0.0:${PORT} --workers 2 --timeout 120
