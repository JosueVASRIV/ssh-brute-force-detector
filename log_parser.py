import re
from datetime import UTC, datetime


def extraer_intentos_fallidos(lineas):
    ips_fallidas = []
    usuarios_fallidos = []
    for linea in lineas:
        if "Failed password" in linea and "sshd" in linea:
            para_ips = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", linea)
            para_usuarios = re.search(r"for (?:invalid user )?(\S+) from", linea)
            para_timestamp = re.search(r"^(\w{3} \d{1,2} \d{2}:\d{2}:\d{2})", linea)

            if para_timestamp and para_ips:
                timestamp = para_timestamp.group(1)
                timestamp_dt = datetime.strptime(timestamp, "%b %d %H:%M:%S").replace(tzinfo=UTC)
                ip = para_ips.group(1)
                ips_fallidas.append((ip, timestamp_dt))
            if para_usuarios:
                usuarios = para_usuarios.group(1)
                usuarios_fallidos.append(usuarios)
            
    return ips_fallidas, usuarios_fallidos
