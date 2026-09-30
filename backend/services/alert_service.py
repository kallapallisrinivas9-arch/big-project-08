from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def create_alert(
    result: dict[str, Any],
) -> dict[str, Any] | None:

    state = result.get("state")

    if state == "NORMAL":
        return None

    if state == "COMMUNICATION_FAULT":
        alert_type = "COMMUNICATION"
        severity = "CRITICAL"

    elif state == "GENUINE_WEATHER_EVENT":
        alert_type = "GENUINE_WEATHER"
        severity = "WARNING"

    elif state == "SENSOR_FAULT":
        alert_type = "SENSOR_FAULT"
        severity = "CRITICAL"

    else:
        alert_type = "ANOMALY"
        severity = "WARNING"

    return {
        "alert_type": alert_type,
        "severity": severity,
        "station_id": result.get("station_id"),
        "sensor_id": result.get("sensor_id"),
        "message": result.get(
            "explanation",
            "Weather observation anomaly detected.",
        ),
        "timestamp": datetime.now(
            timezone.utc
        ),
        "status": "OPEN",
    }