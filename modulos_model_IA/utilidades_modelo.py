from pyspark.ml import PipelineModel

# GUARDAR LO APRENDIDO
def guardar_modelo(modelo, BASE_DIR):
    # SE DEFINE DONDE SE VA A GUARDAR
    ruta = str(BASE_DIR / "outputs" / "modelo_sentimientos")
    # SE ESCRIBE EL CEREBRO ARTIFICIAL EN EL DISCO
    modelo.write().overwrite().save(ruta)

# RECUPERAR LO APRENDIDO
def cargar_modelo(BASE_DIR):
    # SE BUSCA LA CARPETA DONDE ESTA GUARDADO
    ruta = str(BASE_DIR / "outputs" / "modelo_sentimientos")
    # SE TRAE EL CEREBRO ARTIFICIAL A LA MEMORIA
    return PipelineModel.load(ruta)