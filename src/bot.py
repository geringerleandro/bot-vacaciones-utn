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

# (próximo commit)

# ============================================================
# BLOQUE 3: FUNCIONES DE LÓGICA DE NEGOCIO
# ============================================================

# (próximo commit)

# ============================================================
# BLOQUE 4: MÁQUINA DE ESTADOS Y FLUJO PRINCIPAL
# ============================================================

# (próximo commit)