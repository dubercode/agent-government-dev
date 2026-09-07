"""
Carga los datasets entregados (inventory, costs, security_findings) en memoria.

Este módulo NO interpreta lenguaje natural (eso es tarea de nlu/) ni decide
qué hacer con los datos (eso es tarea de actions/). Solo los pone disponibles.
"""

import json
from pathlib import Path

DATASET_DIR = Path(__file__).parent / "dataset"


def load_datasets() -> dict:
    inventory = _load_json("inventory.json")
    costs = _load_json("costs.json")
    findings = _load_json("security_findings.json")

    print(f"[dataset] Recursos de inventario cargados: {len(inventory)}")
    print(f"[dataset] Registros de costo cargados: {len(costs)}")
    print(f"[dataset] Hallazgos de seguridad cargados: {len(findings)}\n")

    return {
        "inventory": inventory,
        "costs": costs,
        "findings": findings,
    }


def _load_json(filename: str):
    path = DATASET_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"No encontré '{filename}' en {DATASET_DIR}. "
            "Coloca ahí los archivos de dataset (inventory.json, costs.json, "
            "security_findings.json)."
        )
    with open(path, encoding="utf-8") as f:
        return json.load(f)
