from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score
from collections import Counter

def precision_stats(coleccion, BASE_DIR):
    print("Iniciando cálculo de estadísticas")
    #TRAER SOLO DOCUMENTOS CON ORIGINALLABEL
    documentos = list(coleccion.find({"etiqueta_original": {"$ne": None}}))

    if not documentos:
        return None

    #EXTRAER ETIQUETAS REALES Y PREDICHAS
    reales    = [doc["etiqueta_original"] for doc in documentos]
    predichas = [doc["prediccion_texto"]    for doc in documentos]

    #DISTRIBUCIÓN
    distribucion = dict(Counter(predichas))

    #ACCURACY
    accuracy = accuracy_score(reales, predichas)

    #MATRIZ DE CONFUSIÓN
    clases = ["positivo", "negativo", "neutral"]
    matriz = confusion_matrix(reales, predichas, labels=clases)

    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor("#051526")
    ax.set_facecolor("#051526")
    sns.heatmap(matriz, annot=True, fmt="d", cmap="Blues",
                xticklabels=clases, yticklabels=clases, ax=ax)
    ax.set_xlabel("Predicción", color="#c5cdd9")
    ax.set_ylabel("Real", color="#c5cdd9")
    ax.tick_params(colors="#c5cdd9")
    plt.tight_layout()

    ruta_img = BASE_DIR / "outputs" / "confusion_matrix.png"
    plt.savefig(ruta_img)
    plt.close()
    print("Cálculo de estadísticas finalizado")

    return {
        "total"        : len(documentos),
        "accuracy"     : round(accuracy, 4),
        "distribucion" : distribucion,
        "matriz_imagen": "/outputs/confusion_matrix.png"
    }