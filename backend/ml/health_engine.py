from __future__ import annotations

import pandas as pd


def calculate_sensor_health(
    observations: pd.DataFrame,
) -> pd.DataFrame:

    if observations.empty:
        return pd.DataFrame(
            columns=[
                "station_id",
                "sensor_id",
                "health_score",
                "status",
                "trend",
                "maintenance_risk",
                "anomaly_frequency",
                "communication_reliability",
            ]
        )

    rows = []

    grouped = observations.groupby(
        ["station_id", "sensor_id"]
    )

    for (station_id, sensor_id), group in grouped:

        total = len(group)

        anomaly_count = int(
            group.get(
                "anomaly_flag",
                pd.Series(False, index=group.index),
            ).fillna(False).sum()
        )

        communication_failures = int(
            group.get(
                "communication_fault",
                pd.Series(False, index=group.index),
            ).fillna(False).sum()
        )

        anomaly_frequency = (
            anomaly_count / total
            if total
            else 0
        )

        communication_reliability = (
            1
            - communication_failures / total
            if total
            else 1
        )

        health_score = 100 * (
            0.65
            * (1 - anomaly_frequency)
            + 0.35
            * communication_reliability
        )

        health_score = max(
            0,
            min(100, health_score),
        )

        if health_score >= 85:
            status = "HEALTHY"
        elif health_score >= 65:
            status = "WARNING"
        else:
            status = "CRITICAL"

        if len(group) >= 6:
            recent = group.tail(3)
            previous = group.iloc[-6:-3]

            recent_health = (
                recent.get(
                    "anomaly_flag",
                    pd.Series(
                        False,
                        index=recent.index,
                    ),
                ).mean()
            )

            previous_health = (
                previous.get(
                    "anomaly_flag",
                    pd.Series(
                        False,
                        index=previous.index,
                    ),
                ).mean()
            )

            if recent_health < previous_health:
                trend = "IMPROVING"
            elif recent_health > previous_health:
                trend = "DECLINING"
            else:
                trend = "STABLE"
        else:
            trend = "STABLE"

        if health_score < 50:
            risk = "HIGH"
        elif health_score < 75:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        rows.append(
            {
                "station_id": station_id,
                "sensor_id": sensor_id,
                "health_score": round(
                    health_score,
                    2,
                ),
                "status": status,
                "trend": trend,
                "maintenance_risk": risk,
                "anomaly_frequency": round(
                    anomaly_frequency,
                    4,
                ),
                "communication_reliability": round(
                    communication_reliability,
                    4,
                ),
            }
        )

    return pd.DataFrame(rows)