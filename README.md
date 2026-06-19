# Bot de Solicitud de Vacaciones

Trabajo Práctico Integrador — Organización Empresarial, TUPaD (UTN).

Simulador de chatbot que automatiza el proceso de solicitud de vacaciones de una empresa ficticia (Soluciones Industriales del Sur S.A.). El bot valida los datos ingresados por el empleado, consulta su saldo de días disponibles, detecta conflictos con licencias ya registradas y decide automáticamente si aprueba la solicitud o la deriva a Recursos Humanos.

## Proceso que automatiza

El flujo completo está modelado en BPMN 2.0 en `docs/diagrama_bpmn.png`. En resumen:

1. El empleado ingresa su ID.
2. Ingresa las fechas de inicio y fin deseadas.
3. El bot valida formato, rango de fechas, saldo disponible y posibles conflictos con licencias existentes.
4. Si la solicitud supera los 10 días corridos, se deriva a RRHH para aprobación manual. Si no, se aprueba automáticamente y se actualiza el saldo.

## Tecnologías utilizadas

- Python 3 (sin librerías externas)
- Persistencia mediante archivos CSV (simulando una base de datos)

Se elige Python por ser el lenguaje visto en la cursada. Como plataforma de despliegue real se propone WhatsApp Business API, aunque para esta entrega el bot se simula por consola.

## Cómo ejecutarlo

1. Cloná el repositorio.
2. Asegurate de tener Python 3 instalado.
3. Desde la raíz del proyecto, ejecutá:

```bash
python src/bot.py
```

El bot va a pedir el ID de empleado y las fechas deseadas por consola.

## Estructura del repositorio
bot-vacaciones-utn/

├── README.md
├── data/
│   ├── empleados.csv       # Padrón de empleados con saldo de días
│   └── solicitudes.csv     # Historial de solicitudes registradas
├── docs/
│   └── diagrama_bpmn.png   # Diagrama BPMN 2.0 (as-is / to-be)
└── src/
└── bot.py # Código del bot
└── .gitignore

## Estados del bot (máquina de estados)

El bot recuerda en qué paso del proceso se encuentra mediante una variable de estado:

- `INICIO`: pide y valida el ID de empleado.
- `PIDIENDO_FECHAS`: pide y valida las fechas solicitadas.
- `VALIDANDO_SALDO`: verifica si el saldo alcanza.
- `VALIDANDO_CONFLICTO`: verifica superposición con licencias existentes.
- `APROBANDO`: decide aprobación automática o derivación a RRHH.
- `DERIVADO_HUMANO`: se alcanza si el usuario supera 3 errores consecutivos.

## Datos de prueba

El archivo `data/empleados.csv` ya incluye 5 empleados con distintos saldos para poder probar todos los caminos del bot (saldo en cero, saldo alto, etc.). El archivo se sobrescribe automáticamente al finalizar cada ejecución para reflejar los cambios.

## Autor

Leandro Geringer — UTN.