from pathlib import Path
import re

ARCHETYPE_PATH = Path("arquetipo-storage-consumidor")
OUTPUT_PATH = Path("generated/terraform.tfvars")


def extract_variables():
    """
    Lee variables.tf del arquetipo y devuelve una lista
    con las variables declaradas.
    """

    variables_file = ARCHETYPE_PATH / "variables.tf"

    if not variables_file.exists():
        raise FileNotFoundError(
            "No encontré variables.tf dentro del arquetipo."
        )

    content = variables_file.read_text(encoding="utf-8")

    variables = re.findall(r'variable\s+"([^"]+)"', content)

    return variables


def build_defaults(intent_entities):
    """
    Convierte el intent del agente en valores Terraform.
    """

    env = intent_entities.get("environment", "dev")
    workload = intent_entities.get("workload", "analytics")
    criticality = intent_entities.get("criticality", "baja")

    resource_name = f"st-{workload.replace('_','-')}-{env}-logs"

    defaults = {
        "resource_name": resource_name,
        "environment": env,
        "criticality": criticality,
        "workload": workload,
        "purpose": "logs",
        "owner": "cloud-agent",
    }

    return defaults


def generate_tfvars(intent_entities):

    variables = extract_variables()

    values = build_defaults(intent_entities)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    lines = []

    for var in variables:

        value = values.get(var, "")

        if isinstance(value, bool):
            lines.append(f"{var} = {'true' if value else 'false'}")

        elif isinstance(value, (int, float)):
            lines.append(f"{var} = {value}")

        else:
            lines.append(f'{var} = "{value}"')

    OUTPUT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return OUTPUT_PATH