# REPARTIR EL TRABAJO
def paralelizar(df_limpio, particiones):
    # SE DIVIDE LA INFORMACION EN VARIAS PARTES
    return df_limpio.repartition(particiones)

# GUARDAR LA INFORMACION POR PEDAZOS
def escribir_lotes_disco(df_test, particiones, ruta_lotes):
    # SE REPARTE Y SE ESCRIBE EN LA CARPETA ELEGIDA
    df_test.repartition(particiones).write.mode("overwrite").csv(ruta_lotes)

    
