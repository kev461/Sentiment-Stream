from dotenv import load_dotenv
from pathlib import Path
import os
from pymongo import MongoClient


#CÓDIGO PRUEBA PARA PROBAR CONEXIÓN A MONGODB
ruta_env = Path(__file__).parent.parent / ".env"
load_dotenv(ruta_env)

cliente = MongoClient(os.getenv("MONGO_URI"))
db = cliente[os.getenv("MONGO_DB")]
print("Conexión exitosa:", db.name)
cliente.close()