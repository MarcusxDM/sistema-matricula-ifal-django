# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY sistema_academico/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Final image
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    mariadb-client \
 && rm -rf /var/lib/apt/lists/*

# Copiar libs instaladas
COPY --from=builder /usr/local /usr/local

# Copiar projeto
COPY sistema_academico/ /app/sistema_academico/

# Gerar settings.py
RUN cp /app/sistema_academico/sistema_academico/settings.py.template /app/sistema_academico/sistema_academico/settings.py


ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=sistema_academico.settings



EXPOSE 8000

WORKDIR /app/sistema_academico

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Comando final para K8s
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]