from datetime import UTC, datetime


def guardar_reporte(ips_sospechosas, usuarios_sospechosos=None, nombre_archivo="reporte.txt"):

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        ahora = datetime.now(UTC)
        archivo.write(ahora.strftime("%Y-%m-%d %H:%M:%S") + "\n")

        if not ips_sospechosas:
            archivo.write("No se detectaron IPs sospechosas")
        else:
            lineas = [f"{ip}: {cantidad} intentos\n" for ip, cantidad in ips_sospechosas.items()]
            archivo.writelines(lineas)

        archivo.write("\nUsuarios Sospechosos:\n")
        if not usuarios_sospechosos:
            archivo.write("No se detectaron usuarios sospechosos")
        else:
            lineas = [f"{usuario}: {cantidad} intentos \n" for usuario, cantidad in usuarios_sospechosos.items()]
            archivo.writelines(lineas)