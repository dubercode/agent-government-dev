import re

ENVIRONMENT = {
    "prod": "prod",
    "producción": "prod",
    "production": "prod",
    "dev": "dev",
    "desarrollo": "dev",
    "qa": "qa",
}

CRITICALITY = {
    "crítico": "alta",
    "critico": "alta",
    "alta": "alta",
    "media": "media",
    "baja": "baja",
}

WORKLOADS = {
    "analytics": "analytics-sandbox",
    "portal": "portal-interno",
    "plataforma": "plataforma-core",
    "core": "core-operativo",
}

RESOURCE_TYPES = {
    "storage": "storage_account",
    "almacenamiento": "storage_account",
    "key vault": "key_vault",
    "sql": "sql_database",
    "vm": "virtual_machine",
    "aks": "aks",
}


def parse_intent(text: str):
    t = text.lower()

    entities = {}

    rg = re.search(r"rg-[a-z0-9-]+", t)

    if rg:
        entities["resource_group"] = rg.group()

    for k, v in ENVIRONMENT.items():
        if k in t:
            entities["environment"] = v
            break

    for k, v in CRITICALITY.items():
        if k in t:
            entities["criticality"] = v
            break

    for k, v in WORKLOADS.items():
        if k in t:
            entities["workload"] = v

    for k, v in RESOURCE_TYPES.items():
        if k in t:
            entities["resource_type"] = v

    if any(x in t for x in ["inventario", "recursos", "resource", "grupo"]):
        intent = "inventory_query"

    elif any(x in t for x in ["costo", "cost", "anomal", "gasto"]):
        intent = "cost_anomaly"

    elif any(x in t for x in ["terraform", "storage", "crear", "generar"]):
        intent = "generate_terraform"

    elif any(x in t for x in ["remedi", "finding", "seguridad", "f-"]):
        intent = "security_remediation"

    else:
        intent = "help"

    return {
        "intent": intent,
        "entities": entities,
        "confidence": 0.95,
    }