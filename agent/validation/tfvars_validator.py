from pathlib import Path

GENERATED = Path("generated/terraform.auto.tfvars")


def validate():

    result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }

    if not GENERATED.exists():
        result["valid"] = False
        result["errors"].append("No existe terraform.auto.tfvars.")
        return result

    content = GENERATED.read_text()

    if 'environment = "prod"' in content:
        result["warnings"].append(
            "Producción: revisar cifrado, tags y aprobación."
        )

    if 'criticality = "high"' in content:
        result["warnings"].append(
            "Recurso crítico requiere revisión adicional."
        )

    return result