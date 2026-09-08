def validate_remediation(finding):
    """
    Valida si una remediación puede proponerse automáticamente.
    """

    if not finding:
        return {
            "allowed": False,
            "reason": "Hallazgo inexistente."
        }

    if finding.get("severity", "").lower() == "alta" and not finding.get("auto_remediable", False):
        return {
            "allowed": False,
            "reason": "Hallazgo crítico requiere aprobación manual."
        }

    return {
        "allowed": True,
        "reason": "Remediación permitida."
    }