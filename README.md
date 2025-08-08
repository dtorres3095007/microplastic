## 🚀 Microplasticos

Sigue estos pasos para levantar el entorno de desarrollo local usando Docker.

---

### 1️⃣ Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Mysql](https://www.mysql.com/)

Por otro lado, debes tener una cuenta en:

- [copernicus](https://identity.dataspace.copernicus.eu/)

Las credenciales creadas deben ser cargadas en las variables de entorno COPERNICUS_USER y COPERNICUS_PASSWORD. 

---

### 2️⃣ Clonar el repositorio e importar base de datos

```bash
git clone https://github.com/dtorres3095007/microplastic.git
cd microplastic
```

La base de datos compartida debe ser importada con el administrador de base de datos de preferencia y configurar las credenciales utilizadas en los archivos docker compose y .env.

### 3️⃣ Levantar los servicios con Docker

Ejecuta el siguiente comando para construir y levantar los contenedores:

```bash
docker-compose up --build
```

Esto iniciará dos servicios:

✅ Backend FastAPI en http://localhost:3000

✅ Base de datos MySQL en el puerto 3306

### 4️⃣ Acceder a la documentación de la API

Una vez levantado el backend, abre en tu navegador:

```bash
http://localhost:3000/docs
```

Aquí podrás probar todos los endpoints de forma interactiva usando Swagger UI.

### 5️⃣ Autenticación con API Key

Algunos endpoints requieren autenticación con API Key. Asegúrate de enviar el siguiente header:

```bash
x-api-key: valor-api-key
```

### 6️⃣ Variables de entorno.

Estas son las credenciales definidas por defecto en docker-compose.yml y el archivo .env:

- CHOKIDAR_USEPOLLING
- DATABASE_HOST
- DATABASE_PORT
- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD
- MEDIA_STORAGE_PATH
- MEDIA_BASE_URL
- API_KEY
- API_KEY_NAME
- COPERNICUS_USER
- COPERNICUS_PASSWORD

### 7️⃣ Almacenamiento de archivos multimedia

Los archivos multimedia se guardan en:

```bash
/app/media
```

Este directorio está montado como volumen (media-data) y accesible desde:

```bash
http://localhost:3000/media/
```

### 8️⃣ Apagar los servicios

Cuando termines de trabajar, puedes detener todo estando dentro de la terminal con:

```bash
CTRL + C
```

### 9️⃣ Ejecutar descarga de imágenes y entrenamiento de modelos

Para iniciar la descarga de imágenes satelitales y el entrenamiento de los modelos, ejecuta:

```bash
python trainer_model.py
```

### 🔟 Ejecutar predicciones

Para correr las predicciones con el modelo entrenado, ejecuta:

```bash
python trainer_predictor.py
```
