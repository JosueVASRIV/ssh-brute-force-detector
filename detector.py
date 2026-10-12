from collections import Counter, defaultdict


def contar_intentos(ips_fallidas, umbral=3):
    conteo = Counter(ips_fallidas)
    ips_sospechosas = {}

    for ip, cantidad in conteo.items():
        if cantidad >= umbral:
            ips_sospechosas[ip] = cantidad

    return ips_sospechosas

def detectar_por_ventana(ips_con_timestamp, umbral=3, ventana_segundos=60):
    ips_agrupados_por_timestamp = defaultdict(list)
    for ip, timestamp in ips_con_timestamp:
        ips_agrupados_por_timestamp[ip].append(timestamp)

    ips_sospechosas = {}

    for ip, timestamps in ips_agrupados_por_timestamp.items():
        timestamps.sort()
        for i, ts in enumerate(timestamps):
            if i + umbral - 1 < len(timestamps):
                diferencia = (timestamps[i+umbral-1] - ts).total_seconds()
                if diferencia < ventana_segundos:
                    ips_sospechosas[ip] = len(timestamps)
                    break
    return ips_sospechosas