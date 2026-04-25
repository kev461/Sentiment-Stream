from datetime import datetime, timezone

# GUARDAR RESULTADOS EN LA BASE DE DATOS
def guardar_predicciones(coleccion, df_final):
    # RECOGER TODA LA INFORMACION ACTUAL
    filas = df_final.collect()
    
    # PREPARAR LA LISTA DE DOCUMENTOS
    documentos = []
    for fila in filas:
        # CREAR UN REGISTRO CON TODA LA INFORMACION SOLICITADA
        documento = {
            "texto"            : fila["texto"],
            "etiqueta_original": fila["OriginalLabel"],
            "prediccion_texto" : fila["prediccion"],
            "prediccion_nro"   : int(fila["prediction"]),
            "probabilidades"   : [float(p) for p in fila["probability"]],
            "confianza"        : float(fila["probability"][int(fila["prediction"])]),
            "timestamp"        : datetime.now(timezone.utc)
        }
        documentos.append(documento)
    
    # SI HAY INFORMACION SE GUARDA TODA DE GOLPE
    if documentos:
        coleccion.insert_many(documentos)
