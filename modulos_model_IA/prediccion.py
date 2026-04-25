from pyspark.sql import functions as F
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# FUNCION PARA ADIVINAR SENTIMIENTOS
def predecir(df, modelo):
    # EL MODELO PROCESA LA INFORMACION ES EL PREDICTO, PERO PARA SPARK ES .TRANSFORM
    df_predicciones = modelo.transform(df)
    
    # SE OBTIENEN LOS NOMBRES DE LAS CATEGORIAS
    indexer_model = modelo.stages[4]
    etiquetas = indexer_model.labels
    print(f"etiquetas: {etiquetas}")
    
    # SE TRADUCE EL RESULTADO DE SEÑALES A PALABRAS
    etiqueta_col = F.when(F.col("prediction") == 0.0, etiquetas[0])
    for i, etiqueta in enumerate(etiquetas[1:], 1):
        etiqueta_col = etiqueta_col.when(F.col("prediction") == float(i), etiqueta)

    # CONVERTIR ORIGINALLABEL NUMÉRICO A ETIQUETA DE TEXTO
    original_col = F.when(F.col("OriginalLabel") == 0.0, etiquetas[0])
    for i, etiqueta in enumerate(etiquetas[1:], 1):
        original_col = original_col.when(F.col("OriginalLabel") == float(i), etiqueta)
    original_col = original_col.otherwise("sin etiqueta")
        
    # SE ORGANIZA EL RESULTADO FINAL PARA MOSTRARLO
    df_final = df_predicciones.select(
        "texto",
        original_col.alias("OriginalLabel"),
        etiqueta_col.alias("prediccion"),
        "probability",
        "prediction"
    )
    return df_final


# FUNCION PARA MEDIR QUE TAN BIEN FUNCIONA
def evaluar(df):
    # SE CREA UN MEDIDOR DE ACIERTOS
    evaluador = MulticlassClassificationEvaluator(
        labelCol="OriginalLabel",
        predictionCol="prediction",
        metricName="accuracy"
    )
    # SE CALCULA LA PUNTUACION
    accuracy = evaluador.evaluate(df)
    print("La precisión del modelo es:", accuracy)
    return accuracy
