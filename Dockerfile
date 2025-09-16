# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Dependências de build para compilar pacotes Python com extensões nativas
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

# Dependências do MySQL
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    mariadb-client \
 && rm -rf /var/lib/apt/lists/*

# Copiando dados do stage de build
COPY --from=builder /usr/local /usr/local

# Copiar projeto
COPY sistema_academico/ /app/

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
