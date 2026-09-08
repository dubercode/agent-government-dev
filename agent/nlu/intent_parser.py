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
    "logs": "logs",
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

    # Resource Group
    rg = re.search(r"rg-[a-z0-9-]+", t)
    if rg:
        entities["resource_group"] = rg.group()

    # Ambiente
    for k, v in ENVIRONMENT.items():
        if k in t:
            entities["environment"] = v
            break

    # Criticidad
    for k, v in CRITICALITY.items():
        if k in t:
            entities["criticality"] = v
            break

    # Workload
    for k, v in WORKLOADS.items():
        if k in t:
            entities["workload"] = v

    # Tipo de recurso
    for k, v in RESOURCE_TYPES.items():
        if k in t:
            entities["resource_type"] = v

    # Finding específico (F-001, F-002...)
    finding = re.search(r"f-\d+", t)
    if finding:
        entities["finding_id"] = finding.group().upper()

    # Solicitud de listar hallazgos
    if any(x in t for x in ["hallazgos", "hallazgo", "findings", "todos los findings"]):
        entities["list"] = True

    # -------------------------
    # Detección de intención
    # -------------------------

    if any(x in t for x in ["hallazgo", "hallazgos", "finding", "seguridad", "remedi", "f-"]):
        intent = "security_remediation"

    elif any(x in t for x in ["terraform", "storage", "almacenamiento", "crear", "generar"]):
        intent = "generate_terraform"

    elif any(x in t for x in ["costo", "cost", "anomal", "gasto"]):
        intent = "cost_anomaly"

    elif (
        any(x in t for x in ["inventario", "recursos", "resource", "grupo"])
        or "qa" in t
        or "prod" in t
        or "dev" in t
    ):
        intent = "inventory_query"

    else:
        intent = "help"

    return {
        "intent": intent,
        "entities": entities,
        "confidence": 0.95,
    }