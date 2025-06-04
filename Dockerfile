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
    && git config --global user.name "Damian Torres Niebles" \
    && git config --global user.email "damian9530007@gmail.com" \
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
EXPOSE 3000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
