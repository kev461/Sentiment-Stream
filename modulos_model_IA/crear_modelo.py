from pyspark.ml import Pipeline
from pyspark.ml.classification import NaiveBayes
from modulos_model_IA.preparar_datos_modelo import preparar_etapas

def dividir_datos(df):
    """
    Lo usual es:
    from sklearn.model_selection import train_test_split
    X_train, X_test = train_test_split(df, test_size=0.2)
    
    Esto no es compatible con Spark, así que su homologación es:
    """
    dftrain, dftest = df.randomSplit([0.8, 0.2])
    return dftrain, dftest

# DEFINIR EL METODO DE APRENDIZAJE
def definir_Naive():
    # SE TRAEN LOS PASOS DE PREPARACION
    etapas = preparar_etapas()
    # SE ELIGE EL TIPO DE CEREBRO ARTIFICIAL
    naive_bayes = NaiveBayes(
        featuresCol="features",
        labelCol="OriginalLabel",
        smoothing=1.0,    # SI APARECEN PALABRAS NUEVAS SU PROBABILIDAD SUBE A 1 NO 0
        modelType="multinomial"  # PARA TRATAR TEXTO
    )
    # SE CREA LA RUTA DE TRABAJO COMPLETA
    return Pipeline(stages=etapas + [naive_bayes])
