# SentimentStream: Pipeline de Análisis de Sentimientos en Tiempo Real

SentimentStream es un ecosistema integrado de Big Data diseñado para la ingesta, procesamiento, almacenamiento y visualización de sentimientos a partir de flujos de datos continuos. El proyecto implementa un pipeline de extremo a extremo que combina procesamiento en streaming, aprendizaje automático y visualización interactiva.

## Arquitectura del Sistema
El sistema se divide en cinco capas funcionales orquestadas mediante Docker Compose:

- Capa de Stream: Simulación de flujo de datos a partir de un dataset de 500 registros etiquetados, enviando micro-lotes para su procesamiento.
- Capa de Procesamiento (PySpark): Pipeline de NLP que realiza limpieza de texto, tokenización, vectorización (TF-IDF) y clasificación de sentimientos utilizando el modelo Naive Bayes.
- Capa de Persistencia (MongoDB Atlas): Almacenamiento en la nube de las predicciones, incluyendo el texto original, la etiqueta predicha, la confianza del modelo y marcas de tiempo.
- Capa de Exposición (Flask API): API REST robusta que permite consultar las estadísticas del flujo (/stats), listar predicciones (/sentiments) y realizar inferencias sobre nuevos textos (/predict).
- Capa de Visualización (Power BI): Dashboard dinámico conectado a la API que permite monitorear la distribución de sentimientos y la evolución temporal de los datos.

## Tecnologías Utilizadas
- Procesamiento: Apache Spark (PySpark)
- Base de Datos: MongoDB Atlas (NoSQL)
- Backend: Flask (Python)
- Visualización: Power BI Desktop + ngrok
- DevOps: Docker, Docker Compose y Jenkins
- Seguridad: Manejo de secretos mediante variables de entorno y Jenkins Credentials.

## Manual de Uso

Este proyecto está preparado para integración y despliegue continuo (CI/CD) utilizando Jenkins y un repositorio de GitHub. A continuación se detallan las instrucciones de uso:

### 1. Despliegue Automático con Jenkins
- Pipeline de Jenkins: El pipeline se encargará de construir las imágenes actualizadas de Docker y levantar toda la infraestructura (Spark, Flask, MongoDB, ngrok) mediante docker-compose.
- Carga de Variables de Entorno: Las variables de entorno necesarias para el funcionamiento del proyecto (como las credenciales de MongoDB Atlas y el token de ngrok) se cargan de forma segura a través de Jenkins Credentials. El pipeline inyecta estas credenciales durante el proceso de construcción y ejecución, evitando la necesidad de exponer archivos en el repositorio.

### 2. Uso Local (Alternativa sin Jenkins)
Si deseas levantar el ecosistema en tu máquina local:
1. Configurar credenciales: Crea un archivo .env en la raíz del proyecto basado en el archivo de ejemplo con tus credenciales de MongoDB Atlas y tu Token de ngrok. Las variables de entorno se leerán de este archivo al levantar los contenedores.
2. Levantar la infraestructura:
   docker-compose up --build -d

### 3. Acceso a la Aplicación
Una vez finalizado el despliegue exitosamente, los servicios estarán en funcionamiento:
- Web UI y API: Puedes acceder mediante la dirección local, o utilizando la propia IP de tu máquina servidor habilitando el puerto correspondiente.
- Túnel Público (ngrok): Puedes verificar la URL generada en los logs del contenedor ngrok o consultando el puerto local 4040 de la interfaz de ngrok. Además, puedes consumir la API directamente usando tu propia IP en lugar de usar ngrok.
  docker logs sentiment_ngrok

### 4. Cómo conectar Power BI a la API
El dashboard de Power BI consume la API expuesta a través de ngrok con su URL o utilizando la IP directa de tu servidor. Si utilizas ngrok y necesitas configurar o actualizar la URL de conexión, sigue estos pasos:
1. Identifica la URL pública de ngrok o tu propia IP.
2. Abre tu archivo de Power BI.
3. Ve a la sección Inicio > Transformar datos > Editar parámetros.
4. Cambia el valor del parámetro correspondiente por la URL de ngrok generada o por la IP de tu servidor.
5. Haz clic en Aplicar cambios para refrescar el modelo con los últimos datos de sentimientos.

## Estructura del Proyecto

- modulos_datos/: Lectura, limpieza y división del dataset original en lotes.
- modulos_model_IA/: Construcción, entrenamiento, evaluación y persistencia del modelo de machine learning.
- modulos_stream/: Simulación del flujo de datos e inferencia en tiempo real con Spark Structured Streaming.
- flujos/: Conexión y operaciones directas con la base de datos MongoDB Atlas.
- api_flask/: Aplicación backend y API REST para exponer las predicciones y estadísticas.
- flujos_docker_jenkins/: Archivos para la orquestación de servicios y pipeline de CI/CD.
- inputs/: Dataset original y carpetas generadas dinámicamente que simulan la llegada de archivos del stream.
- outputs/: Modelo entrenado persistido, lotes generados y punto de control del stream.
