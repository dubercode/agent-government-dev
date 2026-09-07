from pathlib import Path
import re

OUTPUT_PATH = Path("generated/terraform.tfvars")


def parse_tfvars():

    values = {}

    if not OUTPUT_PATH.exists():
        raise FileNotFoundError("terraform.tfvars no existe.")

    for line in OUTPUT_PATH.read_text().splitlines():

        if "=" not in line:
            continue

        k, v = line.split("=", 1)

        values[k.strip()] = v.strip().replace('"', "")

    return values


def validate():

    values = parse_tfvars()

    errors = []
    warnings = []

    required = [
        "environment",
        "workload",
        "criticality",
    ]

    for field in required:

        if field not in values:
            errors.append(f"Falta {field}")

    if "resource_name" in values:

        name = values["resource_name"]

        if len(name) > 24:
            errors.append("resource_name supera 24 caracteres.")

        if not re.match(r"^[a-z0-9-]+$", name):
            errors.append("resource_name contiene caracteres inválidos.")

    if values.get("environment") == "prod":
        warnings.append(
            "Ambiente de producción detectado."
        )

    if values.get("criticality") in ["alta", "critical"]:
        warnings.append(
            "Recurso crítico requiere revisión humana."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }