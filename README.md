SentimentStream: Pipeline de Análisis de Sentimientos en Tiempo Real
SentimentStream es un ecosistema integrado de Big Data diseñado para la ingesta, procesamiento, almacenamiento y visualización de sentimientos a partir de flujos de datos continuos. El proyecto implementa un pipeline de extremo a extremo que combina procesamiento en streaming, aprendizaje automático y visualización interactiva.

Arquitectura del Sistema
El sistema se divide en cinco capas funcionales orquestadas mediante Docker Compose:

Capa de Stream: Simulación de flujo de datos a partir de un dataset de 500 registros etiquetados, enviando micro-lotes para su procesamiento.
Capa de Procesamiento (PySpark): Pipeline de NLP que realiza limpieza de texto, tokenización, vectorización (TF-IDF) y clasificación de sentimientos utilizando el modelo Naive Bayes.
Capa de Persistencia (MongoDB Atlas): Almacenamiento en la nube de las predicciones, incluyendo el texto original, la etiqueta predicha, la confianza del modelo y marcas de tiempo.
Capa de Exposición (Flask API): API REST robusta que permite consultar las estadísticas del flujo (/stats), listar predicciones (/sentiments) y realizar inferencias sobre nuevos textos (/predict).
Capa de Visualización (Power BI): Dashboard dinámico conectado a la API que permite monitorear la distribución de sentimientos y la evolución temporal de los datos.

Tecnologías Utilizadas
Procesamiento: Apache Spark (PySpark)
Base de Datos: MongoDB Atlas (NoSQL)
Backend: Flask (Python)
Visualización: Power BI Desktop + ngrok
DevOps: Docker, Docker Compose y Jenkins
Seguridad: Manejo de secretos mediante variables de entorno y Jenkins Credentials.

Configurar variables de entorno: Cree un archivo .env basado en .env.example con sus credenciales de MongoDB Atlas y su Token de ngrok.
Levantar la infraestructura:
bash
docker-compose up -d
Acceder a la aplicación:
Web UI: http://localhost:5000
API Stats: http://localhost:5000/stats
Túnel Público: Verifique la URL en los logs de sentiment_ngrok.


Estructura del proyecto:



modulos\_datos/

Lectura, limpieza y división del dataset en lotes.



modulos\_model\_IA/

Construcción, entrenamiento, evaluación y persistencia del modelo de machine learning.



modulos\_stream/

Simulación del flujo de datos e inferencia en tiempo real con Spark Structured Streaming.



flujos/

Conexión y operaciones con MongoDB Atlas.



api\_flask/

API REST para exponer las predicciones y estadísticas del modelo.



flujos\_docker\_jenkins/

Orquestación de servicios con Docker Compose y pipeline de CI/CD con Jenkins.



inputs/

Dataset original y carpetas generadas durante la ejecución del stream.



outputs/

Modelo entrenado, lotes, carpeta de llegada de archivos simulando stream, checkpoint del stream.





Cómo conectar Power BI a la API (Jenkins/Local)
Si la dirección de la API cambia (ej. al usar Jenkins), siga estos pasos:

En Power BI, vaya a Inicio > Transformar datos > Editar parámetros.
Cambie el valor de URL_Base por la IP actual (ej: http://192.168.1.2:5000). El :5000 es el puerto del flask
Haga clic en Aceptar y luego en Aplicar cambios.

