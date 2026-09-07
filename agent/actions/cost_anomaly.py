import pandas as pd
from rich.table import Table


CRITICALITY_WEIGHT = {
    "alta": 3,
    "media": 2,
    "baja": 1,
}


def detect_cost_anomalies(costs, inventory):

    df = pd.DataFrame(costs)

    inv = {
        r["resource_id"]: r
        for r in inventory
    }

    anomalies = []

    for resource_id, group in df.groupby("resource_id"):

        group = group.sort_values("day").copy()

        group["rolling_mean"] = group["cost_usd"].rolling(
            7,
            min_periods=3
        ).mean()

        group["rolling_std"] = group["cost_usd"].rolling(
            7,
            min_periods=3
        ).std()

        group["z"] = (
            (group["cost_usd"] - group["rolling_mean"])
            / group["rolling_std"]
        )

        for _, row in group.iterrows():

            if pd.isna(row["z"]):
                continue

            if row["z"] > 2.5:

                resource = inv.get(resource_id)

                weight = CRITICALITY_WEIGHT[
                    resource["tags"]["criticidad"]
                ]

                increase = (
                    (row["cost_usd"] - row["rolling_mean"])
                    / row["rolling_mean"]
                ) * 100

                score = abs(row["z"]) * increase * weight

                anomalies.append({
                    "resource": resource_id,
                    "day": int(row["day"]),
                    "cost": round(row["cost_usd"], 2),
                    "average": round(row["rolling_mean"], 2),
                    "increase": round(increase, 1),
                    "priority_score": round(score, 1),
                    "environment": resource["tags"]["environment"],
                    "criticality": resource["tags"]["criticidad"],
                })

    anomalies.sort(
        key=lambda x: x["priority_score"],
        reverse=True,
    )

    return anomalies


def build_cost_table(anomalies):

    table = Table(title="Anomalías detectadas")

    table.add_column("Recurso")
    table.add_column("Día")
    table.add_column("Costo")
    table.add_column("% Incremento")
    table.add_column("Prioridad")

    for a in anomalies[:10]:
        table.add_row(
            a["resource"],
            str(a["day"]),
            f"${a['cost']}",
            f"{a['increase']}%",
            f"{a['priority_score']}",
        )

    return table