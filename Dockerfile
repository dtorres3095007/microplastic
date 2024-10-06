# Utiliza la imagen base de Python slim
FROM python:3.10-slim

# Instala las dependencias necesarias incluyendo GDAL y otras librerías necesarias para compilar extensiones
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    build-essential \
    python3-dev \
    python3-pip \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece las variables de entorno necesarias para GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_VERSION=3.6.2
ENV GDAL_CONFIG=/usr/bin/gdal-config

# Actualiza pip y setuptools
RUN pip install --upgrade pip setuptools wheel

# Copia el archivo requirements.txt y lo instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . /app
EXPOSE 5678
CMD ["/bin/bash", "-c", "tail -f /dev/null"]
