from pyspark.sql import functions as F

# PROCESO DE LIMPIEZA DE PALABRAS
def limpiar_texto(df):
    # PONER TODO EN MINUSCULAS, ELIMINAR CARACTERES ESPECIALES Y ESPACIOS EN BLANCO AUNQUE SEA EN INGLÉS, QUITAR ESPACIOS EXTRAS
    df_limpio = df \
    .withColumn("texto_limpio", F.lower(F.col("texto"))) \
    .withColumn("texto_limpio", F.regexp_replace(F.col("texto_limpio"), r"[^a-záéíóúüñ0-9\s]", "")) \
    .withColumn("texto_limpio", F.regexp_replace(F.col("texto_limpio"), r"\s+", " ")) \
    .withColumn("texto_limpio", F.trim(F.col("texto_limpio")))

    return df_limpio

