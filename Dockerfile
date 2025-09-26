# Usar el mirror oficial de DockerHub en ECR Public (evita 429 Too Many Requests)
FROM public.ecr.aws/docker/library/python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Usuario no root
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

# 1) Copia requirements primero para aprovechar caché de capas
COPY requirements.txt .

# 2) Instala deps del sistema solo si hace falta compilar wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gcc \
  && pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
  && apt-get purge -y build-essential gcc \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/*

# 3) Copia el código
COPY app/ ./app/

EXPOSE 3000

# Ejecuta como usuario no root
USER app

# Uvicorn directo (opcional: gunicorn -k uvicorn.workers.UvicornWorker para prod)
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","3000"]
