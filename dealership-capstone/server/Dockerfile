FROM node:20-slim AS frontend-build
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

COPY . .
COPY --from=frontend-build /frontend/build ./frontend/build
RUN python manage.py collectstatic --noinput \
    && addgroup --system --gid 10001 app \
    && adduser --system --uid 10001 --ingroup app app \
    && mkdir -p /data \
    && chown -R app:app /app /data

ENV DJANGO_DB_PATH=/data/db.sqlite3 \
    DEBUG=False
USER app

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn djangoproj.wsgi:application --bind 0.0.0.0:8000 --workers 2"]
