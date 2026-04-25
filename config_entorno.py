import os
import urllib.request
from pathlib import Path
import platform

# PREPARACION DEL LUGAR DE TRABAJO
def configurar_entorno(BASE_DIR):
    """
    Configura las variables de entorno necesarias para ejecutar PySpark en Windows.
    Descarga winutils.exe y hadoop.dll si no existen y fuerza el uso de Java 17.
    """
    if platform.system() != "Windows":
        return 
    
    # CARPETAS DEL PROYECTO
    hadoop_dir = BASE_DIR / "hadoop"
    bin_dir = hadoop_dir / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)

    # DIRECCIONES PARA DESCARGAR HERRAMIENTAS
    winutils_url = "https://raw.githubusercontent.com/kontext-tech/winutils/master/hadoop-3.3.0/bin/winutils.exe"
    hadoop_dll_url = "https://raw.githubusercontent.com/kontext-tech/winutils/master/hadoop-3.3.0/bin/hadoop.dll"

    # DESCARGA DE HERRAMIENTA UNO
    if not (bin_dir / "winutils.exe").exists():
        print("Descargando herramienta necesaria para archivos...")
        try:
            urllib.request.urlretrieve(winutils_url, bin_dir / "winutils.exe")
        except Exception as e:
            print(f"Error descargando winutils: {e}")
            
    # DESCARGA DE HERRAMIENTA DOS
    if not (bin_dir / "hadoop.dll").exists():
        print("Descargando hadoop.dll...")
        try:
            urllib.request.urlretrieve(hadoop_dll_url, bin_dir / "hadoop.dll")
        except Exception as e:
            print(f"Error descargando hadoop.dll: {e}")

    # CONFIGURACION DE RUTAS INTERNAS
    os.environ["HADOOP_HOME"] = str(hadoop_dir)
    
    # ACTUALIZACION DE LA LISTA DE RUTAS
    os.environ["PATH"] = str(bin_dir) + os.pathsep + os.environ.get("PATH", "")
    
    # SELECCION DE LA VERSION CORRECTA DE JAVA
    os.environ["JAVA_HOME"] = r"C:\Program Files\Eclipse Adoptium\jdk-17.0.18.8-hotspot"
    
    # ASEGURAR QUE SE USE EL MISMO PROGRAMA DE PYTHON
    import sys
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

