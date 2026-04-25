import sys
from pathlib import Path

# Aseguramos que la raíz del proyecto esté en el path antes de importar nada
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from config_entorno import configurar_entorno
configurar_entorno(BASE_DIR)  # IMPORTANTE: ANTES DE IMPORTAR PYSPARK

from flask import Flask
from flask_cors import CORS
from routes import registrar_rutas

app = Flask(__name__)
CORS(app)
registrar_rutas(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)