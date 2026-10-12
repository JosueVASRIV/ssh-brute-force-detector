import argparse
import logging
import os

from detector import contar_intentos, detectar_por_ventana
from log_parser import extraer_intentos_fallidos
from log_reader import leer_log
from reporte import guardar_reporte

ruta_archivo = os.path.join(os.path.dirname(__file__), "test_auth.log")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("detector.log")],
    )

    parser = argparse.ArgumentParser(description="Detector de fuerza bruta SSH")
    parser.add_argument("--umbral", type=int, default=3)
    args = parser.parse_args()

    lineas = leer_log(ruta_archivo)
    if lineas is not None:
        ips_fallidas, usuarios_fallidos = extraer_intentos_fallidos(lineas)
        ips_sospechosas = detectar_por_ventana(ips_fallidas, args.umbral)
        usuarios_sospechosos = contar_intentos(usuarios_fallidos, args.umbral)

        if ips_sospechosas:
            print("IPs Sospechosas de Fuerza Bruta")
            for ip, cantidad in ips_sospechosas.items():
                print(f" - {ip}: {cantidad} intentos")
        else:
            print("No se detectaron IPs sospechosas.")

        if usuarios_sospechosos:
            print("Usuarios Sospechosos de Fuerza Bruta")
            for usuario, cantidad in usuarios_sospechosos.items():
                print(f" - {usuario}: {cantidad} intentos")
        else:
            print("No se detectaron usuarios sospechosos.")
        guardar_reporte(ips_sospechosas, usuarios_sospechosos)


if __name__ == "__main__":
    main()
