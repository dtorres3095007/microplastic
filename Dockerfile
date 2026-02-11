# Utiliza la imagen base de Python slim
FROM python:3.8-slim

# Instala las dependencias necesarias incluyendo GDAL y otras librerías necesarias para compilar extensiones
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    build-essential \
    python3-dev \
    python3-pip \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Zona horaria (Colombia)
ENV TZ=America/Bogota

# Establece las variables de entorno necesarias para GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_VERSION=3.6.2
ENV GDAL_CONFIG=/usr/bin/gdal-config

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . /app

EXPOSE 3000
# Iniciar Supervisor (FastAPI + cron)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]