from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pathlib import Path

# CARGAR VARIABLES DE ENTORNO

load_dotenv(Path(__file__).parent.parent / ".env")
# CARGAR DATOS SECRETOS DE CONEXION
load_dotenv()

# OBTENER LAS DIRECCIONES DE LA BASE DE DATOS
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB        = os.getenv("MONGO_DB")
MONGO_COLECCION = os.getenv("MONGO_COLECCION")

# FUNCION PARA CONECTARSE
def conectar_mongo():
    # INICIAR EL CLIENTE
    cliente    = MongoClient(MONGO_URI)
    # ELEGIR LA CARPETA DONDE SE GUARDA TODO
    coleccion  = cliente[MONGO_DB][MONGO_COLECCION]
    # DEVOLVER LA CONEXION LISTA
    return cliente, coleccion 
