from rich.table import Table


def query_inventory(resources, entities):
    results = resources

    if "resource_group" in entities:
        results = [
            r for r in results
            if r["resource_group"] == entities["resource_group"]
        ]

    if "environment" in entities:
        results = [
            r for r in results
            if r["tags"]["environment"] == entities["environment"]
        ]

    if "criticality" in entities:
        results = [
            r for r in results
            if r["tags"]["criticidad"] == entities["criticality"]
        ]

    if "workload" in entities:
        results = [
            r for r in results
            if r["tags"]["workload"] == entities["workload"]
        ]

    return results


def build_inventory_table(results):
    table = Table(title=f"Resultados ({len(results)} recursos)")

    table.add_column("Resource ID")
    table.add_column("Tipo")
    table.add_column("Grupo")
    table.add_column("Env")
    table.add_column("Criticidad")

    for r in results:
        table.add_row(
            r["resource_id"],
            r["type"].split("/")[-1],
            r["resource_group"],
            r["tags"]["environment"],
            r["tags"]["criticidad"],
        )

    return table