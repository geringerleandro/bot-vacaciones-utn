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

def saldo_insuficiente(empleado, dias_solicitados):
    """
    Verifica si el saldo disponible del empleado no alcanza los días solicitados.
    Retorna True si el saldo es insuficiente.
    """
    return empleado["saldo_dias_disponibles"] < dias_solicitados

def hay_conflicto_fechas(id_empleado, fecha_inicio_str, fecha_fin_str, solicitudes):
    """
    Verifica si el rango solicitado se superpone con alguna solicitud ya
    registrada (aprobada o pendiente) del mismo empleado.
    Retorna True si existe superposición de fechas.
    """
    nuevo_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
    nuevo_fin    = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
    for solicitud in solicitudes:
        # Solo nos interesan las solicitudes activas del mismo empleado
        if solicitud["id_empleado"] != id_empleado:
            continue
        if solicitud["estado"] not in ("Aprobada", "Pendiente_RRHH"):
            continue
        existente_inicio = datetime.strptime(solicitud["fecha_inicio"], "%Y-%m-%d")
        existente_fin    = datetime.strptime(solicitud["fecha_fin"], "%Y-%m-%d")
        if nuevo_inicio <= existente_fin and nuevo_fin >= existente_inicio:
            return True
    return False

def generar_id_solicitud(solicitudes):
    """
    Busca el ID más alto ya registrado y devuelve el siguiente disponible.
    Retorna un entero con el nuevo ID de solicitud.
    """
    if len(solicitudes) == 0:
        return 1
    id_maximo = solicitudes[0]["id_solicitud"]
    for solicitud in solicitudes:
        if solicitud["id_solicitud"] > id_maximo:
            id_maximo = solicitud["id_solicitud"]
    return id_maximo + 1

def actualizar_saldo_empleado(empleado, dias_solicitados):
    """
    Resta los días aprobados del saldo disponible del empleado.
    Modifica directamente el diccionario recibido (no retorna nada).
    """
    empleado["saldo_dias_disponibles"] -= dias_solicitados

def registrar_solicitud(solicitudes, id_empleado, fecha_inicio, fecha_fin, dias_solicitados, estado):
    """
    Crea el diccionario de la nueva solicitud y lo agrega a la lista.
    Retorna el diccionario de la solicitud recién creada.
    """
    nueva_solicitud = {
        "id_solicitud"    : generar_id_solicitud(solicitudes),
        "id_empleado"     : id_empleado,
        "fecha_inicio"    : fecha_inicio,
        "fecha_fin"       : fecha_fin,
        "dias_solicitados": dias_solicitados,
        "estado"          : estado,
        "fecha_registro"  : datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    }
    solicitudes.append(nueva_solicitud)
    return nueva_solicitud

# ============================================================
# BLOQUE 4: MÁQUINA DE ESTADOS Y FLUJO PRINCIPAL
# ============================================================

empleados   = cargar_empleados()
solicitudes = cargar_solicitudes()

estado_actual     = "INICIO"
empleado_actual   = None
fecha_inicio      = ""
fecha_fin         = ""
dias_solicitados  = 0

print("=== BOT DE SOLICITUD DE VACACIONES ===")

while estado_actual != "FINALIZADO":
    match estado_actual:
        case "INICIO":
            id_ingresado = input("Ingrese su ID de empleado: ")
            id_ingresado = int(id_ingresado)
            empleado_actual = buscar_empleado(id_ingresado, empleados)
            if empleado_actual is None:
                print("ERROR: No se encontró ningún empleado con ese ID.")
            else:
                print(f"Hola {empleado_actual['nombre_completo']}, tiene {empleado_actual['saldo_dias_disponibles']} días disponibles.")
                estado_actual = "PIDIENDO_FECHAS"

        case "PIDIENDO_FECHAS":
            fecha_inicio = input("Ingrese la fecha de inicio deseada (AAAA-MM-DD): ")
            fecha_fin    = input("Ingrese la fecha de fin deseada (AAAA-MM-DD): ")
            if fecha_es_pasada(fecha_inicio):
                print("ERROR: La fecha de inicio no puede ser anterior a hoy.")
            elif fin_anterior_a_inicio(fecha_inicio, fecha_fin):
                print("ERROR: La fecha de fin debe ser posterior a la de inicio.")
            else:
                dias_solicitados = calcular_dias_solicitados(fecha_inicio, fecha_fin)
                estado_actual = "VALIDANDO_SALDO"

        case "VALIDANDO_SALDO":
            if saldo_insuficiente(empleado_actual, dias_solicitados):
                print(f"ERROR: Saldo insuficiente. Disponible: {empleado_actual['saldo_dias_disponibles']} días, solicitados: {dias_solicitados}.")
                registrar_solicitud(solicitudes, empleado_actual["id_empleado"], fecha_inicio, fecha_fin, dias_solicitados, "Cancelada")
                estado_actual = "FINALIZADO"
            else:
                estado_actual = "VALIDANDO_CONFLICTO"

        case "VALIDANDO_CONFLICTO":
            if hay_conflicto_fechas(empleado_actual["id_empleado"], fecha_inicio, fecha_fin, solicitudes):
                print("ERROR: Las fechas ingresadas se superponen con una licencia ya registrada.")
                estado_actual = "PIDIENDO_FECHAS"
            else:
                estado_actual = "APROBANDO"

        case "APROBANDO":
            if dias_solicitados > UMBRAL_DIAS:
                registrar_solicitud(solicitudes, empleado_actual["id_empleado"], fecha_inicio, fecha_fin, dias_solicitados, "Pendiente_RRHH")
                print(f"Su solicitud de {dias_solicitados} días supera el umbral de aprobación automática. Fue derivada a RRHH.")
            else:
                registrar_solicitud(solicitudes, empleado_actual["id_empleado"], fecha_inicio, fecha_fin, dias_solicitados, "Aprobada")
                actualizar_saldo_empleado(empleado_actual, dias_solicitados)
                print(f"Solicitud aprobada automáticamente. Nuevo saldo disponible: {empleado_actual['saldo_dias_disponibles']} días.")
            estado_actual = "FINALIZADO"

print("=== FIN DE LA SIMULACIÓN ===")
