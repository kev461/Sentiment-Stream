import sys
from pathlib import Path

# Asegurar que la raíz del proyecto esté en el path para las importaciones
sys.path.insert(0, str(Path(__file__).parent.parent))

import shutil
import time

# ENVIAR DATOS POCO A POCO A LA CARPETA STREAM PARA SER PROCESADOS
def stream(BASE_DIR, delay):
    # CARPETA DONDE ESTAN LAS PRUEBAS
    ruta_lotes = BASE_DIR / "inputs" / "lotes"
    archivos = sorted(ruta_lotes.glob("*.csv"))
    # CARPETA DE DESTINO PARA EL PROCESO
    ruta_stream = BASE_DIR / "inputs" / "stream"
    ruta_stream.mkdir(parents=True, exist_ok=True)
    # COPIAR CADA ARCHIVO CON UNA ESPERA
    for archivo in archivos:
        shutil.copy(archivo, ruta_stream / archivo.name)
        time.sleep(delay)
        print(f"Enviado: {archivo.name}")
        
# EJECUCION DE LA SIMULACION
if __name__ == "__main__":
    from pathlib import Path
    BASE_DIR = Path(__file__).parent.parent
    
    from config_entorno import configurar_entorno
    configurar_entorno(BASE_DIR)
    
    stream(BASE_DIR, delay=5)
