from rich.table import Table


def get_finding(findings, user_input):

    text = user_input.upper()

    for finding in findings:
        if finding["finding_id"].upper() in text:
            return finding

    return None


def get_all_findings(findings):
    return findings


def build_findings_table(findings):

    table = Table(title="Hallazgos de Seguridad")

    table.add_column("ID", style="cyan")
    table.add_column("Recurso")
    table.add_column("Severidad")
    table.add_column("Fuente")

    for f in findings:
        table.add_row(
            f["finding_id"],
            f["resource_id"],
            f["severity"],
            f["source"],
        )

    return table


def build_remediation(finding):

    table = Table(title=f"Remediación {finding['finding_id']}")

    table.add_column("Campo")
    table.add_column("Valor")

    table.add_row("Recurso", finding["resource_id"])
    table.add_row("Severidad", finding["severity"])
    table.add_row("Descripción", finding["description"])
    table.add_row("Acción", finding["recommended_action"])

    return table


def execute_mock(finding):
    return (
        f"Remediación simulada ejecutada sobre "
        f"{finding['resource_id']}."
    )