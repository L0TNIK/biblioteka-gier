FROM python:3.12-slim

WORKDIR /app

# Instalacja zależności systemowych potrzebnych dla psycopg
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Kopiowanie i instalacja bibliotek Pythona
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu backendu
COPY backend/ ./backend/

# Ustawienie folderu roboczego na backend, aby importy (np. import models) działały poprawnie
WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]