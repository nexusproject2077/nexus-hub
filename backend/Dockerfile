# Nexus-Hub backend — image Cloud Run
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

# Dépendances d'abord (meilleure mise en cache des couches)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code applicatif + dernière valeur d'abonnés connue (fallback)
COPY . .

EXPOSE 8080

# Cloud Run fournit $PORT ; gunicorn sert l'app Flask "app" de main.py
CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 30 main:app
