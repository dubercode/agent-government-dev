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

# Cambia a True si quieres mostrar el JSON del intent
DEBUG = False


def load_datasets():
    inventory = json.loads(
        (DATASET_PATH / "inventory.json").read_text(encoding="utf-8")
    )["resources"]

    costs = json.loads(
        (DATASET_PATH / "costs.json").read_text(encoding="utf-8")
    )["daily_costs"]

    findings = json.loads(
        (DATASET_PATH / "security_findings.json").read_text(encoding="utf-8")
    )["findings"]

    return inventory, costs, findings


def show_banner(inventory, costs, findings):
    console.print(
        Panel.fit(
            "[bold cyan]Cloud Governance Agent[/bold cyan]\n"
            "Tenant: org-demo\n"
            f"Recursos: {len(inventory)}\n"
            f"Registros de costo: {len(costs)}\n"
            f"Findings: {len(findings)}",
            title="Mini Agente Gobierno Cloud",
        )
    )


def show_help():
    console.print(
        Panel(
            """[bold]Capacidades disponibles[/bold]

• Consulta inventario
• Detectar anomalías de costo
• Generar Terraform
• Proponer remediaciones

[bold]Ejemplos[/bold]

• ¿Qué recursos del grupo rg-ops-prod son críticos?
• Muéstrame QA
• Detecta anomalías de costo
• Genera una Storage Account para logs en dev
• Remedia F-001""",
            title="Ayuda",
        )
    )


def run_cli():

    inventory, costs, findings = load_datasets()

    show_banner(inventory, costs, findings)

    while True:

        try:
            user_input = console.input("\n[bold green]> [/bold green]").strip()

            if user_input.lower() in ["exit", "quit", "salir"]:
                console.print("\n[cyan]Hasta luego.[/cyan]")
                break

            intent = parse_intent(user_input)

            if DEBUG:
                console.print("\n[bold cyan]Intent detectado[/bold cyan]")
                console.print(intent)

            # INVENTARIO
            if intent["intent"] == "inventory_query":

                results = query_inventory(inventory, intent["entities"])

                console.print(build_inventory_table(results))

            # COSTOS
            elif intent["intent"] == "cost_anomaly":

                anomalies = detect_cost_anomalies(costs, inventory)

                console.print(build_cost_table(anomalies))

            # TERRAFORM
            elif intent["intent"] == "generate_terraform":

                output = generate_tfvars(intent["entities"])

                validation = validate_tfvars()

                console.print(f"\n[green]Archivo generado:[/green] {output}")

                if validation["warnings"]:
                    console.print("\n[bold yellow]Advertencias[/bold yellow]")
                    for warning in validation["warnings"]:
                        console.print(f"• {warning}")

                if validation["valid"]:
                    console.print("\n[bold green]✔ terraform.tfvars validado correctamente.[/bold green]")
                else:
                    console.print("\n[bold red]Errores encontrados[/bold red]")
                    for error in validation["errors"]:
                        console.print(f"• {error}")

            # REMEDIACIÓN
            elif intent["intent"] == "security_remediation":

                finding = get_finding(findings, user_input)

                if not finding:
                    console.print("[red]No encontré ese finding.[/red]")
                    continue

                validation = validate_remediation(finding)

                if not validation["allowed"]:
                    console.print(f"[red]{validation['reason']}[/red]")
                    continue

                console.print(build_remediation(finding))

                answer = console.input(
                    "\n¿Deseas ejecutar la remediación simulada? [s/N]: "
                )

                if answer.lower() == "s":
                    console.print(execute_mock(finding))
                else:
                    console.print("[yellow]Operación cancelada.[/yellow]")

            # AYUDA
            else:
                show_help()

        except KeyboardInterrupt:
            console.print("\n[cyan]Hasta luego.[/cyan]")
            break

        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {e}")