import sys

# COMPROBAR QUE LA INFORMACION ESTE BIEN
def verificar_datos(df):
    """
    Verifica que el DataFrame cumpla las condiciones mínimas antes de continuar con el pipeline.
    Se usa en Jenkins para detener el proceso si los datos no son válidos.
    """
    try:
        # REVISAR QUE NO ESTE VACIO
        assert df.count() > 0, "No hay datos para procesar"

        # VERIFICAR QUE EXISTAN LAS COLUMNAS ESPERADAS
        assert "texto"    in df.columns, "Falta la columna 'texto'"
        assert "etiqueta" in df.columns, "Falta la columna 'etiqueta'"

        # REVISAR QUE NO FALTEN DATOS EN LAS FILAS
        for col in df.columns:
            nulos = df.filter(df[col].isNull()).count()
            assert nulos == 0, f"Faltan datos en la columna {col}"

        # SI TODO ESTA BIEN SE AVISA
        print("Revision exitosa la informacion esta lista")

    except AssertionError as e:
        # SI HAY UN ERROR SE MUESTRA Y SE DETIENE EL PROGRAMA
        print(f"Problema encontrado: {e}")
        sys.exit(1)
