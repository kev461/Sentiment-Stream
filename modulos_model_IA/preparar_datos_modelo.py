from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer

# PREPARACION DE LOS PASOS DE APRENDIZAJE
def preparar_etapas():
    # SEPARAR EL TEXTO EN PALABRAS SUELTAS
    tokenizer = Tokenizer(inputCol="texto_limpio", outputCol="palabras")
    
    # QUITAR PALABRAS QUE NO APORTAN SIGNIFICADO
    remover = StopWordsRemover(
        inputCol="palabras",
        outputCol="palabras_filtradas",
        stopWords=StopWordsRemover.loadDefaultStopWords("english")
    )
    
    # CONVERTIR PALABRAS EN SEÑALES PARA LA MAQUINA
    hashing_tf = HashingTF(
        inputCol="palabras_filtradas",
        outputCol="tf_features",
        numFeatures=10000
    )
    
    # DAR PESO A LAS PALABRAS MAS IMPORTANTES
    idf = IDF(inputCol="tf_features", outputCol="features")
    
    # ASIGNAR UNA ETIQUETA A CADA SENTIMIENTO
    indexer = StringIndexer(inputCol="etiqueta", outputCol="OriginalLabel",handleInvalid="keep")
    
    # DEVOLVER TODA LA LISTA DE TAREAS
    return [tokenizer, remover, hashing_tf, idf, indexer]


