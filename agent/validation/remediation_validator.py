from rich.console import Console

console = Console()


def validate_remediation(finding):

    if finding["severity"] == "Alta":

        console.print(
            "[yellow]Hallazgo crítico detectado.[/yellow]"
        )

    if not finding["auto_remediable"]:

        console.print(
            "[red]La ejecución automática está bloqueada para este hallazgo.[/red]"
        )

        return False

    return True

def execute_mock(finding):
    return f"""
Acción aprobada.

Modo simulación.

Se habría ejecutado:

{finding["recommended_action"]}

No se realizaron cambios reales.
"""