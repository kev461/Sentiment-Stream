from flask import render_template, request, jsonify, send_from_directory
from pathlib import Path
import sys
from pyspark.sql.types import StructType, StructField, StringType

#RUTAS DEL PROYECTO
BASE_DIR = Path(__file__).parent.parent

#AGREGAR RAÍZ AL PATH PARA IMPORTAR MÓDULOS
sys.path.insert(0, str(BASE_DIR))

from modulos_datos.conf_csv import crear_sesion
from modulos_datos.limpiar_texto import limpiar_texto
from modulos_model_IA.utilidades_modelo import cargar_modelo
from modulos_model_IA.prediccion import predecir
from flujos.conexion_mongo import conectar_mongo
from flujos.guardar_predicciones import guardar_predicciones
from flujos.consultar_stats import precision_stats

#INICIALIZAR SPARK Y MODELO UNA SOLA VEZ
spark  = crear_sesion("FlaskAPI")
modelo = cargar_modelo(BASE_DIR)

#CONEXIÓN MONGODB
cliente, coleccion = conectar_mongo()

#ESQUEMA REUTILIZABLE PARA PREDICCIONES INDIVIDUALES
SCHEMA_PREDICT = StructType([
    StructField("texto",    StringType(), True),
    StructField("etiqueta", StringType(), True)
])

def registrar_rutas(app):

    #SERVIR ARCHIVOS DE OUTPUTS
    @app.route('/outputs/<path:filename>')
    def servir_output(filename):
        return send_from_directory(BASE_DIR / 'outputs', filename)

    #SERVIR ARCHIVOS DE INPUTS (Para el dashboard .pbix)
    @app.route('/inputs/<path:filename>')
    def servir_input(filename):
        return send_from_directory(BASE_DIR / 'inputs', filename)

    #HOME
    @app.route('/')
    def index():
        return render_template('index.html')

    #PREDICCIONES (HISTORIAL)
    @app.route('/predicciones')
    def predicciones():
        filtro    = request.args.get('sentimiento', 'todos').lower().strip()
        query     = {} if filtro == 'todos' else {"prediccion": filtro}
        docs      = list(coleccion.find(query).sort("timestamp", -1).limit(100))
        return render_template('predicciones.html', predicciones=docs)

    #STATS VA A LA FUNCION PRECISION_STATS PARA CALCULAR PRECISION Y DISTRIBUCIONES
    @app.route('/stats')
    def stats():
        datos = precision_stats(coleccion, BASE_DIR)
        return render_template('stats.html', stats=datos)

    #PREDICT (POST)
    @app.route('/predict', methods=['POST'])
    def predict():
        body  = request.get_json()
        texto = body.get('texto', '').strip()

        if not texto:
            return jsonify({"error": "texto vacío"}), 400

        df       = spark.createDataFrame([(texto, None)], schema=SCHEMA_PREDICT)
        df_limpio = limpiar_texto(df)
        df_result = predecir(df_limpio, modelo)

        fila = df_result.collect()[0]

        # GUARDAR EN MONGODB
        guardar_predicciones(coleccion, df_result)

        return jsonify({
            "texto"     : texto,
            "prediccion": fila["prediccion"],
            "confianza" : float(fila["probability"].max())
        })

    #SENTIMENTS (API JSON PARA POWER BI)
    @app.route('/sentiments')
    def sentiments():
        filtro = request.args.get('sentimiento', 'todos').lower().strip()
        query  = {} if filtro == 'todos' else {"prediccion": filtro}
        # Aumentamos el límite a 1000 para que el dashboard sea más robusto
        docs   = list(coleccion.find(query).sort("timestamp", -1).limit(1000))
        for doc in docs:
            doc['_id'] = str(doc['_id'])
            if doc.get('timestamp'):
                doc['timestamp'] = doc['timestamp'].isoformat()
            
            # Extraemos la confianza como un número real para que Power BI lo sume/promedie
            if 'probability' in doc and isinstance(doc['probability'], list):
                doc['confianza'] = float(max(doc['probability']))
            else:
                doc['confianza'] = 0.0
                
        return jsonify(docs)