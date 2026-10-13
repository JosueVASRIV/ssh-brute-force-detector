# SSH Brute-Force Log Detector

Herramienta en Python que analiza logs de autenticación de Linux (`auth.log`) para detectar ataques de fuerza bruta contra SSH. Identifica las IPs y los usuarios más atacados y genera un reporte con los resultados.

## Características

- Lee y valida el archivo de log, con manejo de errores (archivo inexistente, permisos, codificación).
- Filtra solo los intentos fallidos del servicio SSH (`sshd`), ignorando otros servicios como FTP o web que también registran "Failed password".
- Extrae IP, usuario y marca de tiempo de cada intento con expresiones regulares.
- **Detección por ventana de tiempo:** una IP es sospechosa si realiza al menos `umbral` intentos fallidos dentro de una ventana de 60 segundos (ráfagas típicas de un ataque automatizado).
- Detección de usuarios más atacados (por ejemplo `root` o `admin`), acumulando intentos desde distintas IPs.
- Umbral configurable desde la línea de comandos.
- Genera un reporte (`reporte.txt`) con fecha en UTC y un registro de eventos (`detector.log`).

## Estructura del proyecto

```text
.
├── main.py          # Punto de entrada: orquesta el flujo completo
├── log_reader.py    # Lectura y validación del archivo de log
├── log_parser.py    # Extracción de IPs, usuarios y timestamps con regex
├── detector.py      # Lógica de detección (conteo y ventana de tiempo)
├── reporte.py       # Generación del reporte en archivo
├── test_auth.log    # Log de prueba (mixto: SSH, FTP, nginx, líneas rotas)
└── .gitignore
```

## Requisitos

- Python **3.11 o superior** (se usa `datetime.UTC`)
- No requiere librerías externas, solo la biblioteca estándar.

## Instalación

```bash
git clone https://github.com/JosueVASRIV/ssh-brute-force-detector.git
cd ssh-brute-force-detector
```

## Uso

Ejecución con el umbral por defecto (3 intentos):

```bash
python main.py
```

Con un umbral personalizado:

```bash
python main.py --umbral 5
```

Por defecto el programa analiza el archivo `test_auth.log` incluido en el repositorio. Para analizar otro log, cambia la ruta definida en `main.py`.

## Ejemplo de salida

```text
IPs Sospechosas de Fuerza Bruta
 - 192.168.1.50: 5 intentos
 - 45.33.22.11: 5 intentos
 - 200.10.5.3: 4 intentos
Usuarios Sospechosos de Fuerza Bruta
 - root: 5 intentos
 - admin: 4 intentos
 - test: 5 intentos
```

Los intentos de `88.99.12.7` (servicio FTP) no aparecen en el resultado: el detector solo considera líneas de `sshd`.

## Archivos generados

- `reporte.txt`: resultados del análisis con fecha y hora en UTC.
- `detector.log`: registro de eventos y errores del programa.

Ambos se crean en cada ejecución y están excluidos del repositorio mediante `.gitignore`.

## Conceptos aplicados

- Módulo `os` y manejo de excepciones para lectura segura de archivos
- Expresiones regulares (`re`) con grupos de captura
- `collections.Counter` y `defaultdict` para agrupar y contar
- `datetime` con zonas horarias (`UTC`) y operaciones entre fechas
- `argparse` para argumentos de línea de comandos
- `logging` con un logger por módulo
- Separación de responsabilidades en módulos independientes

## Limitaciones y mejoras futuras

- La ventana de tiempo (60 segundos) está fija en el código; podría ser un argumento más.
- La detección de usuarios cuenta intentos totales, sin ventana de tiempo.
- Los logs de syslog no incluyen año, por lo que los timestamps se interpretan sin año real.
- Posible integración con APIs de threat intelligence (VirusTotal, AbuseIPDB) para enriquecer las IPs detectadas.
