import json
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from agent.nlu.intent_parser import parse_intent
from agent.actions.inventory import query_inventory, build_inventory_table
from agent.actions.cost_anomaly import detect_cost_anomalies, build_cost_table
from agent.actions.remediation import (
    get_finding,
    build_remediation,
    execute_mock,
)
from agent.validation.remediation_validator import validate_remediation
from agent.actions.terraform_generator import generate_tfvars
from agent.validation.tfvars_validator import validate as validate_tfvars

console = Console()

DATASET_PATH = Path("dataset")



def load_datasets():
    inventory = json.loads((DATASET_PATH / "inventory.json").read_text())["resources"]
    costs = json.loads((DATASET_PATH / "costs.json").read_text())["daily_costs"]
    findings = json.loads(
        (DATASET_PATH / "security_findings.json").read_text()
    )["findings"]

    return inventory, costs, findings


def show_banner(inventory, costs, findings):
    console.print(
        Panel.fit(
            "[bold cyan]Cloud Governance Agent[/bold cyan]\n"
            f"Tenant: org-demo\n"
            f"Recursos: {len(inventory)}\n"
            f"Registros de costo: {len(costs)}\n"
            f"Findings: {len(findings)}",
            title="Mini Agente Gobierno Cloud",
        )
    )


def run_cli():
    inventory, costs, findings = load_datasets()

    show_banner(inventory, costs, findings)

    while True:
        user_input = console.input("\n[bold green]> [/bold green]")

        if user_input.lower() in ["exit", "quit", "salir"]:
            console.print("[yellow]Hasta luego.[/yellow]")
            break

        intent = parse_intent(user_input)

        console.print("\n[bold]Intent detectado:[/bold]")
        console.print(intent)

        console.print(
            "\n[italic]Los módulos de acciones se conectarán en los siguientes archivos.[/italic]"
        )