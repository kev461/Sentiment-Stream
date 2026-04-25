import sys
from pathlib import Path

# Asegurar que la raíz del proyecto esté en el path para las importaciones
sys.path.insert(0, str(Path(__file__).parent.parent))

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from modulos_model_IA.utilidades_modelo import cargar_modelo
from modulos_model_IA.prediccion import predecir
from modulos_datos.limpiar_texto import limpiar_texto
from flujos.conexion_mongo import conectar_mongo
from flujos.guardar_predicciones import guardar_predicciones

# LEER DATOS QUE LLEGAN POCO A POCO
def leer_stream(spark, BASE_DIR):
    # RUTA DONDE APARECEN LOS NUEVOS ARCHIVOS
    CSV_PATH = str(BASE_DIR / "inputs" / "stream" )
    # ORGANIZACION DE LOS DATOS
    schema = StructType([
        StructField("texto",    StringType(), nullable=True),
        StructField("etiqueta", StringType(), nullable=True)
    ])
    # INICIAR LECTURA CONSTANTE
    df = spark.readStream.format("csv") \
    .option("header", "true") \
    .schema(schema) \
    .option("sep", ",") \
    .load(CSV_PATH)
    return df

# PROCESAR UN GRUPO DE DATOS
def procesar_lote(df, coleccion, modelo, idLote):
    print(f"Trabajando en el grupo actual")
    # LIMPIEZA DE TEXTO (Crea la columna 'texto_limpio')
    df_limpio = limpiar_texto(df)
    # ADIVINAR SENTIMIENTO
    dfpredicho = predecir(df_limpio, modelo)
    # GUARDAR EN LA BASE DE DATOS
    guardar_predicciones(coleccion, dfpredicho)
    
# INICIAR EL PROCESAMIENTO CONSTANTE DE LOTES SE QUEDA ESPERANDO NUEVOS ARCHIVOS
def iniciar_stream(spark, BASE_DIR):
    print("Iniciando Procesamiento en Tiempo Real")
    modelo = cargar_modelo(BASE_DIR)
    cliente, coleccion = conectar_mongo()
    # PREPARAR LA LECTURA
    df_stream = leer_stream(spark, BASE_DIR)
    # EMPEZAR A TRABAJAR POR GRUPOS
    query = df_stream.writeStream \
        .foreachBatch(lambda df, id_lote: procesar_lote(df, coleccion, modelo, id_lote)) \
        .option("checkpointLocation", str(BASE_DIR / "outputs" / "checkpoint")) \
        .start()

    # MANTENER EL PROGRAMA FUNCIONANDO
    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        print("Stream detenido.")
    finally:
        # CERRAR CONEXIONES
        cliente.close()
        spark.stop()
        
# EJECUCION PRINCIPAL DEL FLUJO
if __name__ == "__main__":
    from pathlib import Path
    BASE_DIR = Path(__file__).parent.parent
    
    from config_entorno import configurar_entorno
    configurar_entorno(BASE_DIR)
    
    from modulos_datos.conf_csv import crear_sesion
    spark = crear_sesion()
    iniciar_stream(spark, BASE_DIR)
