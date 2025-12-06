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
    git \
    cron \
    supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece las variables de entorno necesarias para GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_VERSION=3.6.2
ENV GDAL_CONFIG=/usr/bin/gdal-config

WORKDIR /app

# Actualiza pip y setuptools

# Copia el archivo requirements.txt y lo instala
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# ---- AGREGADO PARA CRON ----
# Copiar cronjob al contenedor
COPY cronjob /etc/cron.d/predictor-cron
RUN chmod 0644 /etc/cron.d/predictor-cron
RUN crontab /etc/cron.d/predictor-cron

# Copiar script que ejecutará el predictor
COPY run_predictor.sh /app/run_predictor.sh
RUN chmod +x /app/run_predictor.sh

# ---- AGREGADO PARA SUPERVISOR ----
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 3000
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]