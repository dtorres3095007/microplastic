# Utiliza la imagen base de Python slim
FROM python:3.10-slim

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instala las dependencias necesarias incluyendo GDAL y otras librerías necesarias para compilar extensiones
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    build-essential \
    python3-dev \
    curl \
    git \
    cron \
    supervisor \
    tzdata \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Zona horaria (Colombia)
ENV TZ=America/Bogota

# Establece las variables de entorno necesarias para GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_CONFIG=/usr/bin/gdal-config

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . /app

# ---------- CRON ----------
# Copiar cronjob (DEBE terminar con línea en blanco)
COPY cronjob /etc/cron.d/predictor-cron
RUN chmod 0644 /etc/cron.d/predictor-cron && \
    crontab /etc/cron.d/predictor-cron

# Script ejecutable del predictor
COPY run_predictor.sh /app/run_predictor.sh
RUN chmod +x /app/run_predictor.sh

# ---- AGREGADO PARA SUPERVISOR ----
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 3000
# Iniciar Supervisor (FastAPI + cron)
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]