from pathlib import Path

# RUTA DEL PROYECTO (Raíz)
BASE_DIR = Path(__file__).parent

# CONFIGURACION DEL SISTEMA
from config_entorno import configurar_entorno
configurar_entorno(BASE_DIR) 

# CARGA DE HERRAMIENTAS
from pathlib import Path
from modulos_datos.conf_csv import crear_sesion, leer_csv
from modulos_datos.limpiar_texto import limpiar_texto
from modulos_datos.paralelizacion import paralelizar, escribir_lotes_disco
from modulos_model_IA.entrenar_modelo import entrenamiento
from modulos_model_IA.utilidades_modelo import guardar_modelo, cargar_modelo
from modulos_model_IA.crear_modelo import dividir_datos
from modulos_model_IA.prediccion import predecir

# RUTA DEL PROYECTO
BASE_DIR = Path(__file__).parent

# PROCESO DE PREPARACION DE DATOS 
def pipeline(spark, BASE_DIR):
    # LECTURA DE INFORMACION
    df = leer_csv(spark, BASE_DIR)
    df.groupBy("etiqueta").count().show()
    # LIMPIEZA DE TEXTO
    df_limpio = limpiar_texto(df)
    # SEPARACION PARA APRENDIZAJE Y PRUEBAS
    df_train, df_test = dividir_datos(df_limpio)
    # ORGANIZACION DEL TRABAJO
    df_train = paralelizar(df_train, 8)
    # GUARDADO DE PRUEBAS
    escribir_lotes_disco(df_test, 10, str(BASE_DIR / "inputs" / "lotes"))
    return df_train

# REVISION DE LA EXISTENCIIA DEL MODELO, SI NO EXISTE LO CREA
def comprobar_modelo(df_train, BASE_DIR):
    ruta_modelo = BASE_DIR / "outputs" / "modelo_sentimientos"
    if ruta_modelo.exists():
        return cargar_modelo(BASE_DIR)
    else:
        modelo = entrenamiento(df_train)
        guardar_modelo(modelo, BASE_DIR)
        return modelo

# ADIVINAR SENTIMIENTO DE UN TEXTO, SE USA PARA PRUEBAS
def predecir_texto(spark, modelo, texto):
    from pyspark.sql.types import StructType, StructField, StringType
    # ESTRUCTURA PARA EL TEXTO NUEVO
    schema = StructType([
        StructField("texto", StringType(), True),
        StructField("etiqueta", StringType(), True)
    ])
    df = spark.createDataFrame([(texto, None)], schema=schema)
    dflimpio = limpiar_texto(df)
    dfresultado = predecir(dflimpio, modelo)
    dfresultado.show()
    
# INICIO DEL PROGRAMA
def main():
    # INICIO DE LA SESION
    spark = crear_sesion()
    # PREPARACION
    df_train = pipeline(spark, BASE_DIR)
    # OBTENCION DEL MODELO
    modelo = comprobar_modelo(df_train, BASE_DIR)
    # PRUEBA FINAL
    predecir_texto(spark, modelo, "I loved the product")
    # CIERRE
    spark.stop()

# EJECUCION
if __name__ == "__main__":
    main()


