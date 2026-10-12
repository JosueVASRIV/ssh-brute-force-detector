import logging
import os

logger = logging.getLogger(__name__)


def leer_log(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        logger.error(f"Error: El archivo '{ruta_archivo}' no existe.")
        return None

    if not os.path.isfile(ruta_archivo):
        logger.error(
            f"Error: '{ruta_archivo}' no es un archivo válido (puede ser un directorio)."
        )
        return None

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            return lineas

    except PermissionError:
        logger.error(f"ERROR: No tienes perimisos para leer '{ruta_archivo}'.")
        return None
    except UnicodeDecodeError:
        logger.error(
            f"ERROR: Problemas de codificacion en '{ruta_archivo}'. Intente otra codificacion."
        )
        return None
    except OSError as e:
        logger.error(f"ERROR de E/S al leer el archivo: {e}")
        return None
