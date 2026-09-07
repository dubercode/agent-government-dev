from rich.panel import Panel


def get_finding(findings, user_text):

    text = user_text.upper()

    for finding in findings:

        if finding["finding_id"] in text:
            return finding

        if finding["resource_id"].lower() in user_text.lower():
            return finding

    return None


def build_remediation(finding):

    auto = "Sí" if finding["auto_remediable"] else "No"

    content = f"""
[bold]Finding[/bold]: {finding["finding_id"]}

[bold]Recurso[/bold]:
{finding["resource_id"]}

[bold]Severidad[/bold]:
{finding["severity"]}

[bold]Fuente[/bold]:
{finding["source"]}

[bold]Descripción[/bold]:
{finding["description"]}

[bold]Acción propuesta[/bold]:
{finding["recommended_action"]}

[bold]Auto-remediable[/bold]:
{auto}

[bold yellow]La ejecución siempre requiere confirmación humana.[/bold yellow]
"""

    return Panel(
        content,
        title="Propuesta de remediación",
    )


def execute_mock(finding):

    return f"""
Acción aprobada.

Modo simulación.

Se habría ejecutado:

{finding["recommended_action"]}

No se realizaron cambios reales.
"""