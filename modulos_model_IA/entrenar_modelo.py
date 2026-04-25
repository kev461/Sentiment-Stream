from modulos_model_IA.crear_modelo import definir_Naive

# PROCESO DE APRENDIZAJE
def entrenamiento(df):
    # SE PREPARA LA RUTA DE TRABAJO
    pipeline=definir_Naive()
    # LA MAQUINA ESTUDIA LOS DATOS
    modelo=pipeline.fit(df)
    # DEVOLVER EL CEREBRO YA ENTRENADO
    return modelo