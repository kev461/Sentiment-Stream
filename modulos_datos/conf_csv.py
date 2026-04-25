from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
import os
import sys
import platform

# PREPARAR EL PROGRAMA PARA WINDOWS
if platform.system() == "Windows":
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# CREAR LA CONEXION PRINCIPAL
def crear_sesion(app_name="SentimentStreamSession"):
    '''
    Creo una sesión de Spark "local[*] significa que usaré todos los nucleos del CPU"
    '''
    spark = SparkSession.builder \
    .appName(app_name) \
    .master("local[*]") \
    .getOrCreate()
    #PARA QUE SOLO MUESTRE ADVERTENCIAS Y ERRORES.
    spark.sparkContext.setLogLevel("WARN")
    return spark

# LEER LOS CSV 
def leer_csv(spark, BASE_DIR):
    # SE BUSCA LA CARPETA CON LOS DATOS SIN PROCESAR
    path_str = str(BASE_DIR / "inputs" / "Sin procesar").replace('\\', '/')
    CSV_PATH = f"file:///{path_str}"
    # SE DEFINE COMO ESTA ORGANIZADA LA INFORMACION
    schema = StructType([
        StructField("texto",    StringType(), nullable=True),
        StructField("etiqueta", StringType(), nullable=True)
    ])
    # SE CARGAN LOS DATOS AL PROGRAMA
    df = spark.read.format("csv") \
    .option("header", "true") \
    .schema(schema) \
    .option("sep", ",") \
    .load(CSV_PATH)
    return df
