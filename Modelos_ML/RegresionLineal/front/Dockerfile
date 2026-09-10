FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

ENV PORT=8000

EXPOSE ${PORT}

CMD gunicorn config.wsgi:application --bind 0.0.0.0:${PORT}
