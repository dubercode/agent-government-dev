REGLA DE ARQUITECTURA: estas funciones nunca reciben texto libre del usuario,
solo un Intent ya estructurado por nlu/intent_parser.py. Si mañana cambiamos
el parser (reglas -> LLM), estas funciones no se enteran ni cambian.
"""

CAPABILITIES_TEXT = """Puedo ayudarte con 4 cosas:

1. Consultar inventario
   Ej: "¿qué recursos del grupo rg-ops-prod son críticos y están en producción?"

2. Detectar anomalías de costo
   Te muestro comportamientos inusuales en el histórico de 30 días, priorizados
   por severidad y criticidad del recurso.

3. Generar un proyecto de infraestructura
   Ej: "necesito una cuenta de almacenamiento para logs de analítica, dev, no crítica"
   Genero el archivo de variables de Terraform siguiendo el arquetipo entregado.

4. Proponer una remediación
   Tomo un hallazgo de seguridad y te doy una propuesta de acción concreta.
   La ejecución real SIEMPRE requiere tu confirmación explícita.

Escribe 'salir' para terminar."""


def handle_greeting() -> str:
    return "¡Hola! Soy tu agente de gobierno cloud. Escribe 'ayuda' para ver qué puedo hacer."


def handle_help() -> str:
    return CAPABILITIES_TEXT


def handle_unknown(intent) -> str:
    return (
        "Todavía no sé responder eso (el parser de intents reales se construye "
        "en el Paso 2). Escribe 'ayuda' para ver mis capacidades."
    )
