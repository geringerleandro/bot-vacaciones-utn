from datetime import datetime
import os

# ============================================================
# BLOQUE 0: CONSTANTES Y CONFIGURACIÓN
# ============================================================

# Rutas a los archivos CSV que actúan como base de datos
RUTA_EMPLEADOS="data/empleados.csv"
RUTA_SOLICITUDES="data/solicitudes.csv"

# Reglas de negocio definidas en el análisis sistémico
MAX_INTENTOS=3   # Máximo de errores consecutivos antes de derivar al usuario
UMBRAL_DIAS=10  # Solicitudes que superen este valor requieren aprobación de RRHH

# ============================================================
# BLOQUE 1: FUNCIONES DE LECTURA DE DATOS
# ============================================================

def cargar_empleados():
    """
    Lee el CSV de empleados y lo convierte en una lista de diccionarios.
    Retorna una lista de diccionarios con los datos de cada empleado.
    """
    empleados = []
    with open(RUTA_EMPLEADOS, "r", encoding="utf-8") as archivo:
        next(archivo) # Saltamos la línea de encabezados
        for linea in archivo:
            campos = linea.strip().split(",")
            empleados.append({
                "id_empleado"           : int(campos[0]),
                "nombre_completo"       : campos[1],
                "saldo_dias_disponibles": int(campos[2])
            })
    return empleados

def cargar_solicitudes():
    """
    Lee el CSV de solicitudes y lo convierte en una lista de diccionarios.
    Retorna una lista de diccionarios con los datos de cada solicitud registrada.
    """
    solicitudes = []
    with open(RUTA_SOLICITUDES, "r", encoding="utf-8") as archivo:
        next(archivo) # Saltamos la línea de encabezados
        for linea in archivo:
            campos = linea.strip().split(",")
            solicitudes.append({
                "id_solicitud"    : int(campos[0]),
                "id_empleado"     : int(campos[1]),
                "fecha_inicio"    : campos[2],
                "fecha_fin"       : campos[3],
                "dias_solicitados": int(campos[4]),
                "estado"          : campos[5],
                "fecha_registro"  : campos[6]
            })
    return solicitudes

# ============================================================
# BLOQUE 2: FUNCIONES DE VALIDACIÓN
# ============================================================

def buscar_empleado(id_empleado, empleados):
    """
    Busca un empleado por su ID en la lista de empleados cargada.
    Parámetros: id_empleado (int), empleados (list de dicts).
    Retorna el diccionario del empleado si lo encuentra, o None si no existe.
    """
    for empleado in empleados:
        if empleado["id_empleado"] == id_empleado:
            return empleado
    return None

def valida_formato_fecha(texto):
    """
    Verifica que un string tenga formato de fecha válido (AAAA-MM-DD).
    Retorna True si el formato es válido, False si no lo es.
    """
    try:
        datetime.strptime(texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def fecha_es_pasada(fecha_str):
    """
    Verifica si una fecha ya pasó respecto al día de hoy.
    Retorna True si la fecha es anterior a hoy.
    """
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    hoy = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    return fecha < hoy

def fin_anterior_a_inicio(inicio_str, fin_str):
    """
    Verifica si la fecha de fin es anterior o igual a la fecha de inicio.
    Retorna True si el rango de fechas es inválido.
    """
    inicio = datetime.strptime(inicio_str, "%Y-%m-%d")
    fin    = datetime.strptime(fin_str, "%Y-%m-%d")
    return fin <= inicio

def calcular_dias_solicitados(inicio_str, fin_str):
    """
    Calcula la cantidad de días corridos entre dos fechas.
    Retorna un entero con la diferencia en días.
    """
    inicio = datetime.strptime(inicio_str, "%Y-%m-%d")
    fin    = datetime.strptime(fin_str, "%Y-%m-%d")
    return (fin - inicio).days

# ============================================================
# BLOQUE 3: FUNCIONES DE LÓGICA DE NEGOCIO
# ============================================================

# (próximo commit)

# ============================================================
# BLOQUE 4: MÁQUINA DE ESTADOS Y FLUJO PRINCIPAL
# ============================================================

# (próximo commit)