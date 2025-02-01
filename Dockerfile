# Use an official FastAPI image with Uvicorn and Gunicorn pre-configured
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 80
